from typing import List
from schemas.document_page import DocumentPage
from schemas.ocr_output import OCROutput, OCRMetadata, ClaimFormOCR, DischargeOCR, InvoiceOCR, ReceiptOCR, PaymentProofOCR, IDCardOCR
from document_processors.loader import load_document_processor
from config.settings import get_document_version, is_document_required
import datetime

class OCRService:
    """
    OCR服务，负责协调不同文档类型的处理
    """
    
    def process_documents(self, document_pages: List[DocumentPage]) -> OCROutput:
        """
        处理文档页面，生成OCR输出
        
        Args:
            document_pages: 已分类的文档页面列表
            
        Returns:
            OCROutput: OCR处理结果
        """
        # 按文档类型分组页面
        pages_by_type = {}
        for page in document_pages:
            if page.document_type not in pages_by_type:
                pages_by_type[page.document_type] = []
            pages_by_type[page.document_type].append(page)
        
        # 初始化结果字典
        results = {}
        
        # 处理claim_form（通常只有一份）
        if "claim_form" in pages_by_type:
            pages = pages_by_type["claim_form"]
            processor = load_document_processor("claim_form")
            page_texts = [page.raw_text for page in pages]
            extracted_data = processor.extract(page_texts)
            results["claim_form"] = extracted_data
        
        # 处理可能有多份的文档类型
        multi_doc_types = ["discharge", "invoice", "receipt", "payment_proof", "id_card"]
        for doc_type in multi_doc_types:
            if doc_type in pages_by_type:
                docs_list = []
                # 对于每份文档（可能有多页），调用相应的处理器
                pages = pages_by_type[doc_type]
                processor = load_document_processor(doc_type)
                page_texts = [page.raw_text for page in pages]
                extracted_data = processor.extract(page_texts)
                docs_list.append(extracted_data)
                results[doc_type] = docs_list
        
        # 检查必需的文档是否存在
        missing_required_docs = []
        for doc_type in ["claim_form", "discharge", "invoice", "receipt", "payment_proof", "id_card"]:
            if is_document_required(doc_type) and doc_type not in pages_by_type:
                missing_required_docs.append(doc_type)
        
        if missing_required_docs:
            print(f"Warning: Missing required documents: {missing_required_docs}")
        
        # 创建元数据
        metadata = self._create_metadata(pages_by_type)
        
        # 构建最终结果
        ocr_output = OCROutput(
            metadata=metadata,
            **results
        )
        
        return ocr_output
    
    def _create_metadata(self, pages_by_type: dict) -> OCRMetadata:
        """
        创建OCR元数据
        
        Args:
            pages_by_type: 按类型分组的页面
            
        Returns:
            OCRMetadata: 元数据对象
        """
        # 从处理的文档中提取策略号（如果存在）
        policy_number = None
        claim_id = None
        
        # 尝试从claim_form中获取策略号
        if "claim_form" in pages_by_type and pages_by_type["claim_form"]:
            # 在实际实现中，我们会从处理结果中提取
            policy_number = "POL-2025-001"  # 示例值
            claim_id = "CLAIM-2025-001"     # 示例值
        
        # 获取文档版本信息
        document_versions = {}
        for doc_type in pages_by_type.keys():
            document_versions[doc_type] = get_document_version(doc_type)
        
        return OCRMetadata(
            policy_number=policy_number,
            claim_id=claim_id,
            ocr_version="1.0.0",  # 示例版本号
            document_versions=document_versions
        )