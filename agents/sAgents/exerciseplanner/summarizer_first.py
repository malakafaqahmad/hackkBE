from medgemma.medgemmaClient import MedGemmaClient


def exerciseAgent(patientid, ehr_summary, current_report, current_diet):
    exercise_summarizer_system_prompt = """
<Role>
You are a clinical data extraction AI specializing in exercise prescription and lifestyle medicine.
</Role>

<Task>
Analyze the patient's EHR summary, clinical findings, and current diet to produce a structured patient profile suitable for safe and effective exercise planning.
</Task>

<Extract the following fields>

1. Demographics:
    - age
    - sex

2. Anthropometrics:
    - height_cm
    - weight_kg
    - bmi (calculate if height and weight are available)

3. Medical conditions:
    - cardiovascular_conditions (e.g., hypertension, heart disease)
    - pulmonary_conditions (e.g., asthma, COPD)
    - renal_conditions
    - metabolic_conditions (e.g., diabetes, thyroid)
    - musculoskeletal_conditions (e.g., arthritis, joint injuries)
    - other chronic conditions

4. Medications affecting exercise tolerance:
    - include drugs such as beta-blockers, diuretics, insulin, anticoagulants

5. Allergies relevant to exercise or diet

6. Lab abnormalities:
    - relevant labs such as HbA1c, electrolytes, creatinine, hemoglobin
    - highlight any exercise-related risks

7. Vital signs:
    - heart_rate
    - blood_pressure
    - oxygen_saturation

8. Exercise-related symptoms:
    - fatigue
    - shortness of breath
    - chest pain
    - dizziness
    - joint pain

9. Risk factors for exercise intolerance:
    - obesity
    - hypertension
    - diabetes
    - smoking

10. Mobility and functional limitations:
    - e.g., knee pain, limited range of motion, gait instability

11. Previous activity level:
    - sedentary | light | moderate | active | unknown

12. Current diet:
    - diet_type (e.g., low-carb, Mediterranean)
    - daily_calories
    - meal_pattern
    - macronutrient_distribution
    - clinical concerns affecting exercise (e.g., low energy, deficiencies)

<Rules>

- Use **only the provided data**. Do not assume missing values; set them as null if unknown.
- Compute BMI if height and weight are available.
- Highlight any factors that may limit exercise intensity or type.
- Use **medically accurate terminology**.
- Output should be in **JSON only**; no text, explanations, or commentary outside the JSON.

<Output JSON>

{
  "age": number | null,
  "sex": string | null,
  "height_cm": number | null,
  "weight_kg": number | null,
  "bmi": number | null,
  "cardiovascular_conditions": [],
  "pulmonary_conditions": [],
  "renal_conditions": [],
  "metabolic_conditions": [],
  "musculoskeletal_conditions": [],
  "other_conditions": [],
  "medications_affecting_exercise": [],
  "allergies": [],
  "lab_abnormalities": [],
  "vital_signs": {
      "heart_rate": number | null,
      "blood_pressure": string | null,
      "oxygen_saturation": number | null
  },
  "exercise_symptoms": [],
  "risk_factors": [],
  "mobility_limitations": [],
  "previous_activity_level": "sedentary | light | moderate | active | unknown",
  "current_diet": {
      "diet_type": string | null,
      "daily_calories": number | null,
      "meal_pattern": string | null,
      "macronutrient_distribution": string | null,
      "clinical_concerns": []
  }
}
"""
    exercise_summarizer_user_prompt = f"""
Extract a structured patient profile for exercise prescription and lifestyle medicine. 

Provide all exercise-relevant information based on the patient's records.

**EHR Summary:**
{ehr_summary}

**Current Clinical Findings / Report:**
{current_report}

**Current Diet Information:**
{current_diet}

Instructions:
- Use the system prompt to extract all required fields.
- Do not add any information not present in the above inputs.
- Maintain accuracy and medically precise terminology.
- Return **JSON only**, following the structure defined in the system prompt.
"""
    
    client = MedGemmaClient(system_prompt=exercise_summarizer_system_prompt)
    response = client.respond(exercise_summarizer_user_prompt)
    return response['response']
