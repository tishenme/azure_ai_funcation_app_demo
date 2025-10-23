from document_classifiers.base_classifier import BaseDocumentClassifier, DocumentType
from document_classifiers.v1.prompt import CLASSIFY_PROMPT
# 注意：这里为了简化，我们使用简单的关键字匹配而不是实际调用AI
# 在实际实现中，你需要在这里调用OpenAI或其他分类方法

class DocumentClassifierV1(BaseDocumentClassifier):
    def classify(self, text: str) -> DocumentType:
        """
        基于文本内容分类文档类型 (简化版实现)
        在实际应用中，这将调用OpenAI API使用CLASSIFY_PROMPT
        """
        text_lower = text.lower()
        
        # 基于关键字的简单分类逻辑
        if "claim" in text_lower and ("policy" in text_lower or "insur" in text_lower):
            return "claim_form"
        elif "discharge" in text_lower and ("hospital" in text_lower or "treatment" in text_lower):
            return "discharge"
        elif "invoice" in text_lower or ("bill" in text_lower and "amount" in text_lower):
            return "invoice"
        elif "receipt" in text_lower or ("paid" in text_lower and "date" in text_lower):
            return "receipt"
        elif "payment" in text_lower and ("bank" in text_lower or "transaction" in text_lower):
            return "payment_proof"
        elif "id" in text_lower and ("card" in text_lower or "identification" in text_lower):
            return "id_card"
        else:
            # 默认返回，实际实现中应该使用AI分类
            return "claim_form"