from abc import ABC, abstractmethod
from typing import Literal

DocumentType = Literal["claim_form", "discharge", "invoice", "receipt", "payment_proof", "id_card"]

class BaseDocumentClassifier(ABC):
    @abstractmethod
    def classify(self, text: str) -> DocumentType:
        """
        根据文本内容分类文档类型
        
        Args:
            text: 文档页面的文本内容
            
        Returns:
            DocumentType: 文档类型
        """
        pass