from document_processors.base_processor import BaseDocumentProcessor
from document_processors.id_card.v1.prompt import ID_CARD_V1_PROMPT
from document_processors.id_card.v1.rules import validate_id_card
from schemas.ocr_output import IDCardOCR
from typing import List

class IDCardV1Processor(BaseDocumentProcessor):
    """
    ID Card v1 版本处理器
    """
    
    def extract(self, page_texts: List[str]) -> IDCardOCR:
        """
        从ID Card文档中提取信息
        
        Args:
            page_texts: 文档页面文本列表
            
        Returns:
            IDCardOCR: 提取的信息
        """
        # 合并所有页面文本
        combined_text = "\n".join(page_texts)
        
        # 在实际实现中，这里会调用OpenAI API
        # 为简化起见，我们使用模拟数据
        mock_data = {
            "patient_name": "John Doe",
            "date_of_birth": "1980-05-15",
            "id_number": "ID-1980-05-15-1234",
            "expiration_date": "2030-05-15",
            "issuing_authority": "Government Identity Agency",
            "address": "123 Main St, City, State 12345"
        }
        
        # 应用验证规则
        validated_data = validate_id_card(mock_data)
        
        # 返回Pydantic模型
        return IDCardOCR(**validated_data)