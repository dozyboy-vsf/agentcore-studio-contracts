"""Agent Recipe, Canvas Graph, and Tool Binding contracts."""

from __future__ import annotations

from enum import Enum
from typing import Any
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from studio_contracts.tools import ToolDefinition


class AgentScope(str, Enum):
    """Phạm vi hoạt động của Agent."""
    DEPARTMENT = "DEPARTMENT"
    COMPANY = "COMPANY"


class RecipeStatus(str, Enum):
    """Vòng đời phát triển và phê duyệt Agent."""
    DRAFT = "DRAFT"
    EVALUATED = "EVALUATED"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    PUBLISHED_DEPT = "PUBLISHED_DEPT"
    PUBLISHED_COMPANY = "PUBLISHED_COMPANY"
    ARCHIVED = "ARCHIVED"


class NodeType(str, Enum):
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
    """Cấu hình trí tuệ, công cụ và kho dữ liệu cho Agent."""
    model_config = ConfigDict(frozen=True)

    instructions: str = Field(..., description="System prompt định hướng agent")
    model: str = Field("gpt-4o-mini", description="Mô hình LLM sử dụng")
    temperature: float = 0.2
    max_tokens: int = 2048
    max_tool_iterations: int = Field(
        5, description="Giới hạn số lượt gọi tool để chống loop vô hạn"
    )
    # Danh sách Tool vệ tinh (Calculator, Current Time, Webhooks, v.v.)
    tools: list[ToolDefinition] = Field(default_factory=list)
    # HỖ TRỢ MULTI-KB: Danh sách các kho tri thức gán cho Agent tra cứu
    bound_kb_ids: list[UUID] = Field(
        default_factory=list,
        description="Các kho tri thức Agent được phép tìm kiếm (rỗng = không dùng KB)",
    )


class Recipe(BaseModel):
    """Bản hợp đồng hoàn chỉnh định nghĩa một Agent trong AgentCore Studio."""
    model_config = ConfigDict(frozen=True)

    agent_id: str
    tenant_id: UUID
    department_id: UUID | None = None
    name: str
    version: int = 1
    scope: AgentScope = AgentScope.DEPARTMENT
    status: RecipeStatus = RecipeStatus.DRAFT
    recipe_hash: str = Field(..., description="Mã SHA-256 xác thực cấu hình")
    agent_config: AgentConfig
    graph: CanvasGraph
    golden_set_ref: str | None = None
    tool_description: str | None = Field(
        None,
        description="Mô tả công năng để Router Agent biết khi nào cần điều phối câu hỏi tới con bot này",
    )


# Bắt buộc rebuild để Pydantic nạp đầy đủ schema
AgentConfig.model_rebuild()
Recipe.model_rebuild()