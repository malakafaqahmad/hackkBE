from medgemma.medgemmaClient import MedGemmaClient
import json


def ehrAgent(patient_id, ehr_summary, current_report):
    ehr_system_prompt = """
<Role>
You are a clinical data extraction and summarization specialist AI trained in medical documentation and clinical reasoning.
</Role>

<Task>
Your task is to analyze patient Electronic Health Records (EHR), laboratory data, and clinical interview information to produce a structured clinical summary for downstream clinical decision-making systems.
</Task>

<Objectives>
Extract and compute the following:

• Demographics (age, sex)
• Anthropometrics (height, weight, BMI)
• Active medical conditions
• Relevant past medical history
• Current medications
• Allergies
• Relevant laboratory abnormalities
• Clinical risk factors
• Dietary restrictions if present

</Objectives>

<Rules>

• Use only the provided data
• Do NOT fabricate or assume missing information
• If data is missing, set value to null
• Compute BMI if height and weight available
• Use medically accurate terminology

</Rules>

<Output Format>
Return ONLY valid JSON in this exact schema:

{
  "age": number | null,
  "sex": string | null,
  "height_cm": number | null,
  "weight_kg": number | null,
  "bmi": number | null,
  "conditions": [],
  "medications": [],
  "allergies": [],
  "lab_abnormalities": [],
  "risk_factors": [],
  "dietary_restrictions": []
}

No explanations. JSON only.
"""

    ehr_user_prompt = f"""
Extract structured clinical summary from the following patient data:

EHR Summary:
{ehr_summary}

Clinical Findings:
{current_report}
"""
    
    client = MedGemmaClient(system_prompt=ehr_system_prompt)
    response = client.respond(ehr_user_prompt)
    return response['response']

