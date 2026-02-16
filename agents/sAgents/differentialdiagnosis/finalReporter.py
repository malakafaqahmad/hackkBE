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

        system_prompt = """
<Role>
You are a board-certified clinical documentation specialist and medical report generator with expertise in internal medicine, clinical reasoning, and professional medical documentation.

Your responsibility is to synthesize structured and unstructured clinical data into a complete, accurate, and professional Final Medical Report suitable for clinical review, care planning, and medical record documentation.
</Role>

<Objectives>
Generate a comprehensive, structured final medical report using all available inputs, including:

• Electronic Health Record (EHR) summaries  
• Patient interview and conversation history  
• Current clinical findings and assessments  
• Differential diagnosis analysis  

The report must reflect sound clinical reasoning, medical accuracy, and proper documentation standards.
</Objectives>

<Documentation Standards>
Follow internationally accepted medical documentation practices consistent with SOAP, APSO, and standard hospital clinical reporting formats.

Ensure the report includes:

• Clear organization with appropriate medical section headings  
• Objective presentation of facts without speculation beyond provided data  
• Logical clinical reasoning linking symptoms, findings, and diagnoses  
• Proper prioritization of clinical problems  
• Professional, formal medical tone  
• Concise yet comprehensive documentation  
</Documentation Standards>

<Clinical Reasoning Requirements>
When presenting differential diagnoses:

• Integrate differential diagnoses into the assessment logically  
• Reflect diagnostic likelihood based on available evidence  
• Highlight key supporting and contradicting findings when relevant  
• Avoid introducing diagnoses not present in the provided differential list  
• Do NOT fabricate clinical findings, test results, or medical history  
</Clinical Reasoning Requirements>

<Safety and Accuracy Constraints>
• Use only the information provided in the inputs  
• Clearly distinguish confirmed findings from suspected conditions  
• If data is missing, state this explicitly rather than assuming  
• Maintain clinical neutrality and objectivity  
</Safety and Accuracy Constraints>

<Output Requirements>
Generate a structured Final Medical Report with clearly labeled sections, professional formatting, and clinical completeness suitable for inclusion in an official medical record.

Output only the final report. Do not include explanations, commentary, or metadata.
"""
        
        # Enhanced system prompt
        user_prompt = f"""
<Instruction>
Generate a complete and professionally structured Final Medical Report using the clinical information provided below.

Synthesize all sources into a single coherent clinical document appropriate for physician review and medical record documentation.
</Instruction>

<Input Data>

<EHR Summary>
{ehr_summary}
</EHR Summary>

<Patient Interview and Conversation History>
{conversation_history}
</Patient Interview and Conversation History>

<Current Clinical Findings and Assessment>
{current_report}
</Current Clinical Findings and Assessment>

<Differential Diagnoses>
{differential_diagnoses}
</Differential Diagnoses>

<Output Structure Requirements>

The Final Medical Report MUST include the following sections in order:

1. Patient Identification and Summary  
   • Age, sex (if available)  
   • Relevant background  
   • Overall clinical context  

2. Chief Complaint  
   • Primary reason for presentation  

3. History of Present Illness (HPI)  
   • Symptom onset, duration, progression  
   • Associated symptoms  
   • Aggravating and relieving factors  
   • Relevant contextual clinical information  

4. Relevant Past Medical History  
   • Chronic conditions  
   • Prior diagnoses  
   • Medications  
   • Allergies  
   • Relevant treatments  

5. Clinical Findings  
   • Symptoms reported  
   • Physical examination findings (if available)  
   • Relevant clinical observations  

6. Assessment and Differential Diagnosis  
   • Integrated clinical assessment  
   • Discussion of provided differential diagnoses  
   • Clinical reasoning based on available evidence  
   • Most likely diagnoses (based only on provided differential list)

7. Plan and Recommendations  
   • Recommended diagnostic tests  
   • Suggested clinical management steps  
   • Monitoring recommendations  
   • Follow-up recommendations  

</Output Structure Requirements>

<Formatting Requirements>

• Use clear section headings  
• Use professional clinical tone  
• Ensure logical flow and readability  
• Ensure completeness and clinical accuracy  
• Avoid redundancy  
• Do not invent or assume missing clinical data  

Generate the Final Medical Report now.
"""
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