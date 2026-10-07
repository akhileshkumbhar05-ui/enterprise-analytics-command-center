from __future__ import annotations

from datetime import timedelta
from typing import Any

from databricks.sdk import WorkspaceClient

from eacc.config import settings
from eacc.models import AnalyticsResult, ToolStatus


class GenieAnalyticsTool:
    """
    Production wrapper around the EACC Analytics Genie Agent.

    The caller gives this class a natural-language analytics question.
    This wrapper handles Genie execution, waiting, SQL extraction,
    query-result retrieval, and conversion into an AnalyticsResult.
    """

    def __init__(
        self,
        workspace_client: WorkspaceClient | None = None,
    ) -> None:
        settings.validate_genie()

        self.client = workspace_client or WorkspaceClient()
        self.space_id = settings.genie_space_id

    def ask(
        self,
        question: str,
    ) -> AnalyticsResult:
        """
        Ask the Genie Agent one structured analytics question.

        Returns a clean AnalyticsResult so the orchestration agent
        does not need to understand Genie polling mechanics.
        """

        if not question or not question.strip():
            return AnalyticsResult(
                status=ToolStatus.ERROR,
                question=question,
                answer="No analytics question was provided.",
                error="Question must not be empty.",
            )

        try:
            message = self.client.genie.start_conversation_and_wait(
                space_id=self.space_id,
                content=question.strip(),
                timeout=timedelta(
                    seconds=settings.genie_timeout_seconds
                ),
            )

        except TimeoutError as exc:
            return AnalyticsResult(
                status=ToolStatus.TIMEOUT,
                question=question,
                answer=(
                    "The analytics request did not complete "
                    "within the configured timeout."
                ),
                error=str(exc),
            )

        except Exception as exc:
            return AnalyticsResult(
                status=ToolStatus.ERROR,
                question=question,
                answer="The analytics request failed.",
                error=str(exc),
            )

        return self._build_result(
            question=question,
            message=message,
        )

    def _build_result(
        self,
        question: str,
        message: Any,
    ) -> AnalyticsResult:
        """
        Convert the completed Genie response into our internal model.
        """

        answer_text = ""
        generated_sql = None
        rows: list[dict[str, Any]] = []

        attachments = message.attachments or []

        for attachment in attachments:
            # Genie may return one or more text attachments.
            if attachment.text and attachment.text.content:
                answer_text = attachment.text.content

            # Capture the generated SQL and its result.
            if attachment.query:
                generated_sql = attachment.query.query

                if attachment.attachment_id:
                    rows = self._get_query_rows(
                        conversation_id=message.conversation_id,
                        message_id=message.message_id,
                        attachment_id=attachment.attachment_id,
                    )

        if not answer_text:
            if rows:
                answer_text = (
                    "Genie completed the analytics query successfully."
                )
            else:
                answer_text = (
                    "Genie completed the request but returned "
                    "no analytical result."
                )

        return AnalyticsResult(
            status=ToolStatus.SUCCESS,
            question=question,
            answer=answer_text,
            sql=generated_sql,
            data=rows,
            conversation_id=message.conversation_id,
            message_id=message.message_id,
        )

    def _get_query_rows(
        self,
        conversation_id: str,
        message_id: str,
        attachment_id: str,
    ) -> list[dict[str, Any]]:
        """
        Fetch the SQL result for a Genie query attachment and convert
        rows into dictionaries keyed by column name.
        """

        response = (
            self.client.genie
            .get_message_attachment_query_result(
                space_id=self.space_id,
                conversation_id=conversation_id,
                message_id=message_id,
                attachment_id=attachment_id,
            )
        )

        statement = response.statement_response

        if not statement:
            return []

        if not statement.manifest:
            return []

        if not statement.manifest.schema:
            return []

        if not statement.manifest.schema.columns:
            return []

        if not statement.result:
            return []

        if not statement.result.data_array:
            return []

        column_names = [
            column.name
            for column in statement.manifest.schema.columns
        ]

        return [
            dict(zip(column_names, row))
            for row in statement.result.data_array
        ]


def ask_genie(
    question: str,
) -> AnalyticsResult:
    """
    Convenience function used by the future EACC agent tool layer.
    """

    tool = GenieAnalyticsTool()

    return tool.ask(question)