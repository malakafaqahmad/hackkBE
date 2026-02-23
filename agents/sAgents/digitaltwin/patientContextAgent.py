from medgemma.medgemmaClient import MedGemmaClient
import json

from agents.sAgents.cache import get_ehr_summary
from agents.sAgents.differentialdiagnosis.ehrReport import ehr_summary_to_report
from manageEhr.ehr_manager import EHRManager

ehr_manager = EHRManager()


def pca(patient_id: str):
    """
    Patient Context Agent - Loads and synthesizes comprehensive patient context from EHR.
    
    Args:
        patient_id: Unique identifier for the patient
    
    Returns:
        dict: Comprehensive patient context including demographics, medical history, 
              current medications, allergies, recent labs, vitals, and risk factors
    """
    
    # Load patient EHR data report using cache
    # patient_ehr = get_ehr_summary(patient_id, ehr_summary_to_report)
    patient_ehr = ehr_manager.get_all_patient_ehr_data(patient_id)
    # print(json.dumps(patient_ehr, indent=2))  # Print the EHR data for debugging
    system_prompt = """You are an Expert Clinical Data Synthesizer AI specializing in Electronic Health Records analysis.

YOUR ROLE:
- Extract and organize comprehensive patient context from EHR data
- Identify key clinical risk factors and contraindications
- Synthesize medical history into actionable clinical context
- Provide structured, clinically relevant patient profile

OUTPUT REQUIREMENTS:
Return a valid JSON object with the following structure:
{
    "patient_demographics": {
        "patient_id": "string",
        "name": "string",
        "age": integer,
        "gender": "string",
        "date_of_birth": "YYYY-MM-DD"
    },
    "medical_history": {
        "chronic_conditions": ["condition1", "condition2"],
        "past_diagnoses": [{"diagnosis": "string", "date": "YYYY-MM-DD"}],
        "family_history": ["relevant family conditions"]
    },
    "current_medications": [
        {
            "name": "string",
            "dosage": "string",
            "frequency": "string",
            "prescribed_date": "YYYY-MM-DD",
            "indication": "string"
        }
    ],
    "allergies": [{"allergen": "string", "reaction": "string", "severity": "mild/moderate/severe"}],
    "recent_lab_results": [{"test": "string", "value": "string", "date": "YYYY-MM-DD", "status": "normal/abnormal"}],
    "recent_vitals": {
        "blood_pressure": "systolic/diastolic",
        "heart_rate": integer,
        "temperature": float,
        "weight": float,
        "date": "YYYY-MM-DD"
    },
    "risk_factors": ["diabetes", "hypertension", "smoking", etc.],
    "contraindications": ["specific contraindications"],
    "clinical_summary": "Brief narrative summary of patient's current health status"
}

GUIDELINES:
1. Extract all clinically relevant information from the EHR
2. Identify disease interactions and comorbidities
3. Note medication-disease contraindications
4. Flag critical risk factors
5. Ensure all dates are in YYYY-MM-DD format
6. Return ONLY valid JSON, no markdown or conversational text"""

    user_prompt = f"""Analyze and synthesize the following patient EHR data into a comprehensive patient context:

PATIENT ID: {patient_id}

EHR DATA:
{json.dumps(patient_ehr, indent=2)}

Provide a complete, structured patient context as specified in the output format."""

    client = MedGemmaClient(system_prompt)
    response = client.respond(user_prompt)

    return response

