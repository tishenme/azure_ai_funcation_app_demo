"""
文档分类器加载器
根据全局配置加载相应的文档分类器版本
"""
import uuid
from typing import List
from config.settings import DOCUMENT_CLASSIFIER_VERSION
from schemas.document_page import DocumentPage

def load_document_classifier():
    """
    根据全局配置加载相应的文档分类器版本
    """
    if DOCUMENT_CLASSIFIER_VERSION == "v1":
        from document_classifiers.v1.classifier import DocumentClassifierV1
        return DocumentClassifierV1()
    elif DOCUMENT_CLASSIFIER_VERSION == "v2":
        # 为将来扩展预留
        try:
            from document_classifiers.v2.classifier import DocumentClassifierV2
            return DocumentClassifierV2()
        except ImportError:
            raise ValueError(f"Document classifier version {DOCUMENT_CLASSIFIER_VERSION} not implemented")
    else:
        raise ValueError(f"Unsupported classifier version: {DOCUMENT_CLASSIFIER_VERSION}")

def group_pages_into_documents(pages: List[DocumentPage]) -> List[DocumentPage]:
    """
    将页面分组为文档，为同一类型的不同文档分配唯一ID
    
    Args:
        pages: 已分类的页面列表
        
    Returns:
        带有文档ID的页面列表
    """
    # 按页面顺序和文档类型分组
    result_pages = []
    document_counters = {}  # 记录每种文档类型的计数
    
    # 先处理claim_form类型，确保只有一份
    claim_form_pages = [page for page in pages if page.document_type == "claim_form"]
    other_pages = [page for page in pages if page.document_type != "claim_form"]
    
    # 为理赔表分配ID
    for page in claim_form_pages:
        page.document_id = "claim_form_1"
        result_pages.append(page)
    
    # 为其他文档类型分配ID
    for page in other_pages:
        doc_type = page.document_type
        if doc_type not in document_counters:
            document_counters[doc_type] = 1
        else:
            # 简化逻辑：每遇到一个新页面就认为是新文档
            # 在实际实现中，这里可能需要更复杂的逻辑来判断页面是否属于同一文档
            document_counters[doc_type] += 1
        
        page.document_id = f"{doc_type}_{document_counters[doc_type]}"
        result_pages.append(page)
    
    return result_pages