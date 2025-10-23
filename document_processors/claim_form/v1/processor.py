from document_processors.base_processor import BaseDocumentProcessor
from document_processors.claim_form.v1.prompt import CLAIM_FORM_V1_PROMPT
from document_processors.claim_form.v1.rules import validate_claim_form
from schemas.ocr_output import ClaimFormOCR
from typing import List

class ClaimFormV1Processor(BaseDocumentProcessor):
    """
    Claim Form v1 版本处理器
    """
    
    def extract(self, page_texts: List[str]) -> ClaimFormOCR:
        """
        从Claim Form中提取信息
        
        Args:
            page_texts: 文档页面文本列表 (理赔表通常只有一页)
            
        Returns:
            ClaimFormOCR: 提取的信息
        """
        # 合并所有页面文本
        combined_text = "\n".join(page_texts)
        
        # 在实际实现中，这里会调用OpenAI API
        # 为简化起见，我们使用模拟数据
        mock_data = {
            "policy_number": "POL-2025-001",
            "patient_name": "John Doe",
            "claim_amount": 1250.00,
            "date_of_service": "2025-01-15",
            "diagnosis_codes": ["I10", "E11.9"]
        }
        
        # 应用验证规则
        validated_data = validate_claim_form(mock_data)
        
        # 返回Pydantic模型
        return ClaimFormOCR(**validated_data)