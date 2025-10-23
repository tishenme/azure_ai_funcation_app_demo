from rule_engines.base_rule_engine import BaseRuleEngine
from schemas.ner_output import NEROutput
from schemas.ocr_output import OCROutput
from schemas.rule_output import RuleCheckOutput
from config.settings import is_document_required

class Rules2025Q4V1(BaseRuleEngine):
    """
    2025年Q4版本规则引擎（基于Q3版本的更新）
    """
    
    def check_claim(self, ner_output: NEROutput, policy_data: dict, ocr_output: OCROutput) -> RuleCheckOutput:
        """
        检查索赔是否符合2025年Q4规则
        
        Args:
            ner_output: NER处理结果
            policy_data: 从数据库获取的策略数据
            ocr_output: OCR处理结果
            
        Returns:
            RuleCheckOutput: 规则检查结果
        """
        # 调用Q3版本的检查作为基础
        q3_engine = Rules2025Q3V1()
        result = q3_engine.check_claim(ner_output, policy_data, ocr_output)
        
        # 添加Q4特有的检查规则
        additional_rejections = []
        
        # 检查是否需要提供支付证明（Q4新规则）
        if ner_output.total_claimed_amount and ner_output.total_claimed_amount > 1000:
            # 检查是否提供了支付证明
            if not ocr_output.payment_proof:
                additional_rejections.append("Payment proof required for claims over $1000")
        
        # 更新结果
        result.rejection_reasons.extend(additional_rejections)
        if additional_rejections:
            result.final_decision = "REJECTED"
        
        result.rule_engine_version = "rules_2025_q4_v1"
        
        return result

class Rules2025Q3V1:
    """
    为避免循环导入而简化实现的Q3规则引擎
    """
    def check_claim(self, ner_output: NEROutput, policy_data: dict, ocr_output: OCROutput) -> RuleCheckOutput:
        rejection_reasons = []
        missing_documents = []
        
        # 检查策略是否有效
        policy_valid = policy_data.get("is_active", False)
        if not policy_valid:
            rejection_reasons.append("Policy is not active")
        
        # 检查覆盖范围是否有效
        coverage_active = policy_data.get("coverage_active", False)
        if not coverage_active:
            rejection_reasons.append("Coverage is not active")
        
        # 检查诊断代码是否在覆盖范围内
        diagnosis_covered = True
        excluded_diagnoses = policy_data.get("excluded_diagnoses", [])
        for diagnosis in ner_output.diagnosis_codes:
            if diagnosis in excluded_diagnoses:
                diagnosis_covered = False
                rejection_reasons.append(f"Diagnosis {diagnosis} is not covered")
                break
        
        # 检查金额是否在限额内
        amount_within_limit = True
        claim_amount = ner_output.total_claimed_amount or 0
        policy_limit = policy_data.get("claim_limit", float('inf'))
        if claim_amount > policy_limit:
            amount_within_limit = False
            rejection_reasons.append(f"Claim amount {claim_amount} exceeds policy limit {policy_limit}")
        
        # 检查必需的文档是否存在
        required_documents = policy_data.get("required_documents", [])
        for doc_type in required_documents:
            # 检查文档是否在OCR输出中存在
            if not getattr(ocr_output, doc_type, None):
                missing_documents.append(doc_type)
                rejection_reasons.append(f"Required document missing: {doc_type}")
        
        # 检查配置中必需的文档是否存在
        for doc_type in ["claim_form", "discharge", "invoice", "receipt", "payment_proof", "id_card"]:
            if is_document_required(doc_type) and not getattr(ocr_output, doc_type, None):
                if doc_type not in missing_documents:  # 避免重复
                    missing_documents.append(doc_type)
        
        # 确定最终决策
        if not rejection_reasons:
            final_decision = "APPROVED"
        else:
            final_decision = "REJECTED"
        
        return RuleCheckOutput(
            policy_valid=policy_valid,
            coverage_active=coverage_active,
            diagnosis_covered=diagnosis_covered,
            amount_within_limit=amount_within_limit,
            missing_documents=missing_documents,
            final_decision=final_decision,
            rejection_reasons=rejection_reasons,
            rule_engine_version="rules_2025_q3_v1"
        )