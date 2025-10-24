import uuid
from typing import List, Dict, Optional
from collections import defaultdict
from schemas.document_page import DocumentPage
from schemas.ocr_output import OCROutput, DocumentMetadata
from config.settings import get_document_version, is_document_required
from document_processors.loader import load_document_processor
import datetime

class OCRService:
    """
    OCR服务，负责协调不同文档类型的处理
    """
    
    def process_documents(self, document_pages: List[DocumentPage]) -> OCROutput:
        """
        处理文档页面，支持同一类型多个文档
        
        Args:
            document_pages: 文档页面列表
            
        Returns:
            OCROutput: OCR处理结果
        """
        # 按文档类型和文档ID分组页面
        document_groups = defaultdict(list)
        for page in document_pages:
            # 如果没有文档ID，则生成一个
            doc_id = page.document_id or str(uuid.uuid4())
            group_key = (page.document_type, doc_id)
            document_groups[group_key].append(page)
        
        # 检查必需文档是否存在
        document_types = set(page.document_type for page in document_pages)
        for doc_type in document_types:
            if is_document_required(doc_type):
                # 查找该类型的文档
                type_docs = [k for k in document_groups.keys() if k[0] == doc_type]
                if not type_docs:
                    print(f"Warning: Missing required document type: {doc_type}")
        
        # 处理每个文档组
        results = {
            "discharge": [],
            "invoice": [],
            "receipt": [],
            "payment_proof": [],
            "id_card": []
        }
        
        document_versions = {}
        
        # 先处理claim_form（必须且只有一份）
        claim_form_group = [(k, v) for k, v in document_groups.items() if k[0] == "claim_form"]
        if claim_form_group:
            # 只取第一份理赔表（应该只有一份）
            (doc_type, doc_id), pages = claim_form_group[0]
            version = get_document_version(doc_type)
            document_versions[doc_type] = version
            
            processor = load_document_processor(doc_type, version)
            page_texts = [page.raw_text for page in pages]
            extracted_data = processor.extract(page_texts)
            results["claim_form"] = extracted_data
        else:
            raise ValueError("Required document 'claim_form' is missing")
        
        # 处理可能有多份的文档类型
        multi_doc_types = ["discharge", "invoice", "receipt", "payment_proof", "id_card"]
        for doc_type in multi_doc_types:
            # 查找该类型的所有文档
            type_groups = [(k, v) for k, v in document_groups.items() if k[0] == doc_type]
            for (doc_type, doc_id), pages in type_groups:
                version = get_document_version(doc_type)
                document_versions[doc_type] = version
                
                processor = load_document_processor(doc_type, version)
                page_texts = [page.raw_text for page in pages]
                extracted_data = processor.extract(page_texts)
                results[doc_type].append(extracted_data)
        
        # 构建元数据
        metadata = self._create_metadata(document_versions)
        
        # 构建最终输出
        ocr_output = OCROutput(
            metadata=metadata,
            **results
        )
        
        return ocr_output
    
    def _create_metadata(self, document_versions: Dict[str, str]) -> DocumentMetadata:
        """
        创建OCR元数据
        
        Args:
            document_versions: 文档版本信息
            
        Returns:
            DocumentMetadata: 元数据对象
        """
        # 在实际实现中，我们会从处理结果中提取
        policy_number = "POL-2025-001"  # 示例值
        claim_id = "CLAIM-2025-001"     # 示例值
        
        return DocumentMetadata(
            policy_number=policy_number,
            claim_id=claim_id,
            ocr_version="1.0.0",
            document_versions=document_versions,
            processing_timestamp=datetime.datetime.utcnow().isoformat() + "Z"
        )