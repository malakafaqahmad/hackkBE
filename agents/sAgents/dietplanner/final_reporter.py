from medgemma.medgemmaClient import MedGemmaClient
from ..cache import get_ehr_summary
from ..differentialdiagnosis.ehrReport import ehr_summary_to_report
import json



def finalReporter(patient_id, patient_summary, nutrition_requirements, diet_plan, validation):
    report_system_prompt = """
<Role>
You are a clinical documentation specialist generating professional diet reports for medical use.
</Role>

<Task>

Generate structured clinical diet report.

</Task>

<Output Structure>

Include:

• Patient summary
• Clinical nutrition assessment
• Diet plan
• Safety assessment
• Recommendations
• Monitoring plan

Use professional clinical tone.

Return structured text report.
"""

    report_user_prompt = f"""
Generate final clinical diet report.

Patient Summary:
{patient_summary}

Nutrition Requirements:
{nutrition_requirements}

Diet Plan:
{diet_plan}

Validation:
{validation}
"""
    
    client = MedGemmaClient(system_prompt=report_system_prompt)
    response = client.chat(report_user_prompt)
    return response
