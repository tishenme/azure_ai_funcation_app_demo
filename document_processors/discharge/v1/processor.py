from document_processors.base_processor import BaseDocumentProcessor
from document_processors.discharge.v1.prompt import DISCHARGE_V1_PROMPT
from document_processors.discharge.v1.rules import validate_discharge
from schemas.ocr_output import DischargeOCR
from typing import List

class DischargeV1Processor(BaseDocumentProcessor):
    """
    Discharge v1 版本处理器
    """
    
    def extract(self, page_texts: List[str]) -> DischargeOCR:
        """
        从Discharge文档中提取信息
        
        Args:
            page_texts: 文档页面文本列表
            
        Returns:
            DischargeOCR: 提取的信息
        """
        # 合并所有页面文本
        combined_text = "\n".join(page_texts)
        
        # 在实际实现中，这里会调用OpenAI API
        # 为简化起见，我们使用模拟数据
        mock_data = {
            "patient_name": "John Doe",
            "diagnosis_codes": ["I10", "E11.9"],
            "procedure_codes": ["99213", "85025"],
            "admission_date": "2025-01-10",
            "discharge_date": "2025-01-15",
            "attending_physician": "Dr. Smith",
            "hospital_name": "City General Hospital",
            "discharge_condition": "Stable"
        }
        
        # 应用验证规则
        validated_data = validate_discharge(mock_data)
        
        # 返回Pydantic模型
        return DischargeOCR(**validated_data)