from config.settings import get_document_version

def load_document_processor(document_type: str):
    """
    根据文档类型和配置版本加载相应的文档处理器
    
    Args:
        document_type: 文档类型
        
    Returns:
        对应的文档处理器实例
    """
    version = get_document_version(document_type)
    
    if document_type == "claim_form":
        if version == "v1":
            from document_processors.claim_form.v1.processor import ClaimFormV1Processor
            return ClaimFormV1Processor()
        elif version == "v2":
            from document_processors.claim_form.v2.processor import ClaimFormV2Processor
            return ClaimFormV2Processor()
    elif document_type == "discharge":
        if version == "v1":
            from document_processors.discharge.v1.processor import DischargeV1Processor
            return DischargeV1Processor()
    elif document_type == "invoice":
        if version == "v1":
            from document_processors.invoice.v1.processor import InvoiceV1Processor
            return InvoiceV1Processor()
    elif document_type == "receipt":
        if version == "v1":
            from document_processors.receipt.v1.processor import ReceiptV1Processor
            return ReceiptV1Processor()
    elif document_type == "payment_proof":
        if version == "v1":
            from document_processors.payment_proof.v1.processor import PaymentProofV1Processor
            return PaymentProofV1Processor()
    elif document_type == "id_card":
        if version == "v1":
            from document_processors.id_card.v1.processor import IDCardV1Processor
            return IDCardV1Processor()
    
    raise ValueError(f"Unsupported document type '{document_type}' or version '{version}'")