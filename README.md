# Claims AI Processor

An intelligent document processing system that transforms unstructured insurance claim documents into structured data using Azure AI services. The system processes various document types through a multi-stage pipeline: OCR → NER → Rule Checking, and makes automated decisions on claim approvals.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Pipeline Stages](#pipeline-stages)
- [Version Control System](#version-control-system)
- [Configuration](#configuration)
- [Services](#services)
- [Azure Tools](#azure-tools)
- [Logging](#logging)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)

## Overview

The Claims AI Processor is designed to automate the processing of insurance claims by analyzing uploaded documents and making decisions based on business rules. It handles six document types commonly found in insurance claims:

1. Claims Form
2. Discharge Documents
3. Invoices/Bills
4. Receipts
5. Payment Proofs
6. ID Cards

The system uses Azure AI services including Azure Document Intelligence and Azure OpenAI to extract and process information from these documents.

## Architecture

The system follows a modular, version-controlled architecture that enables easy updates and maintenance:

```
Input Documents → Document Classification → OCR Processing → NER Extraction → Rule Engine → Decision Output
```

Each stage is independently versioned and can be updated without affecting other components.

## Project Structure

```
claims-ai-processor/
│
├── config/                          # Configuration files
│   ├── global_versions.yaml         # Global component versions
│   ├── document_versions.yaml       # Per-document version control
│   └── settings.py                  # Configuration loading and management
│
├── document_classifiers/            # Document type classification
│   ├── base_classifier.py           # Abstract base class
│   └── v1/                          # Classifier version 1
│       ├── classifier.py
│       └── prompt.py
│
├── document_processors/             # Document-specific processing logic
│   ├── base_processor.py            # Abstract base class
│   ├── claim_form/                  # Claims form processors
│   │   ├── v1/
│   │   │   ├── processor.py
│   │   │   ├── prompt.py
│   │   │   └── rules.py
│   │   └── v2/
│   │       ├── processor.py
│   │       ├── prompt.py
│   │       └── rules.py
│   ├── discharge/                   # Discharge document processors
│   │   └── v1/
│   │       ├── processor.py
│   │       ├── prompt.py
│   │       └── rules.py
│   ├── invoice/                     # Invoice processors
│   │   ├── v1/
│   │   └── v2/
│   ├── receipt/                     # Receipt processors
│   │   └── v1/
│   ├── payment_proof/               # Payment proof processors
│   │   └── v1/
│   └── id_card/                     # ID card processors
│       └── v1/
│
├── ner_extractors/                  # Named Entity Recognition
│   ├── base_ner.py                  # Abstract base class
│   ├── v1/                          # NER version 1
│   └── v2/                          # NER version 2
│
├── rule_engines/                    # Business rule engines
│   ├── base_rule_engine.py          # Abstract base class
│   ├── rules_2025_q3_v1.py          # Q3 2025 rules
│   └── rules_2025_q4_v1.py          # Q4 2025 rules
│
├── services/                        # Pipeline orchestration
│   ├── ocr_service.py               # OCR processing service
│   ├── ner_service.py               # NER extraction service
│   └── rule_service.py              # Rule checking service
│
├── handlers/                        # Main processing handlers
│   └── claim_processor.py           # End-to-end claim processing
│
├── utils/                           # Utility functions
│   ├── document_classifier_loader.py # Document classifier loader
│   ├── azure_document_intelligence.py # Azure Document Intelligence client
│   ├── openai_client.py             # Azure OpenAI client
│   ├── blob_storage.py              # Azure Blob Storage client
│   └── log_manager.py               # Logging manager with Application Insights
│
├── schemas/                         # Data models and validation
│   ├── ocr_output.py                # OCR output schema
│   ├── ner_output.py                # NER output schema
│   ├── rule_output.py               # Rule engine output schema
│   └── claim_result.py              # Final claim result schema
│
├── tests/                           # Test suite
│   ├── unit/                        # Unit tests
│   └── integration/                 # Integration tests
│
├── main.py                          # Azure Function entry point
├── host.json                        # Azure Functions host configuration
├── function.json                    # Function binding configuration
├── requirements.txt                 # Python dependencies
└── requirements-test.txt            # Test dependencies
```

## Pipeline Stages

### 1. Document Classification

The first stage identifies what type of document each page represents using the document classifier.

**Input:** Raw PDF pages
**Output:** Classified pages with document type labels

### 2. OCR Processing

Processes each document according to its type using specialized processors.

**Input:** Classified document pages
**Output:** Structured JSON data per document type

### 3. NER Extraction

Extracts and standardizes entities across all documents.

**Input:** OCR output from all documents
**Output:** Unified entity data with standardized codes

### 4. Rule Checking

Applies business rules to make a final decision.

**Input:** NER output and policy data from database
**Output:** Final approval/rejection decision

## Version Control System

The system implements a dual-version control approach:

### Global Versions (`config/global_versions.yaml`)

Controls versions of system-wide components:

```yaml
openai_model: "gpt-4o-2025-08-06"
azure_document_intelligence_api_version: "2024-02-29"
document_classifier_version: "v1"
ner_extractor_version: "v2"
rule_engine: "rules_2025_q4_v1"
```

### Document-Specific Versions (`config/document_versions.yaml`)

Controls versions of individual document processors:

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

## Configuration

Configuration files are located in the [config/](config/) directory:

- [global_versions.yaml](config/global_versions.yaml): Controls global component versions
- [document_versions.yaml](config/document_versions.yaml): Controls per-document processing versions
- [settings.py](config/settings.py): Loads and manages configuration values

## Services

The system is organized into independent services that handle different stages of processing:

### OCR Service ([services/ocr_service.py](services/ocr_service.py))

Routes documents to appropriate processors based on type and version, aggregates results.

### NER Service ([services/ner_service.py](services/ner_service.py))

Performs cross-document entity recognition and standardization.

### Rule Service ([services/rule_service.py](services/rule_service.py))

Applies business rules and makes final decisions based on extracted data and policy information.

## Azure Tools

The system provides utility classes for interacting with Azure services:

### Azure Document Intelligence ([utils/azure_document_intelligence.py](utils/azure_document_intelligence.py))

Provides functionality for document analysis using Azure Document Intelligence:

- Document text extraction
- Table and key-value pair extraction
- Support for various prebuilt models

### Azure OpenAI ([utils/openai_client.py](utils/openai_client.py))

Wrapper for Azure OpenAI services:

- Chat completion API
- Structured data extraction from documents
- Document classification

### Azure Blob Storage ([utils/blob_storage.py](utils/blob_storage.py))

Utility for working with Azure Blob Storage:

- Upload and download blobs
- List blobs in containers
- Check blob existence
- Generate SAS URLs for secure access to private blobs

The `generate_sas_url` method allows secure access to blobs without making them publicly accessible. This is especially useful when passing blob URLs to Azure OpenAI for image analysis, as it maintains security while providing temporary access.

## Logging

The system uses [LogManager](utils/log_manager.py) for centralized logging with Azure Application Insights integration:

- Structured logging with custom properties
- Distributed tracing support
- Custom event and metric logging
- Exception tracking

The LogManager provides a singleton instance for consistent logging across the application and sends telemetry data to Azure Application Insights for monitoring and analysis.

## Development

To set up the development environment:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. For testing, also install test dependencies:
   ```bash
   pip install -r requirements-test.txt
   ```

3. Configure environment variables for Azure services:
   - `AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT`
   - `AZURE_DOCUMENT_INTELLIGENCE_KEY`
   - `AZURE_OPENAI_ENDPOINT`
   - `AZURE_OPENAI_KEY`
   - `AZURE_STORAGE_CONNECTION_STRING`
   - `AZURE_STORAGE_ACCOUNT_NAME`
   - `AZURE_STORAGE_ACCOUNT_KEY`
   - `APPLICATIONINSIGHTS_CONNECTION_STRING`
   - `DATABASE_CONNECTION_STRING`

## Testing

The project includes both unit and integration tests:

```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/unit

# Run integration tests only
pytest tests/integration
```

Tests are organized to match the project structure, with unit tests for individual components and integration tests for end-to-end workflows.

## Deployment

The system is designed as an Azure Function app with a blob trigger. Deployment can be done through:

1. Azure Functions Core Tools
2. GitHub Actions CI/CD
3. Azure DevOps Pipelines

The function is triggered when claim documents are uploaded to a designated blob container and outputs structured results to another container.