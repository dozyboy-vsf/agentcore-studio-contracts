"""Studio contracts — Single Source of Truth for schemas."""

from __future__ import annotations

from studio_contracts.eval import (
    GateDecision,
    MetricResult,
    Scorecard,
    ScorecardThreshold,
    TestCase,
)
from studio_contracts.identity import DepartmentRole, ExecutionContext, SystemRole
from studio_contracts.kb import (
    ChunkMetadata,
    Citation,
    DocumentChunk,
    DocumentMetadata,
    DocumentScope,
    DocumentStatus,
    KbSearchQuery,
    KbSearchResultItem,
    KnowledgeBaseMetadata,
)
from studio_contracts.recipe import (
    AgentConfig,
    AgentScope,
    CanvasEdge,
    CanvasGraph,
    CanvasNode,
    NodeType,
    Recipe,
    RecipeStatus,
)
from studio_contracts.tools import (
    ToolCallRequest,
    ToolCallResult,
    ToolDefinition,
)
from studio_contracts.trace import TokenUsage, TraceEvent

SCHEMA_VERSION: str = "1.0.0"

__all__ = [
    "SCHEMA_VERSION",
    # Identity
    "SystemRole",
    "DepartmentRole",
    "ExecutionContext",
    # Tools
    "ToolDefinition",
    "ToolCallRequest",
    "ToolCallResult",
    # Recipe
    "AgentScope",
    "RecipeStatus",
    "NodeType",
    "CanvasNode",
    "CanvasEdge",
    "CanvasGraph",
    "AgentConfig",
    "Recipe",
    # KB
    "DocumentScope",
    "DocumentStatus",
    "KnowledgeBaseMetadata",
    "DocumentMetadata",
    "ChunkMetadata",
    "DocumentChunk",
    "KbSearchQuery",
    "Citation",
    "KbSearchResultItem",
    # Eval
    "GateDecision",
    "TestCase",
    "MetricResult",
    "ScorecardThreshold",
    "Scorecard",
    # Trace
    "TokenUsage",
    "TraceEvent",
]
