# Receipt v1 提示词

RECEIPT_V1_PROMPT = """
You are an expert payment receipt processor. Extract the following fields from the payment receipt:

- payment_amount: Total amount paid
- payment_date: Date when payment was made
- payment_method: Method of payment (cash, credit card, bank transfer, etc.)
- merchant_name: Name of the merchant or service provider
- transaction_reference: Transaction reference or receipt number
- patient_name: Name of the patient (if present)

Return ONLY a JSON object with these fields. If any field is not present, set it to null.

Text:
{text}
"""