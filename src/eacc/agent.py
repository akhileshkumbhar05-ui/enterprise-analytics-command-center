from __future__ import annotations

import json
from typing import Any

from databricks.sdk import WorkspaceClient
from openai import OpenAI

from eacc.config import settings
from eacc.models import (
    AgentResponse,
    KnowledgeSource,
    RequestType,
    RoutingDecision,
    ToolStatus,
    ToolTrace,
)
from eacc.prompts import EACC_SYSTEM_PROMPT
from eacc.router import RequestRouter
from eacc.tools.enterprise_knowledge import (
    search_enterprise_knowledge,
)
from eacc.tools.genie_analytics import ask_genie


def build_model_client() -> OpenAI:
    """
    Create an OpenAI-compatible client routed through
    the Databricks Unity Gateway.
    """

    workspace = WorkspaceClient()

    auth_headers = workspace.config.authenticate()

    authorization = (
        auth_headers.get("Authorization")
        or auth_headers.get("authorization")
    )

    if not authorization:
        raise RuntimeError(
            "Unable to obtain Databricks authorization."
        )

    token = authorization.removeprefix("Bearer ")

    base_url = (
        f"{workspace.config.host.rstrip('/')}"
        "/ai-gateway/mlflow/v1"
    )

    return OpenAI(
        api_key=token,
        base_url=base_url,
    )


