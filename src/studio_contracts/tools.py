from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ToolDefinition(BaseModel):
    """Khuôn mẫu mô tả một công cụ (Mở rộng tùy ý, không cần sửa schema)."""

    model_config = ConfigDict(frozen=True)

    # Dùng str thay cho Enum: "calculator", "kb_search", "send_slack", v.v.
    name: str = Field(..., description="Tên định danh duy nhất của tool")
    description: str = Field(..., description="Mô tả công năng để LLM biết khi nào cần gọi")
    parameters_schema: dict[str, Any] = Field(
        default_factory=lambda: {"type": "object", "properties": {}},
        description="JSON Schema chuẩn của tham số đầu vào (tương thích OpenAI/Claude Function Calling)",
    )
    config: dict[str, Any] = Field(
        default_factory=dict, description="Cấu hình nội bộ nếu có (ví dụ: kb_id, timeout, api_endpoint)"
    )


class ToolCallRequest(BaseModel):
    """Yêu cầu gọi tool do LLM phát ra."""

    model_config = ConfigDict(frozen=True)

    call_id: str
    tool_name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class ToolCallResult(BaseModel):
    """Kết quả trả về cho LLM sau khi Engine chạy tool xong."""

    model_config = ConfigDict(frozen=True)

    call_id: str
    tool_name: str
    output: Any
    is_error: bool = False
    error_message: str | None = None
