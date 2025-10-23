# Payment Proof v1 提示词

PAYMENT_PROOF_V1_PROMPT = """
You are an expert payment proof processor. Extract the following fields from the payment proof document:

- payer_name: Name of the person or entity making the payment
- payee_name: Name of the person or entity receiving the payment
- payment_amount: Total amount paid
- payment_date: Date when payment was made
- bank_name: Name of the bank (if applicable)
- account_number_last4: Last 4 digits of the account number (if applicable)
- transaction_id: Transaction ID or reference number
- payment_purpose: Purpose or description of the payment

Return ONLY a JSON object with these fields. If any field is not present, set it to null.

Text:
{text}
"""