from medgemma.medgemmaClient import MedGemmaClient

def riskAgent(patientid, patient_summary, current_report ):
    exercise_risk_system_prompt = """
<Role>
You are a clinical exercise risk stratification AI.
</Role>

<Task>
Classify exercise risk level based on patient profile.
</Task>

<Output JSON>

{
  "risk_level": "low | moderate | high",
  "requires_medical_clearance": boolean,
  "exercise_intensity_limit": "low | moderate | high | none",
  "red_flags": [],
  "clinical_justification": string
}
"""
    exercise_risk_user_prompt = f"""
Classify exercise risk.

Patient Summary:
{patient_summary}

Current Report:
{current_report}
"""
    client = MedGemmaClient(system_prompt=exercise_risk_system_prompt)
    response = client.respond(exercise_risk_user_prompt)
    return response['response']