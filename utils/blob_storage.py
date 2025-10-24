"""
Azure Blob Storage工具类
用于与Azure Blob Storage服务进行交互
"""
import os
from typing import List, Optional, IO, Any
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from azure.storage.blob import ContentSettings
from datetime import datetime, timedelta
from pathlib import Path

class AzureBlobStorageClient:
    """
    Azure Blob Storage客户端
    提供与Azure Blob Storage服务的交互功能
    """
    
    def __init__(self, connection_string: Optional[str] = None):
        """
        初始化Azure Blob Storage客户端
        
        Args:
            connection_string: 连接字符串，如果为None则从环境变量获取
        """
        if connection_string is None:
            connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
            
        if not connection_string:
            raise ValueError(
                "Missing Azure Storage connection string. "
                "Please set AZURE_STORAGE_CONNECTION_STRING environment variable "
                "or provide connection_string parameter."
            )
        
        self.connection_string = connection_string
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    def get_container_client(self, container_name: str) -> ContainerClient:
        """
        获取容器客户端
        
        Args:
            container_name: 容器名称
            
        Returns:
            ContainerClient实例
        """
        return self.blob_service_client.get_container_client(container_name)
    
    def get_blob_client(self, container_name: str, blob_name: str) -> BlobClient:
        """
        获取Blob客户端
        
        Args:
            container_name: 容器名称
            blob_name: Blob名称
            
        Returns:
            BlobClient实例
        """
        return self.blob_service_client.get_blob_client(
            container=container_name, 
            blob=blob_name
        )
    
    def list_blobs(self, container_name: str, prefix: Optional[str] = None) -> List[str]:
        """
        列出容器中的所有Blob
        
        Args:
            container_name: 容器名称
            prefix: Blob名称前缀（可选）
            
        Returns:
            Blob名称列表
        """
        container_client = self.get_container_client(container_name)
        blobs = container_client.list_blobs(name_starts_with=prefix)
        return [blob.name for blob in blobs]
    
    def download_blob(self, container_name: str, blob_name: str, file_path: str) -> None:
        """
        下载Blob到本地文件
        
        Args:
            container_name: 容器名称
            blob_name: Blob名称
            file_path: 本地文件路径
        """
        blob_client = self.get_blob_client(container_name, blob_name)
        
        # 确保目标目录存在
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, "wb") as f:
            data = blob_client.download_blob()
            data.readinto(f)
    
    def download_blob_to_bytes(self, container_name: str, blob_name: str) -> bytes:
        """
        下载Blob到字节数据
        
        Args:
            container_name: 容器名称
            blob_name: Blob名称
            
        Returns:
            Blob的字节数据
        """
        blob_client = self.get_blob_client(container_name, blob_name)
        return blob_client.download_blob().readall()
    
    def upload_blob(self, container_name: str, blob_name: str, file_path: str) -> None:
        """
        上传本地文件到Blob
        
        Args:
            container_name: 容器名称
            blob_name: Blob名称
            file_path: 本地文件路径
        """
        blob_client = self.get_blob_client(container_name, blob_name)
        
        with open(file_path, "rb") as f:
            blob_client.upload_blob(f, overwrite=True)
    
    def upload_blob_from_bytes(self, container_name: str, blob_name: str, data: bytes, 
                              content_type: Optional[str] = None) -> None:
        """
        从字节数据上传Blob
        
        Args:
            container_name: 容器名称
            blob_name: Blob名称
            data: 字节数据
            content_type: 内容类型（可选）
        """
        blob_client = self.get_blob_client(container_name, blob_name)
        
        # 设置内容类型
        blob_content_settings = None
        if content_type:
            blob_content_settings = ContentSettings(content_type=content_type)
        
        blob_client.upload_blob(data, overwrite=True, content_settings=blob_content_settings)
    
    def blob_exists(self, container_name: str, blob_name: str) -> bool:
        """
        检查Blob是否存在
        
        Args:
            container_name: 容器名称
            blob_name: Blob名称
            
        Returns:
            如果Blob存在返回True，否则返回False
        """
        blob_client = self.get_blob_client(container_name, blob_name)
        try:
            blob_client.get_blob_properties()
            return True
        except Exception:
            return False
    
    def get_blob_url(self, container_name: str, blob_name: str) -> str:
        """
        获取Blob的URL
        
        Args:
            container_name: 容器名称
            blob_name: Blob名称
            
        Returns:
            Blob的URL
        """
        blob_client = self.get_blob_client(container_name, blob_name)
        return blob_client.url
    
    def generate_sas_url(self, container_name: str, blob_name: str, 
                        expiry_hours: int = 1, 
                        permissions: Optional[BlobSasPermissions] = None) -> str:
        """
        生成Blob的SAS URL，用于在没有公共访问权限的情况下安全访问
        
        Args:
            container_name: 容器名称
            blob_name: Blob名称
            expiry_hours: SAS URL过期时间（小时），默认为1小时
            permissions: SAS权限，默认为读权限
            
        Returns:
            带SAS令牌的Blob URL
        """
        if permissions is None:
            permissions = BlobSasPermissions(read=True)
        
        # 获取账户名和账户密钥
        account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
        account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
        
        if not account_name or not account_key:
            # 从连接字符串中提取账户信息
            try:
                parts = dict(part.split('=', 1) for part in self.connection_string.split(';') if '=' in part)
                account_name = parts.get('AccountName')
                account_key = parts.get('AccountKey')
            except Exception:
                raise ValueError(
                    "Unable to extract account information from connection string. "
                    "Please set AZURE_STORAGE_ACCOUNT_NAME and AZURE_STORAGE_ACCOUNT_KEY environment variables."
                )
        
        if not account_name or not account_key:
            raise ValueError(
                "Missing Azure Storage account credentials. "
                "Please set AZURE_STORAGE_ACCOUNT_NAME and AZURE_STORAGE_ACCOUNT_KEY environment variables."
            )
        
        # 生成SAS令牌
        expiry_time = datetime.utcnow() + timedelta(hours=expiry_hours)
        
        sas_token = generate_blob_sas(
            account_name=account_name,
            container_name=container_name,
            blob_name=blob_name,
            account_key=account_key,
            permission=permissions,
            expiry=expiry_time
        )
        
        # 构造带SAS的URL
        blob_url = self.get_blob_url(container_name, blob_name)
        sas_url = f"{blob_url}?{sas_token}"
        
        return sas_url