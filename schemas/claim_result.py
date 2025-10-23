from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from schemas.ocr_output import OCROutput
from schemas.ner_output import NEROutput
from schemas.rule_output import RuleCheckOutput

class ClaimResult(BaseModel):
    """
    最终索赔处理结果模型
    """
    claim_id: Optional[str] = None
    policy_number: Optional[str] = None
    ocr: OCROutput
    ner: NEROutput
    rule_check: RuleCheckOutput
    overall_status: Optional[str] = None  # "APPROVED", "REJECTED", "PENDING_REVIEW"
    processing_timestamp: datetime
    pipeline_version: Optional[str] = None