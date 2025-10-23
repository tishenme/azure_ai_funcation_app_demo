from pydantic import BaseModel
from typing import List, Optional

class RuleCheckOutput(BaseModel):
    """
    规则检查结果模型
    """
    policy_valid: Optional[bool] = None
    coverage_active: Optional[bool] = None
    diagnosis_covered: Optional[bool] = None
    amount_within_limit: Optional[bool] = None
    missing_documents: List[str] = []
    final_decision: Optional[str] = None  # "APPROVED", "REJECTED", "PENDING_REVIEW"
    rejection_reasons: List[str] = []
    rule_engine_version: Optional[str] = None