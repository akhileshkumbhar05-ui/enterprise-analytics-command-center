from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """
    Runtime configuration for the Enterprise Analytics Command Center.

    Databricks-managed resources should be supplied through environment
    variables when the application is deployed.
    """

    # Foundation model used by the orchestration agent
    model_name: str = os.getenv(
        "EACC_MODEL_NAME",
        "system.ai.gemma-3-12b",
    )

    # Genie Agent
    # Databricks Apps will inject this from the Genie Agent app resource.
    genie_space_id: str | None = os.getenv(
        "EACC_GENIE_SPACE_ID"
    )

    # AI Search
    # Endpoint name is currently stable in this workspace.
    ai_search_endpoint: str = os.getenv(
        "EACC_AI_SEARCH_ENDPOINT",
        "eacc-rag-search",
    )

    # Databricks Apps will eventually inject the index full name.
    ai_search_index: str = os.getenv(
        "EACC_AI_SEARCH_INDEX",
        "workspace.eacc_ecommerce_rag.enterprise_knowledge_index",
    )

    # Retrieval configuration validated during the RAG evaluation
    retrieval_top_k: int = int(
        os.getenv(
            "EACC_RETRIEVAL_TOP_K",
            "3",
        )
    )

    # Genie is asynchronous, so our application will handle polling.
    genie_poll_interval_seconds: float = float(
        os.getenv(
            "EACC_GENIE_POLL_INTERVAL_SECONDS",
            "2.0",
        )
    )

    genie_timeout_seconds: int = int(
        os.getenv(
            "EACC_GENIE_TIMEOUT_SECONDS",
            "90",
        )
    )

    def validate_genie(self) -> None:
        """
        Validate configuration required for Genie analytics.
        """
        if not self.genie_space_id:
            raise RuntimeError(
                "EACC_GENIE_SPACE_ID is not configured."
            )

    def validate_ai_search(self) -> None:
        """
        Validate configuration required for enterprise knowledge search.
        """
        if not self.ai_search_endpoint:
            raise RuntimeError(
                "EACC_AI_SEARCH_ENDPOINT is not configured."
            )

        if not self.ai_search_index:
            raise RuntimeError(
                "EACC_AI_SEARCH_INDEX is not configured."
            )


settings = Settings()