# Receipt v1 规则

def validate_receipt(data):
    """
    验证Receipt文档提取的数据
    
    Args:
        data: 从文档中提取的原始数据
        
    Returns:
        验证后的数据
    """
    # 确保金额为数值类型
    if data.get('payment_amount') is not None:
        try:
            data['payment_amount'] = float(data['payment_amount'])
        except (ValueError, TypeError):
            data['payment_amount'] = None
    
    return data