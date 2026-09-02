from __future__ import annotations

import uuid

import pytest
from pydantic import ValidationError
from studio_contracts import (
    AgentConfig,
    AgentScope,
    CanvasGraph,
    CanvasNode,
    DepartmentRole,
    ExecutionContext,
    KbSearchQuery,
    NodeType,
    Recipe,
    RecipeStatus,
    SystemRole,
    ToolDefinition,
)


def test_execution_context_immutability() -> None:
    """Đảm bảo Context danh tính là bất biến."""
    t_id = uuid.uuid4()
    u_id = uuid.uuid4()
    ctx = ExecutionContext(
        tenant_id=t_id,
        user_id=u_id,
        department_id=None,
        system_role=SystemRole.TENANT_ADMIN,
        dept_role=DepartmentRole.DEPT_ADMIN,
        allowed_department_ids=[],
    )
    assert ctx.tenant_id == t_id
    with pytest.raises(ValidationError):
        ctx.system_role = SystemRole.USER  # type: ignore[misc]


def test_agent_recipe_with_tool_satellites() -> None:
    """Kiểm tra Agent có duy nhất 1 node llm_step và danh sách vệ tinh tool động."""
    calc_tool = ToolDefinition(
        name="calculator",
        description="Tính toán số học chính xác",
        parameters_schema={
            "type": "object",
            "properties": {"expression": {"type": "string"}},
            "required": ["expression"],
        },
    )
    kb_tool = ToolDefinition(
        name="kb_search",
        description="Tra cứu chính sách nội bộ",
        config={"kb_id": str(uuid.uuid4())},
    )

    recipe = Recipe(
        agent_id="agent-copilot-01",
        tenant_id=uuid.uuid4(),
        department_id=None,
        name="Enterprise Assistant",
        recipe_hash="sha256_hash_mock",
        scope=AgentScope.COMPANY,
        status=RecipeStatus.DRAFT,
        tool_description=None,
        agent_config=AgentConfig(
            instructions="Bạn là trợ lý giải toán và hỗ trợ nghiệp vụ công ty.",
            model="gpt-4o-mini",
            temperature=0.2,
            max_tokens=2048,
            max_tool_iterations=5,
            tools=[calc_tool, kb_tool],
            bound_kb_ids=[uuid.uuid4()],
        ),
        graph=CanvasGraph(
            nodes=[
                CanvasNode(
                    id="llm-brain",
                    type=NodeType.LLM_STEP,
                    label="Lõi suy luận",
                )
            ],
            edges=[],
        ),
    )

    assert len(recipe.agent_config.tools) == 2
    assert len(recipe.graph.nodes) == 1
    assert recipe.graph.nodes[0].type == NodeType.LLM_STEP
    assert recipe.scope == AgentScope.COMPANY
    assert len(recipe.agent_config.bound_kb_ids) == 1


def test_kb_search_query_scoping() -> None:
    """Đảm bảo query tìm kiếm vector gắn chặt với tenant và quyền phòng ban."""
    t_id = uuid.uuid4()
    d_id = uuid.uuid4()
    target_kb = uuid.uuid4()
    query = KbSearchQuery(
        query_text="Chính sách nghỉ thai sản",
        tenant_id=t_id,
        target_kb_ids=[target_kb],
        allowed_dept_ids=[d_id],
        include_company_wide=True,
    )
    assert query.tenant_id == t_id
    assert query.include_company_wide is True
    assert d_id in query.allowed_dept_ids
    assert target_kb in query.target_kb_ids
