"""
日志管理器
使用Azure Application Insights进行日志记录和监控
"""
import os
import logging
from typing import Optional, Dict, Any
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure import metrics_exporter
from opencensus.stats import stats, view
from opencensus.trace import config_integration
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer

class LogManager:
    """
    日志管理器类
    提供与Azure Application Insights集成的日志记录功能
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """
        单例模式实现
        """
        if cls._instance is None:
            cls._instance = super(LogManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """
        初始化日志管理器
        """
        if not self._initialized:
            # 获取Application Insights连接字符串
            self.connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
            
            if not self.connection_string:
                raise ValueError(
                    "Missing Application Insights connection string. "
                    "Please set APPLICATIONINSIGHTS_CONNECTION_STRING environment variable."
                )
            
            # 初始化日志记录器
            self.logger = logging.getLogger("claims_ai_processor")
            self.logger.setLevel(logging.INFO)
            
            # 添加Azure日志处理器
            azure_handler = AzureLogHandler(connection_string=self.connection_string)
            self.logger.addHandler(azure_handler)
            
            # 配置追踪集成
            config_integration.trace_integrations(['logging'])
            self.tracer = Tracer(
                exporter=AzureExporter(connection_string=self.connection_string),
                sampler=ProbabilitySampler(1.0)
            )
            
            # 初始化指标导出器
            self.metrics_exporter = metrics_exporter.new_metrics_exporter(
                connection_string=self.connection_string
            )
            
            self._initialized = True
    
    def info(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """
        记录INFO级别日志
        
        Args:
            message: 日志消息
            extra: 额外的日志属性
        """
        self.logger.info(message, extra=extra)
    
    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """
        记录WARNING级别日志
        
        Args:
            message: 日志消息
            extra: 额外的日志属性
        """
        self.logger.warning(message, extra=extra)
    
    def error(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """
        记录ERROR级别日志
        
        Args:
            message: 日志消息
            extra: 额外的日志属性
        """
        self.logger.error(message, extra=extra)
    
    def exception(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """
        记录异常日志
        
        Args:
            message: 日志消息
            extra: 额外的日志属性
        """
        self.logger.exception(message, extra=extra)
    
    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """
        记录DEBUG级别日志
        
        Args:
            message: 日志消息
            extra: 额外的日志属性
        """
        self.logger.debug(message, extra=extra)
    
    def trace_in(self, span_name: str):
        """
        开始一个追踪范围
        
        Args:
            span_name: 追踪范围名称
            
        Returns:
            tracer对象
        """
        return self.tracer.start_span(name=span_name)
    
    def trace_out(self):
        """
        结束当前追踪范围
        """
        self.tracer.end_span()
    
    def log_custom_event(self, event_name: str, properties: Optional[Dict[str, Any]] = None):
        """
        记录自定义事件
        
        Args:
            event_name: 事件名称
            properties: 事件属性
        """
        if properties is None:
            properties = {}
            
        self.logger.info(
            "Custom Event: %s", 
            event_name, 
            extra={
                "custom_dimensions": properties
            }
        )
    
    def log_metric(self, metric_name: str, value: float, properties: Optional[Dict[str, Any]] = None):
        """
        记录指标数据
        
        Args:
            metric_name: 指标名称
            value: 指标值
            properties: 指标属性
        """
        if properties is None:
            properties = {}
            
        # 记录为自定义事件，包含指标值
        properties["metric_value"] = value
        self.log_custom_event(f"Metric: {metric_name}", properties)