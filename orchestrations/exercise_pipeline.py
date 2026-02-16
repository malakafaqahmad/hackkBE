from agents.sAgents.exerciseplanner.validation_agent import validationAgent
from agents.sAgents.exerciseplanner.final_reporter import finalReporter
from agents.sAgents.exerciseplanner.exercise_prescriptor import exercisePrescriptorAgent
from agents.sAgents.exerciseplanner.contraindication import contraindicationAgent
from agents.sAgents.exerciseplanner.functional_agent import functionalAgent
from agents.sAgents.exerciseplanner.risk_agent import riskAgent
from agents.sAgents.exerciseplanner.summarizer_first import exerciseAgent

from agents.sAgents.dietplanner.ehr_agent import ehrAgent
from agents.sAgents.cache import get_ehr_summary
from agents.sAgents.differentialdiagnosis.ehrReport import ehr_summary_to_report
import json

def exercisePipeline(patient_id, current_report, current_diet):
        # Step 1: Get EHR summary
    print('ehr_summary fetching')
    ehr_summary = get_ehr_summary(patient_id, ehr_summary_to_report)
    # get patient summary
    print('patient summary fetching')
    patient_summary = ehrAgent(patient_id, ehr_summary, current_report)
    print('patient summary:', patient_summary)

    print('exercise requirements fetching')
    # Step 2: Analyze exercise requirements
    exercise_requirements = exerciseAgent(patient_id, ehr_summary, current_report, current_diet)
    print('exercise requirements:', exercise_requirements)
    # Step 3: Exercise Risk Stratification Agent
    print('exercise risk stratification')
    exercise_risk = riskAgent(patient_id, patient_summary, current_report)
    print('risk stratification:', exercise_risk)

    # functional capacity assessment
    print('functional capacity assessment')
    functional_capacity = functionalAgent(patient_id, patient_summary, exercise_risk)
    print('functional capacity:', functional_capacity)

    # Step 4: Identify contraindications
    print('identifying contraindications')
    contraindications = contraindicationAgent(patient_id, patient_summary, exercise_requirements, exercise_risk, functional_capacity)
    print('contraindications:', contraindications)

    # Step 5: Generate exercise prescription
    print('generating exercise prescription')
    exercise_plan = exercisePrescriptorAgent(patient_id, patient_summary, exercise_requirements, exercise_risk, functional_capacity, contraindications)
    print('exercise plan:', exercise_plan)

    # Step 6: Validate exercise prescription
    print('validating exercise prescription')
    validation = validationAgent(patient_id, patient_summary, exercise_plan, exercise_risk, current_diet, contraindications)
    print('validation result:', validation)

    # Step 7: Generate final report
    print('generating final report')
    final_report = finalReporter(
        patient_id=patient_id,
        patient_summary=patient_summary,
        risk_assessment=exercise_risk,
        functional_capacity=functional_capacity,
        exercise_plan=exercise_plan,
        validation_result=validation
    )
    print('final report:', final_report)
    return final_report


if __name__ == "__main__":
    # ------------------------------
    # TEST CASE: Complete Rest Edge Case
    # ------------------------------

    # Example patient data
    patient_id = "p1"

    # Current clinical report includes acute high-risk condition
    current_report = """
    Patient presents with acute myocarditis confirmed by cardiology.
    Experiencing chest pain at rest and fatigue.
    Vital signs: HR 110 bpm, BP 150/95 mmHg, O2 sat 94%.
    Patient reports dizziness and shortness of breath on minimal exertion.
    """

    # Current diet (can be minimal, as focus is on rest)
    current_diet = """
    Diet Type: Regular diet
    Daily Calories: 1800 kcal
    Meal Pattern: 3 meals/day
    Macronutrient Distribution: Balanced
    Clinical Concerns: Patient reports low energy due to acute illness
    """

    # # Mock function to get EHR summary (replace with real function in production)
    # def get_ehr_summary(patient_id, ehr_summary_to_report):
    #     # Simulate high-risk cardiovascular disease
    #     return """
    # Patient has a history of hypertension and type 2 diabetes.
    # No prior exercise routine. Currently hospitalized due to acute myocarditis.
    # Medications: Beta-blockers, ACE inhibitors.
    # Allergies: None.
    # """

    # Now run the pipeline
    final_report = exercisePipeline(
        patient_id=patient_id,
        current_report=current_report,
        current_diet=current_diet
    )

    # Print the final report for review
    print("\n===== FINAL EXERCISE REPORT =====\n")
    print(final_report)