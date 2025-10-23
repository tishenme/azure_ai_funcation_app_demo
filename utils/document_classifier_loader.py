from config.settings import DOCUMENT_CLASSIFIER_VERSION

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