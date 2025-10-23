from document_processors.base_processor import BaseDocumentProcessor
from document_processors.receipt.v1.prompt import RECEIPT_V1_PROMPT
from document_processors.receipt.v1.rules import validate_receipt
from schemas.ocr_output import ReceiptOCR
from typing import List

class ReceiptV1Processor(BaseDocumentProcessor):
    """
    Receipt v1 版本处理器
    """
    
    def extract(self, page_texts: List[str]) -> ReceiptOCR:
        """
        从Receipt文档中提取信息
        
        Args:
            page_texts: 文档页面文本列表
            
        Returns:
            ReceiptOCR: 提取的信息
        """
        # 合并所有页面文本
        combined_text = "\n".join(page_texts)
        
        # 在实际实现中，这里会调用OpenAI API
        # 为简化起见，我们使用模拟数据
        mock_data = {
            "payment_amount": 1250.00,
            "payment_date": "2025-01-20",
            "payment_method": "Credit Card",
            "merchant_name": "City General Hospital",
            "transaction_reference": "TXN-2025-456",
            "patient_name": "John Doe"
        }
        
        # 应用验证规则
        validated_data = validate_receipt(mock_data)
        
        # 返回Pydantic模型
        return ReceiptOCR(**validated_data)