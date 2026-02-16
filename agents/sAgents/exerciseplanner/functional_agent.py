# Estimate baseline exercise tolerance

from medgemma.medgemmaClient import MedGemmaClient
def functionalAgent(patientid, patient_summary, exercise_risk):
    functional_system_prompt = """
<Role>
You are a clinical functional capacity assessment AI.
</Role>

<Task>
Estimate patient's functional capacity for exercise.
</Task>

<Output JSON>

{
  "baseline_activity_level": "sedentary | light | moderate | active",
  "estimated_mets": number,
  "exercise_tolerance": "low | moderate | high",
  "mobility_limitations": [],
  "functional_risk_notes": string
}
"""
    functional_user_prompt = f"""
Assess functional capacity.

Patient Summary:
{patient_summary}

Risk Assessment:
{exercise_risk}
"""
    
    client = MedGemmaClient(system_prompt=functional_system_prompt)
    response = client.respond(functional_user_prompt)
    return response['response']
