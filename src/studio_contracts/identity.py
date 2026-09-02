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
    """Context bất biến (frozen) định danh người gọi request."""

    model_config = ConfigDict(frozen=True)

    tenant_id: UUID = Field(..., description="Mã công ty/tenant bắt buộc")
    user_id: UUID = Field(..., description="Mã người dùng đang gửi câu hỏi")
    department_id: UUID | None = Field(None, description="Mã phòng ban chính của user")
    system_role: SystemRole = Field(SystemRole.USER, description="Quyền hệ thống cấp tổ chức")
    dept_role: DepartmentRole | None = Field(None, description="Quyền nội bộ tại phòng ban")
    allowed_department_ids: list[UUID] = Field(
        default_factory=list,
        description="Danh sách các phòng ban user được phép truy cập tài liệu",
    )
