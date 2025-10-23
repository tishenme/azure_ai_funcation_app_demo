from schemas.ocr_output import OCROutput
from schemas.ner_output import NEROutput
from config.settings import NER_VERSION

class NERService:
    """
    NER服务，负责实体识别和标准化
    """
    
    def extract_entities(self, ocr_output: OCROutput) -> NEROutput:
        """
        从OCR输出中提取和标准化实体
        
        Args:
            ocr_output: OCR处理结果
            
        Returns:
            NEROutput: NER处理结果
        """
        # 根据配置的版本选择NER处理器
        if NER_VERSION == "v1":
            return self._extract_v1(ocr_output)
        elif NER_VERSION == "v2":
            return self._extract_v2(ocr_output)
        else:
            raise ValueError(f"Unsupported NER version: {NER_VERSION}")
    
    def _extract_v1(self, ocr_output: OCROutput) -> NEROutput:
        """
        V1版本实体提取逻辑
        
        Args:
            ocr_output: OCR处理结果
            
        Returns:
            NEROutput: NER处理结果
        """
        # 从OCR输出中提取信息并合并
        patient_name = None
        policy_number = None
        diagnosis_codes = []
        procedure_codes = []
        total_amount = None
        provider_signature_verified = None
        hospital_name = None
        service_dates = []
        
        # 从claim_form中提取信息（通常只有一份）
        if ocr_output.claim_form:
            patient_name = ocr_output.claim_form.patient_name
            policy_number = ocr_output.claim_form.policy_number
            diagnosis_codes.extend(ocr_output.claim_form.diagnosis_codes)
            total_amount = ocr_output.claim_form.claim_amount
            if ocr_output.claim_form.date_of_service:
                service_dates.append(ocr_output.claim_form.date_of_service)
        
        # 从discharge文档中提取信息（可能有多份）
        if ocr_output.discharge:
            for discharge_doc in ocr_output.discharge:
                if not patient_name and discharge_doc.patient_name:
                    patient_name = discharge_doc.patient_name
                diagnosis_codes.extend(discharge_doc.diagnosis_codes)
                procedure_codes.extend(discharge_doc.procedure_codes)
                if discharge_doc.admission_date and discharge_doc.admission_date not in service_dates:
                    service_dates.append(discharge_doc.admission_date)
                if discharge_doc.discharge_date and discharge_doc.discharge_date not in service_dates:
                    service_dates.append(discharge_doc.discharge_date)
                if not hospital_name and discharge_doc.hospital_name:
                    hospital_name = discharge_doc.hospital_name
        
        # 从invoice文档中提取信息（可能有多份）
        if ocr_output.invoice:
            invoice_total = 0
            for invoice_doc in ocr_output.invoice:
                # 累加所有发票金额
                if invoice_doc.total_amount:
                    invoice_total += invoice_doc.total_amount
                if not hospital_name and invoice_doc.hospital_name:
                    hospital_name = invoice_doc.hospital_name
                if invoice_doc.service_date and invoice_doc.service_date not in service_dates:
                    service_dates.append(invoice_doc.service_date)
            
            # 如果还没有总金额，使用发票总额
            if not total_amount:
                total_amount = invoice_total
        
        # 从receipt文档中提取信息（可能有多份）
        if ocr_output.receipt:
            receipt_total = 0
            for receipt_doc in ocr_output.receipt:
                # 累加所有收据金额
                if receipt_doc.payment_amount:
                    receipt_total += receipt_doc.payment_amount
            
            # 如果还没有总金额，使用收据总额
            if not total_amount:
                total_amount = receipt_total
        
        # 从payment_proof文档中提取信息（可能有多份）
        if ocr_output.payment_proof:
            # 支付证明可以用来验证签名
            provider_signature_verified = True  # 简化处理
        
        # 从id_card文档中提取信息（可能有多份）
        if ocr_output.id_card:
            for id_card_doc in ocr_output.id_card:
                if not patient_name and id_card_doc.patient_name:
                    patient_name = id_card_doc.patient_name
        
        # 创建NER输出
        ner_output = NEROutput(
            policy_number=policy_number,
            patient_name=patient_name,
            diagnosis_codes=list(set(diagnosis_codes)),  # 去重
            procedure_codes=list(set(procedure_codes)),  # 去重
            total_claimed_amount=total_amount,
            provider_signature_verified=provider_signature_verified,
            hospital_name=hospital_name,
            service_dates=service_dates,
            ner_version="v1"
        )
        
        return ner_output
    
    def _extract_v2(self, ocr_output: OCROutput) -> NEROutput:
        """
        V2版本实体提取逻辑（简化示例，实际实现会更复杂）
        
        Args:
            ocr_output: OCR处理结果
            
        Returns:
            NEROutput: NER处理结果
        """
        # 调用v1作为基础
        ner_output = self._extract_v1(ocr_output)
        ner_output.ner_version = "v2"
        
        # V2版本可能添加额外的处理逻辑
        # 例如：诊断代码标准化、更复杂的实体链接等
        
        return ner_output