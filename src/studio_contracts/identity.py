from __future__ import annotations

from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SystemRole(StrEnum):
    SUPERADMIN = "SUPERADMIN"
    TENANT_ADMIN = "TENANT_ADMIN"
    USER = "USER"


class DepartmentRole(StrEnum):
    MEMBER = "MEMBER"
    DEPT_ADMIN = "DEPT_ADMIN"


class ExecutionContext(BaseModel):
    model_config = ConfigDict(frozen=True)

    tenant_id: UUID
    user_id: UUID
    department_id: UUID | None = Field(default=None)  # Đảm bảo có default=None
    system_role: SystemRole = SystemRole.USER
    dept_role: DepartmentRole | None = Field(default=None)
    allowed_department_ids: list[UUID] = Field(default_factory=list)
