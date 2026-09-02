"""Agent Recipe, Canvas Graph, and Tool Binding contracts."""

from __future__ import annotations

from enum import StrEnum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from studio_contracts.tools import ToolDefinition


class AgentScope(StrEnum):
    """Phạm vi hoạt động của Agent."""

    DEPARTMENT = "DEPARTMENT"
    COMPANY = "COMPANY"


class RecipeStatus(StrEnum):
    """Vòng đời phát triển và phê duyệt Agent."""

    DRAFT = "DRAFT"
    EVALUATED = "EVALUATED"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    PUBLISHED_DEPT = "PUBLISHED_DEPT"
    PUBLISHED_COMPANY = "PUBLISHED_COMPANY"
    ARCHIVED = "ARCHIVED"


class NodeType(StrEnum):
    """Các loại khối kéo thả trên Canvas."""

    LLM_STEP = "llm_step"
    TOOL_NODE = "tool_node"
    GUARDRAIL = "guardrail"
    ROUTER = "router"
    OUTPUT = "output"


class CanvasNode(BaseModel):
    """Một node trong đồ thị Canvas."""

    model_config = ConfigDict(frozen=True)

    id: str
    type: NodeType
    label: str
    params: dict[str, Any] = Field(default_factory=dict)


class CanvasEdge(BaseModel):
    """Cạnh nối giữa 2 node trên Canvas (tương thích serialize 'from' alias)."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    from_: str = Field(..., alias="from")
    to: str
    condition: str | None = None


class CanvasGraph(BaseModel):
    """Toàn bộ đồ thị Canvas (có thể chỉ chứa 1 node LLM_STEP hoặc luồng phức tạp)."""

    model_config = ConfigDict(frozen=True)

    nodes: list[CanvasNode]
    edges: list[CanvasEdge] = Field(default_factory=list)


class AgentConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    instructions: str
    model: str = "gpt-4o-mini"
    temperature: float = 0.2
    max_tokens: int = 2048
    max_tool_iterations: int = Field(default=5)  # Đảm bảo có default=5
    tools: list[ToolDefinition] = Field(default_factory=list)
    bound_kb_ids: list[UUID] = Field(default_factory=list)


class Recipe(BaseModel):
    model_config = ConfigDict(frozen=True)

    agent_id: str
    tenant_id: UUID
    department_id: UUID | None = Field(default=None)
    name: str
    version: int = 1
    scope: AgentScope = AgentScope.DEPARTMENT
    status: RecipeStatus = RecipeStatus.DRAFT
    recipe_hash: str
    agent_config: AgentConfig
    graph: CanvasGraph
    golden_set_ref: str | None = Field(default=None)
    tool_description: str | None = Field(default=None)  # Đảm bảo có default=None


# Bắt buộc rebuild để Pydantic nạp đầy đủ schema
AgentConfig.model_rebuild()
Recipe.model_rebuild()
