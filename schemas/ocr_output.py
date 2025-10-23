from pydantic import BaseModel
from typing import Optional, List

class ClaimFormOCR(BaseModel):
    policy_number: Optional[str] = None
    patient_name: Optional[str] = None
    claim_amount: Optional[float] = None
    date_of_service: Optional[str] = None
    diagnosis_codes: List[str] = []
    provider_name: Optional[str] = None
    provider_npi: Optional[str] = None
    claim_submission_date: Optional[str] = None

class DischargeOCR(BaseModel):
    patient_name: Optional[str] = None
    diagnosis_codes: List[str] = []
    procedure_codes: List[str] = []
    admission_date: Optional[str] = None
    discharge_date: Optional[str] = None
    attending_physician: Optional[str] = None
    hospital_name: Optional[str] = None
    discharge_condition: Optional[str] = None

class InvoiceOCR(BaseModel):
    total_amount: Optional[float] = None
    hospital_name: Optional[str] = None
    service_date: Optional[str] = None
    itemized_services: List[dict] = []
    patient_account_number: Optional[str] = None

class ReceiptOCR(BaseModel):
    payment_amount: Optional[float] = None
    payment_date: Optional[str] = None
    payment_method: Optional[str] = None
    merchant_name: Optional[str] = None
    transaction_reference: Optional[str] = None
    patient_name: Optional[str] = None

class PaymentProofOCR(BaseModel):
    payer_name: Optional[str] = None
    payee_name: Optional[str] = None
    payment_amount: Optional[float] = None
    payment_date: Optional[str] = None
    bank_name: Optional[str] = None
    account_number_last4: Optional[str] = None
    transaction_id: Optional[str] = None
    payment_purpose: Optional[str] = None

class IDCardOCR(BaseModel):
    patient_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    id_number: Optional[str] = None
    expiration_date: Optional[str] = None
    issuing_authority: Optional[str] = None
    address: Optional[str] = None

class OCRMetadata(BaseModel):
    policy_number: Optional[str] = None
    claim_id: Optional[str] = None
    ocr_version: Optional[str] = None
    document_versions: dict = {}

class OCROutput(BaseModel):
    claim_form: Optional[ClaimFormOCR] = None
    discharge: Optional[List[DischargeOCR]] = None
    invoice: Optional[List[InvoiceOCR]] = None
    receipt: Optional[List[ReceiptOCR]] = None
    payment_proof: Optional[List[PaymentProofOCR]] = None
    id_card: Optional[List[IDCardOCR]] = None
    metadata: OCRMetadata