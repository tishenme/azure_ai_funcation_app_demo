from pydantic import BaseModel
from typing import List, Dict, Any

class OCROutput(BaseModel):
    """
    OCR处理输出模型
    """
    document_type: str
    confidence: float
    extracted_data: Dict[str, Any]
    page_count: int
    file_name: str
    checksum: str
    
    class Config:
        schema_extra = {
            "example": {
                "document_type": "invoice",
                "confidence": 0.95,
                "extracted_data": {
                    "total_amount": 1200.0,
                    "date": "2025-01-15",
                    "provider": "北京协和医院"
                },
                "page_count": 1,
                "file_name": "invoice_001.pdf",
                "checksum": "a1b2c3d4e5f6"
            }
        }
from schemas.ner_output import NEROutput
from schemas.ocr_output import OCROutput
from schemas.rule_output import RuleCheckOutput
from config.settings import RULE_ENGINE
import importlib

class RuleService:
    """
    规则服务，负责加载和执行规则引擎
    """
    
    def check_claim(self, ner_output: NEROutput, ocr_outputs: List[OCROutput]) -> RuleCheckOutput:
        """
        检查索赔是否符合规则
        
        Args:
            ner_output: NER处理结果
            ocr_outputs: 多个OCR处理结果列表
            
        Returns:
            RuleCheckOutput: 规则检查结果
        """
        # 根据配置加载规则引擎
        rule_engine = self._load_rule_engine()
        
        # 模拟从数据库获取策略数据
        policy_data = self._get_policy_data(ner_output.policy_number)
        
        # 初始化汇总结果
        all_results = []
        passed = True
        messages = []

        # 遍历每个OCR输出并执行规则检查
        for ocr_output in ocr_outputs:
            result = rule_engine.check_claim(ner_output, policy_data, ocr_output)
            all_results.append(result)
            
            if not result.passed:
                passed = False
                messages.extend(result.messages)

        # 合并最终结果
        final_result = RuleCheckOutput(
            passed=passed,
            claim_id=ner_output.claim_id,
            policy_number=ner_output.policy_number,
            messages=messages or ["所有文档均通过规则检查"]
        )
        
        return final_result
    
    def _load_rule_engine(self):
        """
        根据配置加载规则引擎
        
        Returns:
            规则引擎实例
        """
        if RULE_ENGINE == "rules_2025_q3_v1":
            from rule_engines.rules_2025_q3_v1 import Rules2025Q3V1
            return Rules2025Q3V1()
        elif RULE_ENGINE == "rules_2025_q4_v1":
            from rule_engines.rules_2025_q4_v1 import Rules2025Q4V1
            return Rules2025Q4V1()
        else:
            raise ValueError(f"Unsupported rule engine: {RULE_ENGINE}")
    
    def _get_policy_data(self, policy_number: str) -> dict:
        """
        模拟从数据库获取策略数据
        
        Args:
            policy_number: 策略号
            
        Returns:
            策略数据
        """
        # 在实际实现中，这里会查询数据库
        # 为简化起见，我们返回模拟数据
        return {
            "is_active": True,
            "coverage_active": True,
            "excluded_diagnoses": ["Z00.00", "Z01.818"],  # 示例排除诊断
            "claim_limit": 5000.0,  # 索赔限额
            "required_documents": ["claim_form", "invoice"],  # 必需的文档
            "has_payment_proof": True  # 是否有支付证明
        }