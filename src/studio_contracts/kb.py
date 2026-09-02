"""Knowledge Base, Documents, Chunks, and Multi-KB Retrieval contracts."""

from __future__ import annotations

from enum import Enum
from typing import Any
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class DocumentScope(str, Enum):
    """Phạm vi truy cập tri thức."""
    COMPANY_WIDE = "COMPANY_WIDE"
    DEPARTMENT_RESTRICTED = "DEPARTMENT_RESTRICTED"
    CUSTOM_ACL = "CUSTOM_ACL"


class DocumentStatus(str, Enum):
    """Vòng đời xử lý file tài liệu trong quá trình Ingestion."""
    PENDING = "PENDING"
    PARSING = "PARSING"
    CHUNKING = "CHUNKING"
    INDEXED = "INDEXED"
    FAILED = "FAILED"


class KnowledgeBaseMetadata(BaseModel):
    """Thực thể đại diện cho một Kho tri thức (1 Tenant có nhiều KB, 1 Dept có nhiều KB)."""
    model_config = ConfigDict(frozen=True)

    kb_id: UUID = Field(..., description="Mã định danh duy nhất của Kho tri thức")
    tenant_id: UUID = Field(..., description="Thuộc công ty/tenant nào")
    department_id: UUID | None = Field(
        None,
        description="Phòng ban sở hữu (nếu là None -> KB cấp Toàn công ty / Company-Wide)",
    )
    name: str = Field(..., description="Tên KB (ví dụ: 'Nội quy công ty', 'API Docs')")
    description: str | None = None
    scope: DocumentScope = DocumentScope.DEPARTMENT_RESTRICTED
    shared_department_ids: list[UUID] = Field(
        default_factory=list,
        description="Danh sách các phòng ban khác được phép tra cứu chéo KB này",
    )
    document_count: int = 0
    chunk_count: int = 0


class DocumentMetadata(BaseModel):
    """Thông tin tệp tài liệu gốc được upload vào KB."""
    model_config = ConfigDict(frozen=True)

    doc_id: UUID
    tenant_id: UUID
    kb_id: UUID
    filename: str
    storage_uri: str
    file_hash_sha256: str
    mime_type: str | None = None
    file_size_bytes: int = 0
    status: DocumentStatus = DocumentStatus.PENDING
    error_message: str | None = None
    chunk_count: int = 0
    uploaded_by: UUID | None = None


class ChunkMetadata(BaseModel):
    """Siêu dữ liệu gắn kèm từng Chunk văn bản phục vụ Pre-filtering bảo mật."""
    model_config = ConfigDict(frozen=True)

    tenant_id: UUID
    kb_id: UUID
    doc_id: UUID
    chunk_index: int
    scope: DocumentScope
    allowed_dept_ids: list[UUID] = Field(
        default_factory=list,
        description="Các phòng ban có quyền xem đoạn text này",
    )
    allowed_user_ids: list[UUID] = Field(default_factory=list)
    source_filename: str
    extra: dict[str, Any] = Field(default_factory=dict)


class DocumentChunk(BaseModel):
    """Đoạn văn bản sau khi bẻ nhỏ (Chunk) kèm vector embedding."""
    model_config = ConfigDict(frozen=True)

    id: str
    content: str
    token_count: int
    metadata: ChunkMetadata
    embedding: list[float] | None = None
    external_vector_id: str | None = None


class KbSearchQuery(BaseModel):
    """Truy vấn tìm kiếm Vector có tiêm bộ lọc an toàn và quét qua Multi-KB."""
    model_config = ConfigDict(frozen=True)

    query_text: str
    top_k: int = 5
    tenant_id: UUID
    target_kb_ids: list[UUID] = Field(
        default_factory=list,
        description="Chỉ định quét trong các KB này. Nếu rỗng, quét tất cả KB user có quyền",
    )
    allowed_dept_ids: list[UUID] = Field(
        default_factory=list,
        description="Danh sách phòng ban người dùng hiện tại có quyền truy cập",
    )
    include_company_wide: bool = True


class Citation(BaseModel):
    """Trích dẫn chứng minh nguồn gốc câu trả lời."""
    model_config = ConfigDict(frozen=True)

    doc_id: UUID
    kb_id: UUID
    filename: str
    chunk_index: int
    preview: str


class KbSearchResultItem(BaseModel):
    """Kết quả trả về cho mỗi đoạn văn bản tương đồng."""
    model_config = ConfigDict(frozen=True)

    chunk_id: str
    content: str
    similarity_score: float
    citation: Citation


# Bắt buộc rebuild để Pydantic giải quyết forward reference
KnowledgeBaseMetadata.model_rebuild()
DocumentMetadata.model_rebuild()
DocumentChunk.model_rebuild()
KbSearchResultItem.model_rebuild()