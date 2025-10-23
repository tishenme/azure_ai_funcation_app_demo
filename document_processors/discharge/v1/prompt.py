# Discharge v1 提示词

DISCHARGE_V1_PROMPT = """
You are an expert medical discharge summary processor. Extract the following fields from the discharge document:

- patient_name: Name of the patient
- diagnosis_codes: List of diagnosis codes (ICD-10 format)
- procedure_codes: List of procedure codes
- admission_date: Date when patient was admitted
- discharge_date: Date when patient was discharged
- attending_physician: Name of the attending physician
- hospital_name: Name of the hospital
- discharge_condition: Patient's condition at discharge

Return ONLY a JSON object with these fields. If any field is not present, set it to null.
If diagnosis_codes or procedure_codes are present, return them as JSON arrays.

Text:
{text}
"""