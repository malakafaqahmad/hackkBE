import sys
from pathlib import Path
from typing import Dict, Any
from datetime import date, datetime, timedelta
# Add paths for imports
# Current file: be/agents/sAgents/differentialdiagnosis/finalReporter.py
# Need to get to: be/

_backend_dir = Path(__file__).parent.parent.parent.parent
_medgemma_dir = _backend_dir / 'medgemma'
_systemPrompts_dir = _backend_dir / 'systemPrompts'
_sAgents_dir = Path(__file__).parent.parent
_current_dir = Path(__file__).parent

if str(_backend_dir) not in sys.path:
    sys.path.insert(0, str(_backend_dir))
if str(_medgemma_dir) not in sys.path:
    sys.path.insert(0, str(_medgemma_dir))
if str(_systemPrompts_dir) not in sys.path:
    sys.path.insert(0, str(_systemPrompts_dir))
if str(_sAgents_dir) not in sys.path:
    sys.path.insert(0, str(_sAgents_dir))
if str(_current_dir) not in sys.path:
    sys.path.insert(0, str(_current_dir))

from medgemma.medgemmaClient import MedGemmaClient
from cache import get_ehr_summary
from ehrReport import ehr_summary_to_report
import json
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def finalReporter(
    patient_id: str, 
    conversation_history: str, 
    current_report: str, 
    differential_diagnoses: str
) -> Dict[str, Any]:
    """
    Generate the final comprehensive medical report for a patient.
    
    This function synthesizes information from multiple sources including EHR data,
    conversation history, current findings, and differential diagnoses to produce
    a comprehensive final medical report.
    
    Args:
        patient_id: Unique identifier for the patient
        conversation_history: Complete transcript of patient-doctor interactions
        current_report: Current medical findings and observations
        differential_diagnoses: List of potential diagnoses with probabilities
        
    Returns:
        Dict containing:
            - success (bool): Whether the report was generated successfully
            - report (str): The final medical report
            - error (str, optional): Error message if generation failed
            - metadata (dict): Additional information about the report generation
            
    Raises:
        ValueError: If required parameters are missing or invalid
    """
    try:
        # Input validation
        if not patient_id or not isinstance(patient_id, str):
            raise ValueError("patient_id must be a non-empty string")
        
        if not conversation_history:
            logger.warning(f"Empty conversation history for patient {patient_id}")
        
        if not current_report:
            logger.warning(f"Empty current report for patient {patient_id}")
            
        if not differential_diagnoses:
            logger.warning(f"No differential diagnoses provided for patient {patient_id}")
        
        # Retrieve EHR summary
        logger.info(f"Generating final report for patient: {patient_id}")
        ehr_summary = get_ehr_summary(patient_id, ehr_summary_to_report)
        
        if not ehr_summary:
            logger.warning(f"No EHR summary found for patient {patient_id}")
            ehr_summary = "No EHR data available"
        
        # Enhanced system prompt
        system_prompt = """You are an expert medical report generator specializing in creating comprehensive, 
structured clinical documentation. Your role is to synthesize information from multiple sources including 
Electronic Health Records (EHR), patient interviews, physical examinations, and diagnostic assessments 
into a clear, professional final medical report.

Your reports should:
- Follow standard medical documentation format
- Be clear, concise, and professionally written
- Include all relevant clinical information
- Highlight key findings and recommendations
- Use appropriate medical terminology
- Maintain objectivity and clinical accuracy"""

        # Enhanced user prompt with better structure
        user_prompt = f"""Generate a comprehensive final medical report by synthesizing the following information:

**PATIENT EHR SUMMARY:**
{ehr_summary}

**CONVERSATION HISTORY:**
{conversation_history}

**CURRENT CLINICAL FINDINGS:**
{current_report}

**DIFFERENTIAL DIAGNOSES:**
{differential_diagnoses}

Please provide a structured final report that includes:
1. Patient Summary
2. Chief Complaint
3. History of Present Illness
4. Relevant Medical History
5. Clinical Findings
6. Assessment and Differential Diagnoses
7. Plan and Recommendations

Ensure the report is professional, comprehensive, and clinically accurate."""

        # Generate report using MedGemma
        client = MedGemmaClient(system_prompt=system_prompt)
        response = client.respond(user_prompt)
        
        if not response:
            raise Exception("Empty response received from MedGemma")
        
        logger.info(f"Successfully generated final report for patient {patient_id}")
        
        # Return structured response
        return {
            "success": True,
            "report": response,
            "metadata": {
                "patient_id": patient_id,
                "generated_at": datetime.now().isoformat(),
                "has_ehr_data": bool(ehr_summary and ehr_summary != "No EHR data available"),
                "has_conversation": bool(conversation_history),
                "has_differential_diagnoses": bool(differential_diagnoses)
            }
        }
        
    except ValueError as ve:
        logger.error(f"Validation error in finalReporter: {str(ve)}")
        return {
            "success": False,
            "error": f"Validation error: {str(ve)}",
            "report": None
        }
        
    except Exception as e:
        logger.error(f"Error generating final report for patient {patient_id}: {str(e)}", exc_info=True)
        return {
            "success": False,
            "error": f"Failed to generate final report: {str(e)}",
            "report": None
        }