# Invoice v1 规则

def validate_invoice(data):
    """
    验证Invoice提取的数据
    
    Args:
        data: 从文档中提取的原始数据
        
    Returns:
        验证后的数据
    """
    # 确保金额为数值类型
    if data.get('total_amount') is not None:
        try:
            data['total_amount'] = float(data['total_amount'])
        except (ValueError, TypeError):
            data['total_amount'] = None
    
    # 确保itemized_services为列表
    if data.get('itemized_services') is not None:
        if not isinstance(data['itemized_services'], list):
            data['itemized_services'] = []
    else:
        data['itemized_services'] = []
    
    return data