from pydantic import BaseModel
from typing import List, Optional

class NEROutput(BaseModel):
    """
    NER处理结果模型
    """
    policy_number: Optional[str] = None
    patient_name: Optional[str] = None
    diagnosis_codes: List[str] = []
    procedure_codes: List[str] = []
    total_claimed_amount: Optional[float] = None
    provider_signature_verified: Optional[bool] = None
    hospital_name: Optional[str] = None
    service_dates: List[str] = []
    ner_version: Optional[str] = None