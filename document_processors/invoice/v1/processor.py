from document_processors.base_processor import BaseDocumentProcessor
from document_processors.invoice.v1.prompt import INVOICE_V1_PROMPT
from document_processors.invoice.v1.rules import validate_invoice
from schemas.ocr_output import InvoiceOCR
from typing import List

class InvoiceV1Processor(BaseDocumentProcessor):
    """
    Invoice v1 版本处理器
    """
    
    def extract(self, page_texts: List[str]) -> InvoiceOCR:
        """
        从Invoice中提取信息
        
        Args:
            page_texts: 文档页面文本列表 (可能有多份发票，每份发票可能有多页)
            
        Returns:
            InvoiceOCR: 提取的信息 (合并所有发票的信息)
        """
        # 在实际实现中，我们会处理每份发票并合并信息
        # 为简化起见，我们使用模拟数据
        
        # 合并所有页面文本以模拟处理过程
        combined_text = "\n".join(page_texts)
        
        # 模拟从多份发票中提取并合并信息
        mock_data = {
            "total_amount": 1450.00,  # 合并金额
            "hospital_name": "City General Hospital",
            "service_date": "2025-01-15",  # 使用最早的日期
            "itemized_services": [
                {"service": "Consultation", "cost": 100.00},
                {"service": "Laboratory Tests", "cost": 350.00},
                {"service": "Medication", "cost": 800.00},
                {"service": "Follow-up Visit", "cost": 200.00}
            ],
            "patient_account_number": "ACC-2025-789"
        }
        
        # 应用验证规则
        validated_data = validate_invoice(mock_data)
        
        # 返回Pydantic模型
        return InvoiceOCR(**validated_data)