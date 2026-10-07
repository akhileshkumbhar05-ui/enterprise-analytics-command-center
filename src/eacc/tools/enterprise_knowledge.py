from __future__ import annotations

from databricks.sdk import WorkspaceClient

from eacc.config import settings
from eacc.models import (
    KnowledgeResult,
    KnowledgeSource,
    ToolStatus,
)


KNOWLEDGE_COLUMNS = [
    "chunk_id",
    "document_title",
    "section_title",
    "source_text",
]


class EnterpriseKnowledgeTool:
    """
    Semantic enterprise knowledge retrieval over the EACC AI Search index.

    This tool retrieves governed policy/document evidence.
    It does not independently invent or infer company policy.
    """

    def __init__(
        self,
        workspace_client: WorkspaceClient | None = None,
    ) -> None:
        settings.validate_ai_search()

        self.client = workspace_client or WorkspaceClient()

        self.index_name = settings.ai_search_index

    def search(
        self,
        question: str,
        top_k: int | None = None,
    ) -> KnowledgeResult:
        """
        Retrieve enterprise knowledge relevant to a question.
        """

        if not question or not question.strip():
            return KnowledgeResult(
                status=ToolStatus.ERROR,
                question=question,
                answer="No enterprise knowledge question was provided.",
                error="Question must not be empty.",
            )

        num_results = (
            top_k
            if top_k is not None
            else settings.retrieval_top_k
        )

        try:
            response = (
                self.client.vector_search_indexes.query_index(
                    index_name=self.index_name,
                    columns=KNOWLEDGE_COLUMNS,
                    query_text=question.strip(),
                    query_type="ANN",
                    num_results=num_results,
                )
            )

        except Exception as exc:
            return KnowledgeResult(
                status=ToolStatus.ERROR,
                question=question,
                answer="Enterprise knowledge search failed.",
                error=str(exc),
            )

        return self._build_result(
            question=question,
            response=response,
        )

    def _build_result(
        self,
        question: str,
        response,
    ) -> KnowledgeResult:
        """
        Convert an AI Search response into a clean KnowledgeResult.
        """

        if not response.result:
            return self._insufficient_result(question)

        rows = response.result.data_array or []

        if not rows:
            return self._insufficient_result(question)

        sources: list[KnowledgeSource] = []
        evidence_blocks: list[str] = []

        expected_column_count = len(KNOWLEDGE_COLUMNS)

        for source_number, row in enumerate(
            rows,
            start=1,
        ):
            values = row[:expected_column_count]

            record = dict(
                zip(
                    KNOWLEDGE_COLUMNS,
                    values,
                )
            )

            score = None

            # AI Search appends the relevance score after
            # the requested result columns.
            if len(row) > expected_column_count:
                try:
                    score = float(
                        row[expected_column_count]
                    )
                except (TypeError, ValueError):
                    score = None

            source = KnowledgeSource(
                source_number=source_number,
                document_title=(
                    record.get("document_title")
                    or "Unknown document"
                ),
                section_title=record.get(
                    "section_title"
                ),
                chunk_id=record.get(
                    "chunk_id"
                ),
                score=score,
            )

            sources.append(source)

            evidence_blocks.append(
                self._format_evidence(
                    source_number=source_number,
                    document_title=record.get(
                        "document_title"
                    ),
                    section_title=record.get(
                        "section_title"
                    ),
                    source_text=record.get(
                        "source_text"
                    ),
                )
            )

        return KnowledgeResult(
            status=ToolStatus.SUCCESS,
            question=question,
            answer="\n\n".join(evidence_blocks),
            sources=sources,
        )

    @staticmethod
    def _format_evidence(
        source_number: int,
        document_title: str | None,
        section_title: str | None,
        source_text: str | None,
    ) -> str:
        """
        Produce deterministic evidence text for the orchestration agent.
        """

        return (
            f"[Source {source_number}]\n"
            f"Document: "
            f"{document_title or 'Unknown document'}\n"
            f"Section: "
            f"{section_title or 'Unknown section'}\n\n"
            f"{source_text or ''}"
        )

    @staticmethod
    def _insufficient_result(
        question: str,
    ) -> KnowledgeResult:
        return KnowledgeResult(
            status=ToolStatus.INSUFFICIENT_EVIDENCE,
            question=question,
            answer=(
                "No relevant enterprise knowledge "
                "was retrieved."
            ),
            sources=[],
        )


def search_enterprise_knowledge(
    question: str,
    top_k: int | None = None,
) -> KnowledgeResult:
    """
    Convenience function used by the EACC agent.
    """

    tool = EnterpriseKnowledgeTool()

    return tool.search(
        question=question,
        top_k=top_k,
    )