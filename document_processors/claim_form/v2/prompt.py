# Claim Form v2 提示词

CLAIM_FORM_V2_PROMPT = """
You are an expert insurance claims processor. Extract the following fields from the claim form:

- policy_number: Insurance policy number
- patient_name: Name of the patient
- claim_amount: Total amount claimed
- date_of_service: Date when service was provided
- diagnosis_codes: List of diagnosis codes (ICD-10 format)
- provider_name: Name of healthcare provider
- provider_npi: National Provider Identifier
- claim_submission_date: Date when claim was submitted

Return ONLY a JSON object with these fields. If any field is not present, set it to null.
If diagnosis_codes are present, return them as a JSON array.

Text:
{text}
"""