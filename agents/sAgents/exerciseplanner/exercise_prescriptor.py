# Estimate baseline exercise tolerance

from medgemma.medgemmaClient import MedGemmaClient
def exercisePrescriptorAgent(patientid, patient_summary, exercise_risk, functional_capacity, exercise_contraindications, current_diet):
    exercise_system_prompt = """
<Role>
You are a clinical exercise prescription AI.
</Role>

<Task>
Generate personalized exercise plan using FITT principle considering risk, functional capacity, and current diet.
</Task>

<Output JSON>

{
  "aerobic": {...},
  "strength_training": {...},
  "flexibility": {...},
  "weekly_schedule": {},
  "progression_plan": "",
  "clinical_notes": ""
}
"""

    exercise_user_prompt = f"""
Generate personalized exercise plan.

Patient Summary:
{patient_summary}

Risk Assessment:
{exercise_risk}

Functional Capacity:
{functional_capacity}

Contraindications:
{exercise_contraindications}

Current Diet:
{current_diet}
"""

    client = MedGemmaClient(system_prompt=exercise_system_prompt)
    response = client.respond(exercise_user_prompt)
    return response['response']