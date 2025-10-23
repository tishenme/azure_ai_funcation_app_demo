# Claim Form v1 规则

def validate_claim_form(data):
    """
    验证Claim Form提取的数据
    
    Args:
        data: 从文档中提取的原始数据
        
    Returns:
        验证后的数据
    """
    # 确保金额为数值类型
    if data.get('claim_amount') is not None:
        try:
            data['claim_amount'] = float(data['claim_amount'])
        except (ValueError, TypeError):
            data['claim_amount'] = None
    
    # 确保诊断代码为列表
    if data.get('diagnosis_codes') is not None:
        if not isinstance(data['diagnosis_codes'], list):
            data['diagnosis_codes'] = [data['diagnosis_codes']]
    else:
        data['diagnosis_codes'] = []
    
    return data