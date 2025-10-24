from pydantic import BaseModel
from typing import Literal, Optional

class DocumentPage(BaseModel):
    page_number: int
    raw_text: str
    document_type: Literal["claim_form", "discharge", "invoice", "receipt", "payment_proof", "id_card"]
    document_id: Optional[str] = None  # 用于标识同一类型的不同文档
    confidence: float = 1.0