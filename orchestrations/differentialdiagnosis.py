import sys
from pathlib import Path

# Add paths for imports
_module_dir = Path(__file__).parent.parent
_manageEhr_dir = _module_dir / 'manageEhr'

if str(_module_dir) not in sys.path:
    sys.path.insert(0, str(_module_dir))
if str(_manageEhr_dir) not in sys.path:
    sys.path.insert(0, str(_manageEhr_dir))

from medgemma.medgemmaClient import MedGemmaClient
from manageEhr.ehr_manager import EHRManager

from agents.sAgents.differentialdiagnosis.secondinterviewer import secondInterviewer
from agents.sAgents.differentialdiagnosis.ehrReport import ehr_summary_to_report
from agents.sAgents.differentialdiagnosis.interviewer import Assistant_Agent
from agents.sAgents.differentialdiagnosis.ddGenerator import DDGenerator
from agents.sAgents.differentialdiagnosis.dPredictor import dPredictor


def run_differential_diagnosis(patient_id):
    """
    Run the complete differential diagnosis workflow for a patient
    
    Args:
        patient_id: The patient identifier
        
    Returns:
        dict: Contains conversation, reports, and diagnosis results
    """
    # Start the interview agent to gather symptoms and update the report
    conv, report = Assistant_Agent(patient_id)
    
    # Run differential diagnosis agent to find top potential diagnoses
    diagnosis = DDGenerator(patient_id, conv, report)
    
    # Conduct second interview with more specific questions
    second_conv, updated_report = secondInterviewer(patient_id, conv, report, diagnosis)
    
    return {
        'conversation': conv,
        'initial_report': report,
        'diagnosis': diagnosis,
        'second_interview': second_conv,
        'updated_report': updated_report
    }


if __name__ == "__main__":
    patient_id = "p1"
    result = run_differential_diagnosis(patient_id)
    print("Predicted Diagnosis:", result['diagnosis'])
    
