# 理赔AI处理系统

一个智能文档处理系统，使用Azure AI服务将非结构化的保险理赔文档转换为结构化数据。该系统通过多阶段流水线处理各种文档类型：OCR → NER → 规则检查，并对理赔申请做出自动化决策。

## 目录

- [概述](#概述)
- [架构](#架构)
- [项目结构](#项目结构)
- [流水线阶段](#流水线阶段)
- [版本控制系统](#版本控制系统)
- [配置](#配置)
- [服务](#服务)
- [Azure工具](#azure工具)
- [日志记录](#日志记录)
- [开发](#开发)
- [测试](#测试)
- [部署](#部署)

## 概述

理赔AI处理器旨在通过分析上传的文档并根据业务规则做出决策来自动化保险理赔处理。它处理保险理赔中常见的六种文档类型：

1. 理赔表
2. 出院文件
3. 发票/账单
4. 收据
5. 付款证明
6. 身份证

该系统使用Azure AI服务，包括Azure文档智能和Azure OpenAI从这些文档中提取和处理信息。

## 架构

该系统采用模块化、版本控制的架构，便于更新和维护：

```
输入文档 → 文档分类 → OCR处理 → NER提取 → 规则引擎 → 决策输出
```

每个阶段都是独立版本控制的，可以在不影响其他组件的情况下进行更新。

## 项目结构

```
claims-ai-processor/
│
├── config/                          # 配置文件
│   ├── global_versions.yaml         # 全局组件版本
│   ├── document_versions.yaml       # 每个文档的版本控制
│   └── settings.py                  # 配置加载和管理
│
├── document_classifiers/            # 文档类型分类
│   ├── base_classifier.py           # 抽象基类
│   └── v1/                          # 分类器版本1
│       ├── classifier.py
│       └── prompt.py
│
├── document_processors/             # 文档特定处理逻辑
│   ├── base_processor.py            # 抽象基类
│   ├── claim_form/                  # 理赔表处理器
│   │   ├── v1/
│   │   │   ├── processor.py
│   │   │   ├── prompt.py
│   │   │   └── rules.py
│   │   └── v2/
│   │       ├── processor.py
│   │       ├── prompt.py
│   │       └── rules.py
│   ├── discharge/                   # 出院文档处理器
│   │   └── v1/
│   │       ├── processor.py
│   │       ├── prompt.py
│   │       └── rules.py
│   ├── invoice/                     # 发票处理器
│   │   ├── v1/
│   │   └── v2/
│   ├── receipt/                     # 收据处理器
│   │   └── v1/
│   ├── payment_proof/               # 付款证明处理器
│   │   └── v1/
│   └── id_card/                     # 身份证处理器
│       └── v1/
│
├── ner_extractors/                  # 命名实体识别
│   ├── base_ner.py                  # 抽象基类
│   ├── v1/                          # NER版本1
│   └── v2/                          # NER版本2
│
├── rule_engines/                    # 业务规则引擎
│   ├── base_rule_engine.py          # 抽象基类
│   ├── rules_2025_q3_v1.py          # 2025年Q3规则
│   └── rules_2025_q4_v1.py          # 2025年Q4规则
│
├── services/                        # 流水线编排
│   ├── ocr_service.py               # OCR处理服务
│   ├── ner_service.py               # NER提取服务
│   └── rule_service.py              # 规则检查服务
│
├── handlers/                        # 主处理程序
│   └── claim_processor.py           # 端到端理赔处理
│
├── utils/                           # 工具函数
│   ├── document_classifier_loader.py # 文档分类器加载器
│   ├── azure_document_intelligence.py # Azure文档智能客户端
│   ├── openai_client.py             # Azure OpenAI客户端
│   ├── blob_storage.py              # Azure Blob存储客户端
│   └── log_manager.py               # 日志管理器（集成Application Insights）
│
├── schemas/                         # 数据模型和验证
│   ├── ocr_output.py                # OCR输出模式
│   ├── ner_output.py                # NER输出模式
│   ├── rule_output.py               # 规则引擎输出模式
│   └── claim_result.py              # 最终理赔结果模式
│
├── tests/                           # 测试套件
│   ├── unit/                        # 单元测试
│   └── integration/                 # 集成测试
│
├── main.py                          # Azure函数入口点
├── host.json                        # Azure函数主机配置
├── function.json                    # 函数绑定配置
├── requirements.txt                 # Python依赖
└── requirements-test.txt            # 测试依赖
```

## 流水线阶段

### 1. 文档分类

第一阶段使用文档分类器识别每页代表的文档类型。

**输入：** 原始PDF页面
**输出：** 已分类的带文档类型标签的页面

### 2. OCR处理

根据文档类型使用专门的处理器处理每个文档。

**输入：** 已分类的文档页面
**输出：** 每种文档类型的结构化JSON数据

### 3. NER提取

跨所有文档提取和标准化实体。

**输入：** 所有文档的OCR输出
**输出：** 带标准化代码的统一实体数据

### 4. 规则检查

应用业务规则做出最终决策。

**输入：** NER输出和来自数据库的保单数据
**输出：** 最终批准/拒绝决策

## 版本控制系统

该系统实现了双版本控制方法：

### 全局版本 (`config/global_versions.yaml`)

控制系统范围组件的版本：

```yaml
openai_model: "gpt-4o-2025-08-06"
azure_document_intelligence_api_version: "2024-02-29"
document_classifier_version: "v1"
ner_extractor_version: "v2"
rule_engine: "rules_2025_q4_v1"
```

### 文档特定版本 (`config/document_versions.yaml`)

控制各个文档处理器的版本：

```yaml
claim_form:
  version: "v2"
  required: true
invoice:
  version: "v2"
  required: true
receipt:
  version: "v1"
  required: false
```

## 配置

配置文件位于[config/](config/)目录中：

- [global_versions.yaml](config/global_versions.yaml)：控制全局组件版本
- [document_versions.yaml](config/document_versions.yaml)：控制每个文档处理版本
- [settings.py](config/settings.py)：加载和管理配置值

## 服务

该系统被组织为独立的服务，处理处理过程的不同阶段：

### OCR服务 ([services/ocr_service.py](services/ocr_service.py))

根据类型和版本将文档路由到适当的处理器，聚合结果。

### NER服务 ([services/ner_service.py](services/ner_service.py))

执行跨文档实体识别和标准化。

### 规则服务 ([services/rule_service.py](services/rule_service.py))

应用业务规则并根据提取的数据和策略信息做出最终决策。

## Azure工具

系统提供了与Azure服务交互的工具类：

### Azure文档智能 ([utils/azure_document_intelligence.py](utils/azure_document_intelligence.py))

提供使用Azure文档智能服务的文档分析功能：

- 文档文本提取
- 表格和键值对提取
- 支持各种预构建模型

### Azure OpenAI ([utils/openai_client.py](utils/openai_client.py))

Azure OpenAI服务的封装：

- 聊天完成API
- 从文档中提取结构化数据
- 文档分类

### Azure Blob存储 ([utils/blob_storage.py](utils/blob_storage.py))

处理Azure Blob存储的工具：

- 上传和下载blob
- 列出容器中的blob
- 检查blob是否存在
- 生成SAS URL以安全访问私有blob

`generate_sas_url`方法允许在不公开blob的情况下安全访问它们。当需要将blob URL传递给Azure OpenAI进行图像分析时，这特别有用，因为它在提供临时访问权限的同时保持了安全性。

## 日志记录

系统使用[LogManager](utils/log_manager.py)进行集中日志记录，并与Azure Application Insights集成：

- 结构化日志记录，支持自定义属性
- 分布式追踪支持
- 自定义事件和指标记录
- 异常跟踪

LogManager提供单例实例，确保应用程序中的日志记录一致性，并将遥测数据发送到Azure Application Insights以进行监控和分析。

## 开发

设置开发环境：

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 对于测试，还需要安装测试依赖：
   ```bash
   pip install -r requirements-test.txt
   ```

3. 为Azure服务配置环境变量：
   - `AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT`
   - `AZURE_DOCUMENT_INTELLIGENCE_KEY`
   - `AZURE_OPENAI_ENDPOINT`
   - `AZURE_OPENAI_KEY`
   - `AZURE_STORAGE_CONNECTION_STRING`
   - `AZURE_STORAGE_ACCOUNT_NAME`
   - `AZURE_STORAGE_ACCOUNT_KEY`
   - `APPLICATIONINSIGHTS_CONNECTION_STRING`
   - `DATABASE_CONNECTION_STRING`

## 测试

该项目包括单元测试和集成测试：

```bash
# 运行所有测试
pytest

# 仅运行单元测试
pytest tests/unit

# 仅运行集成测试
pytest tests/integration
```

测试按项目结构组织，有针对单个组件的单元测试和针对端到端工作流的集成测试。

## 部署

该系统被设计为具有blob触发器的Azure函数应用。可以通过以下方式部署：

1. Azure Functions Core Tools
2. GitHub Actions CI/CD
3. Azure DevOps Pipelines

当理赔文档上传到指定的blob容器时触发函数，并将结构化结果输出到另一个容器。