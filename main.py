import logging
import azure.functions as func
from handlers.claim_processor import ClaimProcessor

def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    
    # 创建索赔处理器实例
    processor = ClaimProcessor()
    
    # 处理索赔
    result = processor.process(myblob.name)
    
    logging.info(f"Processing result: {result}")