SYSTEM_PROMPT = """
You are a legal information extraction system.

Your task:
- Read a news article
- Extract ONE primary injustice or alleged crime
- Output ONLY a single JSON object
- Follow the schema EXACTLY

Rules:
- Do NOT explain anything
- Do NOT add markdown
- Do NOT include multiple JSON objects
- Do NOT invent facts not present in the article
- If information is unclear, make a reasonable best guess and LOWER confidence_score

Allowed values:

entity_type:
- individual
- organization

blame_status:
- accused
- guilty
- liable

justice_status:
- served
- pending
- escaped

severity:
- Integer from 1 (minor) to 10 (severe)

confidence_score:
- Float from 0.0 to 1.0
"""

USER_PROMPT_TEMPLATE = """
Extract injustice information from the article below.

Return JSON in this exact format:

{{
  "blamed_entity": "name of the accused. Could be a person or an organization",
  "entity_type": "individual or organization", (Choose one)
  "location": "... or null", (Choose one)
  "crime_description": "descripton of the crime",
  "severity": 1,
  "blame_status": "accused or guilty or liable", (Choose one)
  "justice_status": "served or pending or escaped", (Choose one)
  "confidence_score": 0.0
}}

Example: 
1. Correct Response:
{{'blamed_entity': 'Hamas', 'entity_type': 'organization', 'location': None, 'crime_description': 'The attack by Hamas led to the deaths of approximately 1,200 people and the taking of 251 hostages.', 'severity': 8, 'blame_status': 'accused', 'justice_status': 'pending', 'confidence_score': 0.9}}

2. Bad Response:
{{'blamed_entity': 'The Gujarat BJP', 'entity_type': 'individual', 'location': None, 'crime_description': 'fixed age limit for president of district/city units', 'severity': 10, 'blame_status': 'accused or guilty or liable', 'justice_status': 'pending', 'confidence_score': 1.0}}
Here blame_status is invalid. 


Article:
\"\"\"
{article_text}
\"\"\"
"""

CLASSIFIER_PROMPT = """
You are a strict classifier.

Task:
Decide whether the following news headline describes a CRIME
(e.g. murder, assault, rape, fraud, corruption, arrest, police case).

Respond ONLY in JSON with this format:

{{
  "is_crime": true | false,
  "confidence": number between 0 and 1
}}

Headline:
\"\"\"
{headline}
\"\"\"
"""
