from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TokenUsage(BaseModel):
    model_config = ConfigDict(frozen=True)

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class TraceEvent(BaseModel):
    """Bản ghi sự kiện từng bước chạy của Agent phục vụ phân tích chi phí."""

    model_config = ConfigDict(frozen=True)

    event_id: str
    run_id: str
    agent_id: str
    tenant_id: UUID
    step_name: str
    inputs: dict[str, Any] = Field(default_factory=dict)
    outputs: dict[str, Any] = Field(default_factory=dict)
    tokens: TokenUsage
    cost: float = 0.0
    citations: list[str] = Field(default_factory=list)
    timestamp: str
