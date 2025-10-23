import yaml
from pathlib import Path

# 加载全局配置
def load_global_config():
    config_path = Path(__file__).parent / "global_versions.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

# 加载文档版本配置
def load_document_versions():
    config_path = Path(__file__).parent / "document_versions.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

# 全局配置
GLOBAL_CONFIG = load_global_config()

# 文档版本配置
DOCUMENT_VERSIONS = load_document_versions()

# 提供便捷访问
DOCUMENT_CLASSIFIER_VERSION = GLOBAL_CONFIG["document_classifier_version"]
NER_VERSION = GLOBAL_CONFIG["ner_extractor_version"]
RULE_ENGINE = GLOBAL_CONFIG["rule_engine"]
OPENAI_MODEL = GLOBAL_CONFIG["openai_model"]
ADI_API_VERSION = GLOBAL_CONFIG["azure_document_intelligence_api_version"]

# 获取特定文档类型的版本
def get_document_version(document_type: str) -> str:
    return DOCUMENT_VERSIONS.get(document_type, {}).get("version", "v1")

# 检查文档类型是否必需
def is_document_required(document_type: str) -> bool:
    return DOCUMENT_VERSIONS.get(document_type, {}).get("required", False)