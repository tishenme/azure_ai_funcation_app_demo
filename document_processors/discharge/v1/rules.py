# Discharge v1 规则

def validate_discharge(data):
    """
    验证Discharge文档提取的数据
    
    Args:
        data: 从文档中提取的原始数据
        
    Returns:
        验证后的数据
    """
    # 确保诊断代码和过程代码为列表
    for field in ['diagnosis_codes', 'procedure_codes']:
        if data.get(field) is not None:
            if not isinstance(data[field], list):
                data[field] = [data[field]]
        else:
            data[field] = []
    
    return data