class EACCAgent:
    """
    Enterprise Analytics Command Center orchestration agent.

    Architecture:

        User request
            ↓
        Request router
            ↓
        ANALYTICS / KNOWLEDGE / HYBRID / GENERAL
            ↓
        Required enterprise tools executed deterministically
            ↓
        Tool observations
            ↓
        Foundation model synthesis
            ↓
        Final grounded answer

    The orchestration deliberately avoids multi-turn model tool calls
    because the selected Gemma endpoint does not support that pattern.
    """

    def __init__(
        self,
        client: OpenAI | None = None,
    ) -> None:
        self.client = client or build_model_client()

        self.router = RequestRouter(
            self.client
        )

    def _required_tools(
        self,
        routing: RoutingDecision,
    ) -> list[str]:
        """
        Convert a routing decision into the enterprise
        capabilities that must execute.
        """

        if routing.classification == RequestType.ANALYTICS:
            return [
                "genie_analytics",
            ]

        if routing.classification == RequestType.KNOWLEDGE:
            return [
                "enterprise_knowledge",
            ]

        if routing.classification == RequestType.HYBRID:
            return [
                "genie_analytics",
                "enterprise_knowledge",
            ]

        return []

    def run(
        self,
        question: str,
    ) -> AgentResponse:
        """
        Execute one complete EACC request.
        """

        if not question or not question.strip():
            return AgentResponse(
                answer="Please provide a question.",
            )

        user_question = question.strip()

        # ---------------------------------------------------------
        # 1. REASON / PLAN
        # ---------------------------------------------------------

        routing = self.router.classify(
            user_question
        )

        required_tools = self._required_tools(
            routing
        )

        # ---------------------------------------------------------
        # Runtime state
        # ---------------------------------------------------------

        traces: list[ToolTrace] = []

        tools_used: list[str] = []

        sources: list[KnowledgeSource] = []

        observations: list[dict[str, Any]] = []

        # ---------------------------------------------------------
        # 2. ACT / OBSERVE
        #
        # Execute every capability required by the routing decision.
        # ---------------------------------------------------------

        for tool_name in required_tools:

            tool_question = self._build_tool_question(
                tool_name=tool_name,
                user_question=user_question,
            )

            observation, trace, new_sources = (
                self._execute_tool(
                    tool_name=tool_name,
                    arguments={
                        "question": tool_question,
                    },
                )
            )

            tools_used.append(
                tool_name
            )

            traces.append(
                trace
            )

            self._merge_sources(
                existing=sources,
                incoming=new_sources,
            )

            observations.append(
                {
                    "tool_name": tool_name,
                    "result": observation,
                }
            )

        # ---------------------------------------------------------
        # 3A. GENERAL REQUEST
        #
        # No company-specific tools are required.
        # ---------------------------------------------------------

        if not required_tools:

            response = self.client.chat.completions.create(
                model=settings.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are the Enterprise Analytics "
                            "Command Center assistant. "
                            "Answer this general question normally. "
                            "Do not invent company-specific facts."
                        ),
                    },
                    {
                        "role": "user",
                        "content": user_question,
                    },
                ],
                temperature=0.1,
                max_tokens=800,
            )

            final_answer = (
                response.choices[0].message.content
                or "No final answer was generated."
            )

            return AgentResponse(
                answer=final_answer.strip(),
                tools_used=[],
                trace=[],
                sources=[],
            )

        # ---------------------------------------------------------
        # 3B. SYNTHESIZE
        #
        # All required enterprise tools have already executed.
        # Gemma performs synthesis only.
        # ---------------------------------------------------------

        synthesis_prompt = f"""
{EACC_SYSTEM_PROMPT}

FINAL SYNTHESIS MODE

The application has already classified the request and executed
all enterprise capabilities required to answer it.

Routing classification:
{routing.classification.value}

Required structured data:
{routing.requires_structured_data}

Required enterprise knowledge:
{routing.requires_knowledge_retrieval}

Routing reason:
{routing.reason}

Rules for this synthesis step:

- Use only the supplied tool observations for company-specific facts.

- Do not invent any numerical result, policy, threshold,
  procedure, eligibility rule, or enterprise fact.

- A value from enterprise documentation must not be presented
  as a current analytical result.

- A value from structured analytics must not be interpreted as
  company policy unless enterprise knowledge explicitly provides
  the corresponding rule.

- Preserve numerical boundary language exactly.
  "Above 15%" is not equivalent to "15% or above".

- If a required tool returned ERROR, TIMEOUT, or
  INSUFFICIENT_EVIDENCE, explicitly state that the required
  information could not be established.

- Cite enterprise-document claims only with source labels that
  actually appear in the enterprise knowledge observation,
  such as [Source 1].

- Do not invent citations.

- Give the conclusion first.

- Keep the answer concise and business-focused.

- Do not expose private chain-of-thought or hidden reasoning.
""".strip()

        observation_text = json.dumps(
            observations,
            ensure_ascii=False,
            default=str,
            indent=2,
        )

        response = self.client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {
                    "role": "system",
                    "content": synthesis_prompt,
                },
                {
                    "role": "user",
                    "content": (
                        "Original user question:\n"
                        f"{user_question}\n\n"
                        "Enterprise tool observations:\n"
                        f"{observation_text}\n\n"
                        "Produce the final grounded answer."
                    ),
                },
            ],
            temperature=0.1,
            max_tokens=800,
        )

        final_answer = (
            response.choices[0].message.content
            or "No final answer was generated."
        )

        return AgentResponse(
            answer=final_answer.strip(),
            tools_used=tools_used,
            trace=traces,
            sources=sources,
        )

    @staticmethod
    def _build_tool_question(
        tool_name: str,
        user_question: str,
    ) -> str:
        """
        Give each enterprise capability a scoped version
        of the original request.
        """

        if tool_name == "genie_analytics":
            return (
                "Using governed structured enterprise data only, "
                "answer the quantitative or analytical portion of "
                "the following request. Do not answer company policy "
                "or documentation questions.\n\n"
                f"Original request: {user_question}"
            )

        if tool_name == "enterprise_knowledge":
            return (
                "Using enterprise documentation only, retrieve the "
                "policy, procedure, threshold, definition, or guidance "
                "needed for the following request. Do not infer current "
                "analytical values from documentation.\n\n"
                f"Original request: {user_question}"
            )

        return user_question

    def _execute_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> tuple[
        dict[str, Any],
        ToolTrace,
        list[KnowledgeSource],
    ]:
        """
        Execute one required enterprise capability.
        """

        question = str(
            arguments.get(
                "question",
                "",
            )
        ).strip()

        # ---------------------------------------------------------
        # Genie Analytics
        # ---------------------------------------------------------

        if tool_name == "genie_analytics":

            result = ask_genie(
                question
            )

            summary = result.answer

            if result.error:
                summary = (
                    f"{result.answer} "
                    f"Error: {result.error}"
                )

            trace = ToolTrace(
                tool_name="genie_analytics",
                purpose=question,
                status=result.status,
                summary=self._shorten(
                    summary
                ),
            )

            return (
                result.model_dump(
                    mode="json"
                ),
                trace,
                [],
            )

        # ---------------------------------------------------------
        # Enterprise Knowledge
        # ---------------------------------------------------------

        if tool_name == "enterprise_knowledge":

            result = search_enterprise_knowledge(
                question
            )

            if result.error:
                summary = (
                    f"Enterprise knowledge search failed. "
                    f"Error: {result.error}"
                )
            else:
                summary = (
                    f"Retrieved "
                    f"{len(result.sources)} "
                    f"enterprise knowledge sources."
                )

            trace = ToolTrace(
                tool_name="enterprise_knowledge",
                purpose=question,
                status=result.status,
                summary=self._shorten(
                    summary
                ),
            )

            return (
                result.model_dump(
                    mode="json"
                ),
                trace,
                result.sources,
            )

        # ---------------------------------------------------------
        # Defensive fallback
        # ---------------------------------------------------------

        error_message = (
            f"Unknown tool requested: {tool_name}"
        )

        trace = ToolTrace(
            tool_name=tool_name,
            purpose=question,
            status=ToolStatus.ERROR,
            summary=error_message,
        )

        return (
            {
                "status": ToolStatus.ERROR.value,
                "error": error_message,
            },
            trace,
            [],
        )

    @staticmethod
    def _merge_sources(
        existing: list[KnowledgeSource],
        incoming: list[KnowledgeSource],
    ) -> None:
        """
        Merge knowledge sources without duplicating chunks.
        """

        existing_keys = {
            (
                source.chunk_id,
                source.document_title,
                source.section_title,
            )
            for source in existing
        }

        for source in incoming:

            key = (
                source.chunk_id,
                source.document_title,
                source.section_title,
            )

            if key not in existing_keys:
                existing.append(
                    source
                )

                existing_keys.add(
                    key
                )

    @staticmethod
    def _shorten(
        text: str | None,
        limit: int = 300,
    ) -> str | None:
        """
        Keep agent-activity summaries compact.
        """

        if not text:
            return None

        clean = " ".join(
            text.split()
        )

        if len(clean) <= limit:
            return clean

        return (
            clean[: limit - 3]
            + "..."
        )


def run_agent(
    question: str,
) -> AgentResponse:
    """
    Public application entry point.
    """

    agent = EACCAgent()

    return agent.run(
        question
    )