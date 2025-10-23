# Claim Form v1 提示词

CLAIM_FORM_V1_PROMPT = """
You are an expert insurance claims processor. Extract the following fields from the claim form:

- policy_number: Insurance policy number
- patient_name: Name of the patient
- claim_amount: Total amount claimed
- date_of_service: Date when service was provided
- diagnosis_codes: List of diagnosis codes (ICD-10 format)

Return ONLY a JSON object with these fields. If any field is not present, set it to null.
If diagnosis_codes are present, return them as a JSON array.

Text:
{text}
"""