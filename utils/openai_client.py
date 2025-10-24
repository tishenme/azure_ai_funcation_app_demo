"""
Azure OpenAI工具类
用于与Azure OpenAI服务进行交互
"""
import os
from typing import Dict, Any, List, Optional
import openai
from azure.identity import DefaultAzureCredential
from config.settings import OPENAI_MODEL

class AzureOpenAIClient:
    """
    Azure OpenAI客户端
    提供与Azure OpenAI服务的交互功能
    支持API密钥和托管身份验证
    """
    
    def __init__(self):
        """
        初始化Azure OpenAI客户端
        支持使用API密钥或托管身份进行身份验证
        """
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        
        if not endpoint:
            raise ValueError(
                "Missing Azure OpenAI endpoint. "
                "Please set AZURE_OPENAI_ENDPOINT environment variable."
            )
        
        # 配置Azure OpenAI客户端
        if os.getenv("AZURE_USE_MANAGED_IDENTITY", "false").lower() == "true":
            # 使用托管身份
            credential = DefaultAzureCredential()
            token = credential.get_token("https://cognitiveservices.azure.com/.default")
            
            self.client = openai.AzureOpenAI(
                azure_endpoint=endpoint,
                azure_ad_token=token.token,
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-29")
            )
        else:
            # 使用API密钥
            key = os.getenv("AZURE_OPENAI_KEY")
            if not key:
                raise ValueError(
                    "Missing Azure OpenAI credentials. "
                    "Please set AZURE_OPENAI_KEY environment variable "
                    "or use managed identity by setting AZURE_USE_MANAGED_IDENTITY=true."
                )
            
            self.client = openai.AzureOpenAI(
                azure_endpoint=endpoint,
                api_key=key,
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-29")
            )
        
        # 默认部署名称（模型）
        self.default_deployment = OPENAI_MODEL
    
    def chat_completion(self, 
                       messages: List[Dict[str, str]], 
                       deployment_name: Optional[str] = None,
                       temperature: float = 0.7,
                       max_tokens: int = 800,
                       **kwargs) -> Dict[str, Any]:
        """
        调用聊天完成API
        
        Args:
            messages: 消息列表，包含角色和内容
            deployment_name: 部署名称（模型），默认使用全局配置
            temperature: 采样温度，控制输出随机性
            max_tokens: 最大生成token数
            **kwargs: 其他参数
            
        Returns:
            API响应结果
        """
        if deployment_name is None:
            deployment_name = self.default_deployment
            
        response = self.client.chat.completions.create(
            model=deployment_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        return {
            "content": response.choices[0].message.content,
            "role": response.choices[0].message.role,
            "finish_reason": response.choices[0].finish_reason,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }
    
    def extract_json_data(self, 
                         prompt: str, 
                         text: str, 
                         deployment_name: Optional[str] = None,
                         temperature: float = 0.3) -> Dict[str, Any]:
        """
        从文本中提取结构化JSON数据
        
        Args:
            prompt: 指导模型如何提取数据的提示
            text: 要处理的文本内容
            deployment_name: 部署名称（模型），默认使用全局配置
            temperature: 采样温度
            
        Returns:
            提取的JSON数据
        """
        full_prompt = f"{prompt}\n\n{text}"
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant that extracts structured data from documents. Respond only with valid JSON."},
            {"role": "user", "content": full_prompt}
        ]
        
        response = self.chat_completion(
            messages=messages,
            deployment_name=deployment_name,
            temperature=temperature
        )
        
        # 在实际应用中，可能需要添加JSON解析和验证逻辑
        return response
    
    def classify_document(self,
                         prompt: str,
                         text: str,
                         deployment_name: Optional[str] = None,
                         temperature: float = 0.1) -> str:
        """
        对文档进行分类
        
        Args:
            prompt: 分类提示
            text: 要分类的文档文本
            deployment_name: 部署名称（模型），默认使用全局配置
            temperature: 采样温度
            
        Returns:
            分类结果
        """
        messages = [
            {"role": "system", "content": "You are an expert document classifier. Respond only with the document type."},
            {"role": "user", "content": f"{prompt}\n\nDocument text:\n{text}"}
        ]
        
        response = self.chat_completion(
            messages=messages,
            deployment_name=deployment_name,
            temperature=temperature
        )
        
        return response["content"].strip()