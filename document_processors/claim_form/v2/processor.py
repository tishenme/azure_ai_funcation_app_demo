from document_processors.base_processor import BaseDocumentProcessor
from document_processors.claim_form.v2.prompt import CLAIM_FORM_V2_PROMPT
from document_processors.claim_form.v2.rules import validate_claim_form_v2
from schemas.ocr_output import ClaimFormOCR
from typing import List

class ClaimFormV2Processor(BaseDocumentProcessor):
    """
    Claim Form v2 版本处理器
    """
    
    def extract(self, page_texts: List[str]) -> ClaimFormOCR:
        """
        从Claim Form中提取信息
        
        Args:
            page_texts: 文档页面文本列表
            
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
            "diagnosis_codes": ["I10", "E11.9"],
            "provider_name": "City General Hospital",
            "provider_npi": "1234567890",
            "claim_submission_date": "2025-01-20"
        }
        
        # 应用验证规则
        validated_data = validate_claim_form_v2(mock_data)
        
        # 返回Pydantic模型
        return ClaimFormOCR(**validated_data)