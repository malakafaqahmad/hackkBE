from medgemma.medgemmaClient import MedGemmaClient

def validationAgent(patientid, patient_summary, exercise_plan, exercise_risk, current_diet, contraindications):
    exercise_validation_system_prompt = """
<Role>
You are a clinical exercise safety validator AI.
</Role>

<Task>
Validate exercise plan against patient risk, functional capacity, and diet.
</Task>

<Output JSON>

{
  "is_safe": boolean,
  "violations": [],
  "clinical_concerns": [],
  "approval_status": "approved | rejected",
  "recommendations": []
}
"""
    exercise_validation_user_prompt = f"""
Validate exercise plan.

Patient Summary:
{patient_summary}

Exercise Plan:
{exercise_plan}

Risk Assessment:
{exercise_risk}

contraindications:
{contraindications}

Current Diet:
{current_diet}
"""
    
    client = MedGemmaClient(system_prompt=exercise_validation_system_prompt)
    response = client.respond(exercise_validation_user_prompt)
    return response['response']