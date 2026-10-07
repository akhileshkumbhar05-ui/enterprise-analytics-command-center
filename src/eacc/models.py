from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ToolStatus(str, Enum):
    """
    Standard status values returned by EACC tools.
    """

    SUCCESS = "SUCCESS"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    TIMEOUT = "TIMEOUT"
    ERROR = "ERROR"

class RequestType(str, Enum):
    """
    High-level routing classification for an EACC request.
    """

    ANALYTICS = "ANALYTICS"
    KNOWLEDGE = "KNOWLEDGE"
    HYBRID = "HYBRID"
    GENERAL = "GENERAL"

class RoutingDecision(BaseModel):
    """
    Model-generated decision describing which enterprise
    capabilities are required for a user request.
    """

    classification: RequestType

    requires_structured_data: bool

    requires_knowledge_retrieval: bool

    reason: str

class KnowledgeSource(BaseModel):
    """
    Enterprise document evidence returned by AI Search.
    """

    source_number: int

    document_title: str

    section_title: str | None = None

    chunk_id: str | None = None

    score: float | None = None


class AnalyticsResult(BaseModel):
    """
    Clean result returned by the Genie analytics tool.

    The agent should see this result rather than Genie's internal
    asynchronous query/polling mechanics.
    """

    status: ToolStatus

    question: str

    answer: str

    sql: str | None = None

    data: list[dict[str, Any]] = Field(
        default_factory=list
    )

    conversation_id: str | None = None

    message_id: str | None = None

    error: str | None = None


class KnowledgeResult(BaseModel):
    """
    Grounded result returned by enterprise knowledge search.
    """

    status: ToolStatus

    question: str

    answer: str

    sources: list[KnowledgeSource] = Field(
        default_factory=list
    )

    error: str | None = None


class ToolTrace(BaseModel):
    """
    One high-level tool action performed during an agent run.

    This will later support the Agent Activity panel in the UI.
    """

    tool_name: str

    purpose: str

    status: ToolStatus

    summary: str | None = None


class AgentResponse(BaseModel):
    """
    Final structured response from the EACC agent.
    """

    answer: str

    tools_used: list[str] = Field(
        default_factory=list
    )

    trace: list[ToolTrace] = Field(
        default_factory=list
    )

    sources: list[KnowledgeSource] = Field(
        default_factory=list
    )