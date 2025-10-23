# ID Card v1 提示词

ID_CARD_V1_PROMPT = """
You are an expert identity document processor. Extract the following fields from the ID card:

- patient_name: Full name of the patient
- date_of_birth: Date of birth
- id_number: ID card number
- expiration_date: Expiration date of the ID card
- issuing_authority: Authority that issued the ID card
- address: Address on the ID card

Return ONLY a JSON object with these fields. If any field is not present, set it to null.

Text:
{text}
"""