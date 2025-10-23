from typing import List
from schemas.document_page import DocumentPage
from schemas.claim_result import ClaimResult
from utils.document_classifier_loader import load_document_classifier
from services.ocr_service import OCRService
from services.ner_service import NERService
from services.rule_service import RuleService
from datetime import datetime
import uuid

class ClaimProcessor:
    def __init__(self):
        # 根据全局配置加载文档分类器
        self.classifier = load_document_classifier()
        self.ocr_service = OCRService()
        self.ner_service = NERService()
        self.rule_service = RuleService()
    
    def process(self, blob_directory: str) -> ClaimResult:
        """
        处理索赔请求的主要入口点
        
        Args:
            blob_directory: Azure Blob存储中的目录路径
            
        Returns:
            ClaimResult: 处理结果
        """
        print(f"Processing claim from directory: {blob_directory}")
        print(f"Using document classifier version: {type(self.classifier).__name__}")
        
        # 1. 模拟下载和预处理PDF文件
        # 在实际实现中，这里会从Azure Blob Storage下载文件
        page_texts = self._download_and_extract_pages(blob_directory)
        
        # 2. 对文档页面进行分类
        classified_pages = self._classify_pages(page_texts)
        
        # 3. OCR处理 - 支持多文档结构
        ocr_result = self.ocr_service.process_documents(classified_pages)
        
        # 4. NER处理 - 支持从多文档中提取实体
        ner_result = self.ner_service.extract_entities(ocr_result)
        
        # 5. 规则检查 - 基于多文档的规则验证
        rule_result = self.rule_service.check_claim(ner_result, ocr_result)
        
        # 6. 构建最终结果 - 适配多文档输出结构
        claim_id = ocr_result.metadata.claim_id or str(uuid.uuid4())
        policy_number = ocr_result.metadata.policy_number or ner_result.policy_number
        
        claim_result = ClaimResult(
            claim_id=claim_id,
            policy_number=policy_number,
            ocr=ocr_result,
            ner=ner_result,
            rule_check=rule_result,
            overall_status=rule_result.final_decision,
            processing_timestamp=datetime.utcnow(),
            pipeline_version="1.1.0"  # 更新版本号以反映多文档支持
        )
        
        return claim_result
    
    def _download_and_extract_pages(self, blob_directory: str) -> List[str]:
        """
        模拟从Blob存储下载PDF并提取页面文本
        
        Args:
            blob_directory: Blob目录路径
            
        Returns:
            页面文本列表
        """
        # 在实际实现中，这里会:
        # 1. 连接到Azure Blob Storage
        # 2. 下载目录中的所有PDF文件
        # 3. 将PDF分解为页面
        # 4. 使用OCR提取每页文本
        
        # 为简化起见，我们返回模拟数据，包括多份文档示例
        return [
            # 理赔表 (只有一份)
            "Insurance Claim Form\nPolicy Number: POL-2025-001\nPatient: John Doe\nClaim Amount: $1,250.00\nDate of Service: 2025-01-15\nDiagnosis: I10, E11.9",
            
            # 出院小结 (可能有多份)
            "Discharge Summary\nPatient: John Doe\nDiagnosis: I10, E11.9\nProcedure: 99213, 85025\nAdmission: 2025-01-10\nDischarge: 2025-01-15\nPhysician: Dr. Smith",
            
            # 发票 (可能有多份)
            "Invoice\nHospital: City General Hospital\nTotal Amount: $1,250.00\nService Date: 2025-01-15\nItemized:\n- Consultation: $100.00\n- Laboratory: $350.00\n- Medication: $800.00",
            
            # 另一份发票
            "Invoice\nHospital: City General Hospital\nTotal Amount: $200.00\nService Date: 2025-01-16\nItemized:\n- Follow-up Visit: $200.00",
            
            # 收据 (可能缺失或有多份)
            "Receipt\nPayment Amount: $1,450.00\nPayment Date: 2025-01-20\nPayment Method: Credit Card\nMerchant: City General Hospital",
            
            # 身份证 (可能缺失或只有一份)
            "ID Card\nName: John Doe\nDate of Birth: 1980-05-15\nID Number: ID-1980-05-15-1234\nExpiration Date: 2030-05-15"
        ]
    
    def _classify_pages(self, page_texts: List[str]) -> List[DocumentPage]:
        """
        对文档页面进行分类
        
        Args:
            page_texts: 文档页面文本列表
            
        Returns:
            DocumentPage对象列表
        """
        classified_pages = []
        for i, text in enumerate(page_texts):
            document_type = self.classifier.classify(text)
            classified_pages.append(DocumentPage(
                page_number=i,
                raw_text=text,
                document_type=document_type,
                confidence=0.95  # 简化处理，实际应由分类器提供
            ))
        return classified_pages