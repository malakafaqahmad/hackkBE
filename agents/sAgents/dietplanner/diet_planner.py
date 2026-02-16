from medgemma.medgemmaClient import MedGemmaClient
from ..cache import get_ehr_summary
from ..differentialdiagnosis.ehrReport import ehr_summary_to_report
import json



def dietPlanner(patient_id, patient_summary, nutrition_requirements, contraindications):
    diet_system_prompt = """
<Role>
You are a clinical diet planning specialist AI trained in therapeutic nutrition and medical diet planning.
</Role>

<Task>
Generate a medically safe, nutritionally balanced daily diet plan.
</Task>

<Requirements>

The diet must:

• Meet nutritional targets
• Respect contraindications
• Be safe for medical conditions
• Be realistic and practical
• Be balanced nutritionally

</Requirements>

<Output Format>

Return ONLY JSON:

{
  "breakfast": {
    "meal": string,
    "calories": number,
    "protein_g": number
  },
  "lunch": {
    "meal": string,
    "calories": number,
    "protein_g": number
  },
  "dinner": {
    "meal": string,
    "calories": number,
    "protein_g": number
  },
  "snacks": [],
  "total_calories": number,
  "macronutrients": {
    "protein_g": number,
    "carbohydrates_g": number,
    "fat_g": number
  },
  "dietary_notes": string
}
"""
    diet_user_prompt = f"""
Generate personalized diet plan.

Patient Summary:
{patient_summary}

Nutrition Requirements:
{nutrition_requirements}

Contraindications:
{contraindications}
"""
    client = MedGemmaClient(system_prompt=diet_system_prompt)
    response = client.respond(diet_user_prompt)

    return response['response']