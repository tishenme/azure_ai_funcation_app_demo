# Invoice v1 提示词

INVOICE_V1_PROMPT = """
You are an expert medical billing specialist. Extract the following fields from the medical invoice:

- total_amount: Total amount billed
- hospital_name: Name of the hospital or medical facility
- service_date: Date when service was provided
- itemized_services: List of services with their individual costs
- patient_account_number: Patient account or reference number

Return ONLY a JSON object with these fields. If any field is not present, set it to null.
If itemized_services is present, return it as a JSON array of objects with 'service' and 'cost' properties.

Text:
{text}
"""