from medgemma.medgemmaClient import MedGemmaClient


def contraindicationAgent(patientid, patient_summary, exercise_requirements, exercise_risk, functional_capacity):
    exercise_contra_system_prompt = """
<Role>
You are a clinical exercise safety AI.
</Role>

<Task>
Identify absolute and relative contraindications for exercise.
</Task>

<Output JSON>

{
  "absolute_contraindications": [],
  "relative_contraindications": [],
  "avoid_exercises": [],
  "recommended_exercises": [],
  "max_heart_rate_bpm": number | null,
  "bp_upper_limit": string | null,
  "clinical_safety_notes": string
}
"""

    exercise_contra_user_prompt = f"""
Identify exercise contraindications.

Patient Summary:
{patient_summary}

Exercise Requirements:
{exercise_requirements}

Risk Assessment:
{exercise_risk}

Functional Capacity:
{functional_capacity}
"""
    
    client = MedGemmaClient(system_prompt=exercise_contra_system_prompt)
    response = client.respond(exercise_contra_user_prompt)
    return response['response']