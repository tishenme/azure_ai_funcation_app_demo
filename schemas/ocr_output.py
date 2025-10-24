"""
OCR输出数据模型
定义从文档中提取的结构化数据
"""
from pydantic import BaseModel
from typing import List, Optional, Union
from datetime import date
from enum import Enum

class DocumentMetadata(BaseModel):
    """
    文档元数据
    """
    claim_id: Optional[str] = None
    policy_number: Optional[str] = None
    ocr_version: str
    document_versions: dict
    processing_timestamp: str

class SignatureType(str, Enum):
    """
    签名类型枚举
    """
    PATIENT = "patient"           # 患者签名
    PROVIDER = "provider"         # 医疗提供者签名
    INSURED = "insured"           # 被保险人签名
    AUTHORIZED = "authorized"     # 授权代表签名
    WITNESS = "witness"           # 见证人签名
    UNKNOWN = "unknown"           # 未知类型签名

class SignatureInfo(BaseModel):
    """
    签名信息模型
    """
    url: str                      # 签名图像URL
    signature_type: SignatureType # 签名类型
    confidence: Optional[float]   # 签名检测置信度

class ClaimFormOCR(BaseModel):
    """
    理赔表OCR提取结果（只有一份）
    """
    policy_number: str
    patient_name: str
    claim_amount: float
    claim_date: date
    diagnosis_codes: List[str]
    signatures: List[SignatureInfo] = []  # 签名信息列表

class DischargeOCR(BaseModel):
    """
    出院小结OCR提取结果（可能有多份）
    """
    patient_name: str
    diagnosis_codes: List[str]
    procedure_codes: List[str]
    admission_date: date
    discharge_date: date
    attending_physician: str
    hospital_name: str
    discharge_condition: str
    signatures: List[SignatureInfo] = []  # 签名信息列表

class InvoiceOCR(BaseModel):
    """
    发票OCR提取结果（可能有多份）
    """
    total_amount: float
    service_date: date
    hospital_name: str
    itemized_charges: List[dict]
    signatures: List[SignatureInfo] = []  # 签名信息列表

class ReceiptOCR(BaseModel):
    """
    收据OCR提取结果（可能有多份）
    """
    payment_amount: float
    payment_date: date
    payment_method: str
    merchant_name: str
    transaction_reference: str
    patient_name: str
    signatures: List[SignatureInfo] = []  # 签名信息列表

class PaymentProofOCR(BaseModel):
    """
    付款证明OCR提取结果（可能有多份）
    """
    payer_name: str
    payment_amount: float
    payment_date: date
    payment_method: str
    beneficiary_name: str
    transaction_id: str
    signatures: List[SignatureInfo] = []  # 签名信息列表

class IDCardOCR(BaseModel):
    """
    身份证OCR提取结果（可能有多份）
    """
    name: str
    id_number: str
    date_of_birth: date
    address: str
    issue_date: date
    expiry_date: date
    signatures: List[SignatureInfo] = []  # 签名信息列表

class OCROutput(BaseModel):
    """
    OCR处理结果
    包含所有文档类型的提取结果，支持同一类型多个文档
    """
    claim_form: ClaimFormOCR  # 理赔表（只有一份）
    discharge: List[DischargeOCR] = []  # 出院小结（可能有多份）
    invoice: List[InvoiceOCR] = []  # 发票（可能有多份）
    receipt: List[ReceiptOCR] = []  # 收据（可能有多份）
    payment_proof: List[PaymentProofOCR] = []  # 付款证明（可能有多份）
    id_card: List[IDCardOCR] = []  # 身份证（可能有多份）
    metadata: DocumentMetadata