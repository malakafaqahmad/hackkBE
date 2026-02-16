from agents.sAgents.dietplanner.final_reporter import finalReporter
from agents.sAgents.dietplanner.diet_planner import dietPlanner as generateDietPlan
from agents.sAgents.dietplanner.validation_agent import validationAgent
from agents.sAgents.dietplanner.contraindication_agent import contraindicationAgent
from agents.sAgents.dietplanner.ehr_agent import ehrAgent
from agents.sAgents.dietplanner.nutrition_agent import nutritionAgent
from agents.sAgents.cache import get_ehr_summary
from agents.sAgents.differentialdiagnosis.ehrReport import ehr_summary_to_report
import json


def dietPlanner(patient_id,current_report):
    # Step 1: Get EHR summary
    print('ehr_summary fetching')
    ehr_summary = get_ehr_summary(patient_id, ehr_summary_to_report)
    # get patient summary
    print('patient summary fetching')
    patient_summary = ehrAgent(patient_id, ehr_summary, current_report)
    print('patient summary:', patient_summary)
    print('nutrition requirements fetching')

    # Step 2: Analyze nutrition requirements
    nutrition_requirements = nutritionAgent(patient_id, patient_summary)
    print('nutrition requirements:', nutrition_requirements)
    print('identifying contraindications')

    # Step 3: Identify contraindications
    contraindications = contraindicationAgent(patient_id, patient_summary, nutrition_requirements)
    print('contraindications:', contraindications)
    print('generating diet plan')

    # Step 4: Generate diet plan
    diet_plan = generateDietPlan(patient_id, patient_summary, nutrition_requirements, contraindications)
    print('diet plan:', diet_plan)
    print('validating diet plan')

    # Step 5: Validate diet plan
    validation = validationAgent(patient_id, patient_summary, diet_plan, contraindications)
    print('validation result:', validation)
    print('generating final report')

    # Step 6: Generate final report
    final_report = finalReporter(
        patient_id=patient_id,
        patient_summary=patient_summary,
        nutrition_requirements=nutrition_requirements,
        diet_plan=diet_plan,
        validation=validation
    )
    print('final report:', final_report)
    return final_report


dietPlanner(patient_id='p1', current_report='Patient has diabetes and hypertension.')