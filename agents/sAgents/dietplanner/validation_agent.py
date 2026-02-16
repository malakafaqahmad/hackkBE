from medgemma.medgemmaClient import MedGemmaClient
from ..cache import get_ehr_summary
from ..differentialdiagnosis.ehrReport import ehr_summary_to_report
import json


def validationAgent(patient_id, patient_summary, diet_plan, contraindications):
    validation_system_prompt = """
<Role>
You are a clinical diet safety validation AI.
</Role>

<Task>

Evaluate diet plan for:

• Medical safety
• Contraindications
• Nutritional adequacy
• Clinical appropriateness

</Task>

<Output Format>

Return ONLY JSON:

{
  "is_safe": boolean,
  "violations": [],
  "clinical_concerns": [],
  "approval_status": "approved" | "rejected",
  "recommendations": []
}
"""

    validation_user_prompt = f"""
Validate diet plan safety.

Patient Summary:
{patient_summary}

Diet Plan:
{diet_plan}

Contraindications:
{contraindications}
"""
    client = MedGemmaClient(system_prompt=validation_system_prompt)
    response = client.respond(validation_user_prompt)

    return response
    
