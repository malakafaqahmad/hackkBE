
from medgemma.medgemmaClient import MedGemmaClient

def finalReporter(patient_id, patient_summary, risk_assessment, functional_capacity, exercise_plan, validation_result):
    final_report_system_prompt = """
<Role>
You are a clinical documentation AI specializing in exercise prescription and lifestyle medicine.
</Role>

<Task>
Generate a professional, structured exercise prescription report using the patient profile, risk assessment, functional capacity, exercise plan, and validation results.
</Task>

<Include the following sections in the report>

1. Patient Summary
   - Demographics (age, sex, height, weight, BMI)
   - Medical conditions
   - Medications affecting exercise
   - Exercise-related symptoms
   - Mobility or functional limitations
   - Current diet summary

2. Risk Assessment
   - Exercise risk level (low, moderate, high)
   - Red flags or contraindications
   - Functional capacity summary

3. Exercise Prescription
   - Aerobic exercises: type, duration, frequency, intensity
   - Strength training: type, duration, frequency, intensity
   - Flexibility exercises
   - Weekly schedule
   - Progression plan

4. Safety Precautions
   - Absolute and relative contraindications
   - Maximum heart rate, blood pressure limits
   - Safety considerations based on diet or clinical concerns

5. Validation Results
   - Safety approval or rejection
   - Violations or concerns
   - Recommendations

6. Follow-Up Plan
   - Reassessment timeline
   - Adjustments for diet or medical conditions
   - Monitoring plan

<Rules>

- Use **only the provided data** from previous agents.
- Maintain **professional, clinically accurate language**.
- Highlight any **risk factors or precautions clearly**.
- Return **text formatted as a report**; JSON output is optional if structured data is needed.
"""

    final_report_user_prompt = f"""
Generate the final professional exercise prescription report.

**Patient Summary:**
{patient_summary}

**Risk Assessment:**
{risk_assessment}

**Functional Capacity:**
{functional_capacity}

**Exercise Plan:**
{exercise_plan}

**Validation Results:**
{validation_result}

Instructions:
- Combine all information into a single, professional report.
- Clearly separate sections: Patient Summary, Risk Assessment, Exercise Prescription, Safety Precautions, Validation Results, Follow-Up Plan.
- Use clinically accurate terminology.
- Emphasize safety, contraindications, and progression instructions.
- Maintain clarity and readability for both clinicians and patients.
- Return the final report as formatted text.
"""
    client = MedGemmaClient(system_prompt=final_report_system_prompt)
    response = client.respond(final_report_user_prompt)
    return response['response']
