"""
签名检测和处理工具类
用于检测文档中的签名并将其保存到Azure Blob Storage
"""
import os
import base64
from typing import List, Optional, Tuple
from azure.storage.blob import ContentSettings
from .azure_document_intelligence import AzureDocumentIntelligenceClient
from .blob_storage import AzureBlobStorageClient
from .log_manager import LogManager
from schemas.ocr_output import SignatureInfo, SignatureType

class SignatureDetector:
    """
    签名检测器
    使用Azure Document Intelligence检测文档中的签名并保存到Blob Storage
    """
    
    def __init__(self):
        """
        初始化签名检测器
        """
        self.document_intelligence_client = AzureDocumentIntelligenceClient()
        self.blob_storage_client = AzureBlobStorageClient()
        self.log_manager = LogManager()
    
    def detect_and_extract_signatures(self, 
                                    document_bytes: bytes, 
                                    container_name: str,
                                    blob_name_prefix: str,
                                    document_type: str) -> List[SignatureInfo]:
        """
        检测并提取文档中的签名
        
        Args:
            document_bytes: 文档的字节数据
            container_name: 用于存储签名图像的Blob容器名称
            blob_name_prefix: 签名图像blob名称前缀
            document_type: 文档类型（用于确定签名类型）
            
        Returns:
            签名信息列表
        """
        self.log_manager.info(f"开始检测文档中的签名: {blob_name_prefix}")
        
        try:
            # 使用Azure Document Intelligence分析文档
            result = self.document_intelligence_client.analyze_document_from_bytes(
                document_bytes, 
                model_id="prebuilt-layout"
            )
            
            signature_infos = []
            
            # 遍历所有页面查找签名
            for page in result.get("pages", []):
                page_number = page.get("page_number", 1)
                page_signatures = self._extract_signatures_from_page(
                    document_bytes, 
                    page, 
                    page_number,
                    document_type
                )
                
                # 保存每个签名到Blob Storage
                for signature_data in page_signatures:
                    signature_bytes, signature_type, confidence = signature_data
                    blob_name = f"{blob_name_prefix}_page{page_number}_{signature_type}_{len(signature_infos)+1}.png"
                    signature_url = self._save_signature_to_blob(
                        signature_bytes, 
                        container_name, 
                        blob_name
                    )
                    
                    signature_info = SignatureInfo(
                        url=signature_url,
                        signature_type=signature_type,
                        confidence=confidence
                    )
                    signature_infos.append(signature_info)
            
            self.log_manager.info(f"成功检测并提取 {len(signature_infos)} 个签名")
            return signature_infos
            
        except Exception as e:
            self.log_manager.error(f"检测签名时发生错误: {str(e)}")
            raise
    
    def _extract_signatures_from_page(self, 
                                    document_bytes: bytes, 
                                    page: dict, 
                                    page_number: int,
                                    document_type: str) -> List[Tuple[bytes, SignatureType, float]]:
        """
        从页面中提取签名图像
        
        Args:
            document_bytes: 文档的字节数据
            page: 页面信息
            page_number: 页码
            document_type: 文档类型
            
        Returns:
            签名数据元组列表 (签名图像字节, 签名类型, 置信度)
        """
        signatures = []
        
        # 在实际实现中，这里会使用更复杂的逻辑来检测签名
        # 例如，基于特定的标记、位置或图像特征
        # 当前实现使用一个简化的示例
        
        # 查找可能的签名区域（示例实现）
        # 在实际应用中，这可能涉及更复杂的图像处理或机器学习模型
        for line in page.get("lines", []):
            # 这是一个简化的示例 - 在实际应用中，您可能需要更复杂的逻辑
            # 比如查找"Signature"关键词附近的图像区域
            text = line["text"].lower()
            if "signature" in text or "签名" in text or "signed" in text:
                # 根据文档类型和上下文推断签名类型
                signature_type = self._infer_signature_type(text, document_type)
                
                # 这里我们模拟找到一个签名区域
                # 在实际实现中，您需要从文档中提取实际的图像数据
                signature_image = self._create_dummy_signature_image()
                signatures.append((signature_image, signature_type, 0.95))
        
        return signatures
    
    def _infer_signature_type(self, text: str, document_type: str) -> SignatureType:
        """
        根据文本内容和文档类型推断签名类型
        
        Args:
            text: 文本内容
            document_type: 文档类型
            
        Returns:
            推断的签名类型
        """
        text = text.lower()
        
        # 根据文本内容推断签名类型
        if any(keyword in text for keyword in ["patient", "患者", "病人"]):
            return SignatureType.PATIENT
        elif any(keyword in text for keyword in ["physician", "doctor", "医生", "医师", "provider", "医疗"]):
            return SignatureType.PROVIDER
        elif any(keyword in text for keyword in ["insured", "被保险人", "投保人"]):
            return SignatureType.INSURED
        elif any(keyword in text for keyword in ["authorized", "授权", "representative", "代表"]):
            return SignatureType.AUTHORIZED
        elif any(keyword in text for keyword in ["witness", "见证", "证人"]):
            return SignatureType.WITNESS
        else:
            # 根据文档类型进行默认推断
            if document_type == "claim_form":
                return SignatureType.PATIENT
            elif document_type == "discharge":
                return SignatureType.PROVIDER
            elif document_type == "invoice":
                return SignatureType.PROVIDER
            elif document_type == "receipt":
                return SignatureType.PATIENT
            elif document_type == "payment_proof":
                return SignatureType.INSURED
            elif document_type == "id_card":
                return SignatureType.UNKNOWN
            else:
                return SignatureType.UNKNOWN
    
    def _save_signature_to_blob(self, 
                              signature_bytes: bytes, 
                              container_name: str, 
                              blob_name: str) -> str:
        """
        将签名图像保存到Blob Storage并生成SAS URL
        
        Args:
            signature_bytes: 签名图像的字节数据
            container_name: Blob容器名称
            blob_name: Blob名称
            
        Returns:
            签名图像的SAS URL
        """
        try:
            # 上传签名图像到Blob Storage
            self.blob_storage_client.upload_blob_from_bytes(
                container_name, 
                blob_name, 
                signature_bytes,
                content_type="image/png"
            )
            
            # 生成SAS URL以便安全访问
            sas_url = self.blob_storage_client.generate_sas_url(
                container_name, 
                blob_name, 
                expiry_hours=24,  # 24小时过期
                permissions="r"   # 只读权限
            )
            
            self.log_manager.info(f"签名已保存到Blob: {blob_name}")
            return sas_url
            
        except Exception as e:
            self.log_manager.error(f"保存签名到Blob时发生错误: {str(e)}")
            raise
    
    def _create_dummy_signature_image(self) -> bytes:
        """
        创建一个虚拟的签名图像（用于演示）
        在实际实现中，这应该是从文档中提取的实际签名图像
        
        Returns:
            虚拟签名图像的字节数据
        """
        # 创建一个简单的PNG图像作为示例
        # 在实际应用中，这应该是从文档中提取的真实签名图像
        dummy_png = (
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
            b"\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\xff\xff?"
            b"\x05\x00\x01\x01\x01\x00\x1f\x9d\xcd\xef\x00\x00\x00\x00IEND\xaeB`\x82"
        )
        return dummy_png