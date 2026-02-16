
from medgemma.medgemmaClient import MedGemmaClient
from ..cache import get_ehr_summary
from ..differentialdiagnosis.ehrReport import ehr_summary_to_report
import json


def contraindicationAgent(patient_id, patient_summary, nutrition_requirements):
    contra_system_prompt = """
<Role>
You are a clinical diet safety AI responsible for identifying dietary contraindications based on medical conditions, medications, and laboratory findings.
</Role>

<Task>

Identify:

• Foods to avoid
• Foods to limit
• Recommended food categories
• Disease-specific dietary restrictions

</Task>

<Safety Rules>

Consider:

• CKD restrictions
• Diabetes restrictions
• Hypertension restrictions
• Cardiovascular disease
• Medication-food interactions

</Safety Rules>

<Output Format>

Return ONLY JSON:

{
  "avoid_foods": [],
  "limit_foods": [],
  "recommended_foods": [],
  "dietary_pattern": string,
  "safety_notes": string
}
"""

    contra_user_prompt = f"""
Identify dietary contraindications.

Patient Summary:
{patient_summary}

Nutrition Requirements:
{nutrition_requirements}
"""
    
    client = MedGemmaClient(system_prompt=contra_system_prompt)
    response = client.respond(contra_user_prompt)
    return response['response']

