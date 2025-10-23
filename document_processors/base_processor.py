from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List

class BaseDocumentProcessor(ABC):
    """
    文档处理器抽象基类
    """
    
    @abstractmethod
    def extract(self, page_texts: List[str]) -> BaseModel:
        """
        从文档页面文本中提取信息
        
        Args:
            page_texts: 文档页面文本列表 (一个文档可能有多页)
            
        Returns:
            提取的信息（特定于文档类型的Pydantic模型）
        """
        pass