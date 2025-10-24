"""
Azure Document Intelligence工具类
用于与Azure Document Intelligence服务进行交互
"""
import os
from typing import List, Dict, Any
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from config.settings import ADI_API_VERSION

class AzureDocumentIntelligenceClient:
    """
    Azure Document Intelligence客户端
    提供文档分析功能，包括OCR和关键信息提取
    """
    
    def __init__(self):
        """
        初始化Azure Document Intelligence客户端
        从环境变量获取认证信息
        """
        endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
        
        if not endpoint or not key:
            raise ValueError(
                "Missing Azure Document Intelligence credentials. "
                "Please set AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and "
                "AZURE_DOCUMENT_INTELLIGENCE_KEY environment variables."
            )
        
        self.client = DocumentAnalysisClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key),
            api_version=ADI_API_VERSION
        )
    
    def analyze_document(self, document_path: str, model_id: str = "prebuilt-document") -> Dict[str, Any]:
        """
        分析文档内容
        
        Args:
            document_path: 文档文件路径
            model_id: 使用的模型ID，默认为"prebuilt-document"
            
        Returns:
            包含文档分析结果的字典
        """
        with open(document_path, "rb") as f:
            poller = self.client.begin_analyze_document(model_id, f)
            result = poller.result()
            
        return self._format_result(result)
    
    def analyze_document_from_bytes(self, document_bytes: bytes, model_id: str = "prebuilt-document") -> Dict[str, Any]:
        """
        从字节数据分析文档内容
        
        Args:
            document_bytes: 文档文件的字节数据
            model_id: 使用的模型ID，默认为"prebuilt-document"
            
        Returns:
            包含文档分析结果的字典
        """
        poller = self.client.begin_analyze_document(model_id, document_bytes)
        result = poller.result()
        
        return self._format_result(result)
    
    def _format_result(self, result) -> Dict[str, Any]:
        """
        格式化分析结果为标准字典格式
        
        Args:
            result: Azure Document Intelligence分析结果对象
            
        Returns:
            格式化后的结果字典
        """
        formatted_result = {
            "content": result.content,
            "pages": [],
            "tables": [],
            "key_value_pairs": []
        }
        
        # 提取页面信息
        for page in result.pages:
            page_info = {
                "page_number": page.page_number,
                "width": page.width,
                "height": page.height,
                "unit": page.unit,
                "lines": []
            }
            
            # 提取页面中的文本行
            for line in page.lines:
                page_info["lines"].append({
                    "text": line.content,
                    "bounding_box": [(point.x, point.y) for point in line.polygon]
                })
            
            formatted_result["pages"].append(page_info)
        
        # 提取表格信息
        for table in result.tables:
            table_info = {
                "row_count": table.row_count,
                "column_count": table.column_count,
                "cells": []
            }
            
            for cell in table.cells:
                cell_info = {
                    "row_index": cell.row_index,
                    "column_index": cell.column_index,
                    "text": cell.content,
                    "is_header": cell.kind == "columnHeader" if cell.kind else False
                }
                table_info["cells"].append(cell_info)
            
            formatted_result["tables"].append(table_info)
        
        # 提取键值对信息
        if result.key_value_pairs:
            for kv_pair in result.key_value_pairs:
                kv_info = {
                    "key": kv_pair.key.content if kv_pair.key else None,
                    "value": kv_pair.value.content if kv_pair.value else None,
                    "confidence": kv_pair.confidence
                }
                formatted_result["key_value_pairs"].append(kv_info)
        
        return formatted_result
    
    def extract_text(self, document_path: str) -> str:
        """
        从文档中提取纯文本内容
        
        Args:
            document_path: 文档文件路径
            
        Returns:
            提取的纯文本内容
        """
        result = self.analyze_document(document_path, "prebuilt-read")
        return result.get("content", "")
    
    def extract_text_from_bytes(self, document_bytes: bytes) -> str:
        """
        从字节数据中提取纯文本内容
        
        Args:
            document_bytes: 文档文件的字节数据
            
        Returns:
            提取的纯文本内容
        """
        result = self.analyze_document_from_bytes(document_bytes, "prebuilt-read")
        return result.get("content", "")