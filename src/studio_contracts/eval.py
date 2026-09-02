from __future__ import annotations

from enum import Enum
from typing import Any
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class GateDecision(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"


class TestCase(BaseModel):
    model_config = ConfigDict(frozen=True)

    case_id: str
    question: str
    expected_answer: str | None = None
    required_citations: list[str] = Field(default_factory=list)


class MetricResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str  # e.g., 'faithfulness', 'answer_relevancy', 'latency_ms'
    score: float
    threshold: float
    passed: bool


class ScorecardThreshold(BaseModel):
    model_config = ConfigDict(frozen=True)

    min_overall_score: float = 0.8
    min_faithfulness: float = 0.9


class Scorecard(BaseModel):
    """Kết quả kiểm định bắt buộc trước khi Publish Agent."""
    model_config = ConfigDict(frozen=True)

    scorecard_id: UUID
    agent_id: str
    recipe_version: int
    recipe_hash: str
    decision: GateDecision
    overall_score: float = Field(..., ge=0.0, le=1.0)
    metrics: list[MetricResult] = Field(default_factory=list)
    raw_details: list[dict[str, Any]] = Field(default_factory=list)