from pydantic import BaseModel, Field
from typing import Any, Optional


class ResearchRequest(BaseModel):
    user_query: str = Field(..., min_length=1, max_length=1000)
    session_id: str


class AgentResult(BaseModel):
    agent_name: str
    status: str
    data: dict[str, Any] = {}
    error: Optional[str] = None


class StatusUpdate(BaseModel):
    agent: str
    status: str
    detail: Optional[str] = None


class FinalReport(BaseModel):
    session_id: str
    summary: str
    details: dict[str, Any] = {}
    agent_statuses: list[AgentResult] = []
