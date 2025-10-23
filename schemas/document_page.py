from pydantic import BaseModel
from typing import Literal

class DocumentPage(BaseModel):
    page_number: int
    raw_text: str
    document_type: Literal["claim_form", "discharge", "invoice", "receipt", "payment_proof", "id_card"]
    confidence: float = 1.0