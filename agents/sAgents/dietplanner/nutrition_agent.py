from medgemma.medgemmaClient import MedGemmaClient
from ..cache import get_ehr_summary
from ..differentialdiagnosis.ehrReport import ehr_summary_to_report
import json



def nutritionAgent(patient_id, patient_summary: str = None):
    patient_summary = get_ehr_summary(patient_id, ehr_summary_to_report)
    nutrition_system_prompt = """
<Role>
You are a clinical nutrition specialist AI responsible for calculating medically appropriate nutritional requirements.
</Role>

<Task>
Calculate daily nutritional requirements based on patient clinical profile and medical conditions.
</Task>

<Considerations>

You must adjust calculations based on:

• Age
• Sex
• BMI
• Chronic diseases
• CKD
• Diabetes
• Hypertension
• Cardiovascular disease
• Malnutrition risk

</Considerations>

<Output Requirements>

Return ONLY valid JSON:

{
  "calories_kcal": number,
  "protein_g": number,
  "carbohydrates_g": number,
  "fat_g": number,
  "sodium_mg": number,
  "potassium_mg": number,
  "fluid_ml": number,
  "diet_type": string,
  "clinical_notes": string
}

No explanations.
"""
    nutrition_user_prompt = f"""
Calculate nutrition requirements for the following patient:

Patient Summary:
{patient_summary}
"""
    client = MedGemmaClient(system_prompt=nutrition_system_prompt)
    
    response = client.respond(nutrition_user_prompt)
    return response['response']


