from abc import ABC, abstractmethod
from schemas.ner_output import NEROutput
from schemas.ocr_output import OCROutput
from schemas.rule_output import RuleCheckOutput

class BaseRuleEngine(ABC):
    """
    规则引擎抽象基类
    """
    
    @abstractmethod
    def check_claim(self, ner_output: NEROutput, policy_data: dict, ocr_output: OCROutput) -> RuleCheckOutput:
        """
        检查索赔是否符合规则
        
        Args:
            ner_output: NER处理结果
            policy_data: 从数据库获取的策略数据
            ocr_output: OCR处理结果
            
        Returns:
            RuleCheckOutput: 规则检查结果
        """
        pass