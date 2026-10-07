from __future__ import annotations

import json

from openai import OpenAI

from eacc.config import settings
from eacc.models import (
    RequestType,
    RoutingDecision,
)


ROUTER_TOOL = {
    "type": "function",
    "function": {
        "name": "route_request",
        "description": (
            "Classify an EACC user request and determine which "
            "enterprise capabilities are required."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "classification": {
                    "type": "string",
                    "enum": [
                        "ANALYTICS",
                        "KNOWLEDGE",
                        "HYBRID",
                        "GENERAL",
                    ],
                },
                "requires_structured_data": {
                    "type": "boolean",
                },
                "requires_knowledge_retrieval": {
                    "type": "boolean",
                },
                "reason": {
                    "type": "string",
                },
            },
            "required": [
                "classification",
                "requires_structured_data",
                "requires_knowledge_retrieval",
                "reason",
            ],
            "additionalProperties": False,
        },
    },
}


ROUTER_SYSTEM_PROMPT = """
You are the routing layer for the Enterprise Analytics Command Center.

Classify each user request into exactly one category:

ANALYTICS
- Requires governed structured enterprise data.
- Examples include counts, percentages, financial metrics,
  trends, comparisons, distributions, or current observed values.

KNOWLEDGE
- Requires enterprise documentation.
- Examples include policies, procedures, thresholds,
  eligibility rules, metric definitions, or documented guidance.

HYBRID
- Requires both structured enterprise data and enterprise
  documentation to answer completely.

GENERAL
- Can be answered without company-specific structured data
  or enterprise documentation.

Rules:

- A question asking for a current company metric plus what company
  policy says about that metric is HYBRID.

- Do not classify a policy threshold as ANALYTICS merely because
  the threshold contains a number.

- Do not classify a current enterprise metric as KNOWLEDGE merely
  because documents may mention examples of that metric.

- The boolean requirements must agree with the classification:

  ANALYTICS:
  requires_structured_data = true
  requires_knowledge_retrieval = false

  KNOWLEDGE:
  requires_structured_data = false
  requires_knowledge_retrieval = true

  HYBRID:
  requires_structured_data = true
  requires_knowledge_retrieval = true

  GENERAL:
  requires_structured_data = false
  requires_knowledge_retrieval = false
""".strip()


class RequestRouter:
    """
    Structured routing layer for EACC requests.
    """

    def __init__(
        self,
        client: OpenAI,
    ) -> None:
        self.client = client

    def classify(
        self,
        question: str,
    ) -> RoutingDecision:
        """
        Classify one user request using a forced structured function call.
        """

        if not question or not question.strip():
            return RoutingDecision(
                classification=RequestType.GENERAL,
                requires_structured_data=False,
                requires_knowledge_retrieval=False,
                reason="The request is empty.",
            )

        response = self.client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {
                    "role": "system",
                    "content": ROUTER_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": question.strip(),
                },
            ],
            tools=[ROUTER_TOOL],
            tool_choice={
                "type": "function",
                "function": {
                    "name": "route_request",
                },
            },
            temperature=0.0,
            max_tokens=250,
        )

        message = response.choices[0].message

        if not message.tool_calls:
            raise RuntimeError(
                "The routing model did not return a routing decision."
            )

        tool_call = message.tool_calls[0]

        if tool_call.function.name != "route_request":
            raise RuntimeError(
                "The routing model returned an unexpected tool call."
            )

        arguments = json.loads(
            tool_call.function.arguments
        )

        decision = RoutingDecision(
            **arguments
        )

        self._validate_consistency(
            decision
        )

        return decision

    @staticmethod
    def _validate_consistency(
        decision: RoutingDecision,
    ) -> None:
        """
        Ensure classification and required capabilities agree.
        """

        expected = {
            RequestType.ANALYTICS: (
                True,
                False,
            ),
            RequestType.KNOWLEDGE: (
                False,
                True,
            ),
            RequestType.HYBRID: (
                True,
                True,
            ),
            RequestType.GENERAL: (
                False,
                False,
            ),
        }

        expected_structured, expected_knowledge = (
            expected[decision.classification]
        )

        if (
            decision.requires_structured_data
            != expected_structured
            or decision.requires_knowledge_retrieval
            != expected_knowledge
        ):
            raise RuntimeError(
                "Routing decision is internally inconsistent."
            )