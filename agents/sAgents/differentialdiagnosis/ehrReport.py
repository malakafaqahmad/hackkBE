
import sys
from pathlib import Path
from typing import Dict, Any
from datetime import date, datetime, timedelta

# Add paths for imports
_module_dir = Path(__file__).parent.parent
_manageEhr_dir = _module_dir / 'manageEhr'

if str(_module_dir) not in sys.path:
    sys.path.insert(0, str(_module_dir))
if str(_manageEhr_dir) not in sys.path:
    sys.path.insert(0, str(_manageEhr_dir))

from manageEhr.ehr_manager import EHRManager
from medgemma.medgemmaClient import MedGemmaClient

ehr_manager = EHRManager()


def ehr_summary_to_report(id: str) -> str:
    """
    Converts an EHR summary to a report.
    """
    patientdata = ehr_manager.get_all_patient_ehr_data(id)
    # Get first and last name
    first_name = patientdata['patient']['first_name']
    last_name = patientdata['patient']['last_name']

    # Combine into full name
    full_name = f"{first_name} {last_name}"
    print(f"Retrieved EHR data for patient: {full_name} (ID: {id})")
 

    prompt = f"""

        You are a medical assistant summarizing the EHR (FHIR) records
        for the patient {full_name}.

        Provide a concise summary including:
        - Medical history
        - Existing conditions
        - Medications
        - Relevant past treatments
        - allergies

        Do not include opinions or assumptions.
        Only factual information.

        """
    
    cleint = MedGemmaClient(prompt)
    print("Generating EHR summary report using MedGemma...")
    patientdata = cleint.respond(patientdata)
    print("EHR summary report generated.")
    return patientdata
