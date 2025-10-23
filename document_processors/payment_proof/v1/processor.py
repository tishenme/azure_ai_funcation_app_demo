from document_processors.base_processor import BaseDocumentProcessor
from document_processors.payment_proof.v1.prompt import PAYMENT_PROOF_V1_PROMPT
from document_processors.payment_proof.v1.rules import validate_payment_proof
from schemas.ocr_output import PaymentProofOCR
from typing import List

class PaymentProofV1Processor(BaseDocumentProcessor):
    """
    Payment Proof v1 版本处理器
    """
    
    def extract(self, page_texts: List[str]) -> PaymentProofOCR:
        """
        从Payment Proof文档中提取信息
        
        Args:
            page_texts: 文档页面文本列表
            
        Returns:
            PaymentProofOCR: 提取的信息
        """
        # 合并所有页面文本
        combined_text = "\n".join(page_texts)
        
        # 在实际实现中，这里会调用OpenAI API
        # 为简化起见，我们使用模拟数据
        mock_data = {
            "payer_name": "John Doe",
            "payee_name": "City General Hospital",
            "payment_amount": 1250.00,
            "payment_date": "2025-01-20",
            "bank_name": "Global Bank",
            "account_number_last4": "5678",
            "transaction_id": "TXN-2025-456",
            "payment_purpose": "Medical Services"
        }
        
        # 应用验证规则
        validated_data = validate_payment_proof(mock_data)
        
        # 返回Pydantic模型
        return PaymentProofOCR(**validated_data)