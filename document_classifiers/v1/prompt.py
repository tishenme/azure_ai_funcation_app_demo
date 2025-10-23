# 文档分类提示词模板

CLASSIFY_PROMPT = """
You are an expert document classifier for insurance claims processing. 

Please classify the following document text into one of these exact categories:
- "claim_form": Insurance claim form with policy number and claim details
- "discharge": Hospital discharge summary or report
- "invoice": Medical invoice or bill with itemized costs
- "receipt": Payment receipt with transaction details
- "payment_proof": Bank statement or other proof of payment
- "id_card": Patient identification card or document

Text to classify:
{text}

Respond with ONLY the category name in lowercase, nothing else.
"""