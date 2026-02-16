import sys
from pathlib import Path
from typing import Dict, Any

# Add paths for imports
# Current file: backend/agents/sAgents/ddConversationAgent.py
# Need to get to: backend/

_backend_dir = Path(__file__).parent.parent.parent
_medgemma_dir = _backend_dir / 'medgemma'
_systemPrompts_dir = _backend_dir / 'systemPrompts'
_sAgents_dir = Path(__file__).parent

if str(_backend_dir) not in sys.path:
    sys.path.insert(0, str(_backend_dir))
if str(_medgemma_dir) not in sys.path:
    sys.path.insert(0, str(_medgemma_dir))
if str(_systemPrompts_dir) not in sys.path:
    sys.path.insert(0, str(_systemPrompts_dir))
if str(_sAgents_dir) not in sys.path:
    sys.path.insert(0, str(_sAgents_dir))

from medgemma.medgemmaClient import MedGemmaClient
from agents.sAgents.cache import get_ehr_summary
from agents.sAgents.differentialdiagnosis.ehrReport import ehr_summary_to_report
from agents.sAgents.differentialdiagnosis.reportUpdater import report_updater


def get_interview_prompt(ehr_summary: str) -> str:
    """Generate the system prompt for the interview agent."""
    return f"""
    SYSTEM INSTRUCTION: Always think silently before responding.

    ### Persona & Objective ###
    You are a clinical assistant. Your objective is to interview a patient, and build a comprehensive and detailed report for their PCP.

        ### Critical Rules ###
        - **No Assessments:** You are NOT authorized to provide medical advice, diagnoses, or express any form of assessment to the patient.
        - **Question Format:** Ask only ONE question at a time. Do not enumerate your questions.
        - **Question Length:** Each question must be 20 words or less.
        - **Question Limit:** You have a maximum of 20 questions.

        ### Interview Strategy ###
        - **Clinical Reasoning:** Based on the patient's responses and EHR, actively consider potential diagnoses.
        - **Differentiate:** Formulate your questions strategically to help differentiate between these possibilities.
        - **Probe Critical Clues:** When a patient's answer reveals a high-yield clue (e.g., recent travel, a key symptom like rapid breathing), ask one or two immediate follow-up questions to explore that clue in detail before moving to a new line of questioning.
        - **Exhaustive Inquiry:** Your goal is to be thorough. Do not end the interview early. Use your full allowance of questions to explore the severity, character, timing, and context of all reported symptoms.
        - **Fact-Finding:** Focus exclusively on gathering specific, objective information.

        ### Context: Patient EHR ###
        You MUST use the following EHR summary to inform and adapt your questioning. Do not ask for information already present here unless you need to clarify it.
        {ehr_summary}
        ### Procedure ###
        1.  **Start Interview:** Begin the conversation with this exact opening: "Thank you for booking an appointment with your primary doctor. I am an assistant here to ask a few questions to help your doctor prepare for your visit. To start, what is your main concern today?"
        2.  **Conduct Interview:** Proceed with your questioning, following all rules and strategies above.
        3.  **End Interview:** You MUST continue the interview until you have asked 20 questions OR the patient is unable to provide more information. When the interview is complete, you MUST conclude by printing this exact phrase: "Thank you for answering my questions. I have everything needed to prepare a report for your visit. End interview."
    """


def interview_message(patient_id: str, user_message: str = None, conversation_history: list = None, conversation_id: str = None, current_report: str = None) -> Dict[str, Any]:
    """
    Handle interview messages - both starting the interview and processing ongoing messages.
    
    Args:
        patient_id: The patient's ID
        user_message: The user's message (optional, if None, starts the interview)
        conversation_history: List of tuples (role, message) representing the conversation (optional)
        conversation_id: The conversation ID from previous messages (optional)
        current_report: The current state of the medical report (optional)
    Returns:
        Dictionary containing:
        - message: The assistant's response
        - updated_report: The updated medical report (None for initial message)
        - patient_id: The patient ID
        - conversation_id: The conversation ID for continuing the chat
    """
    if conversation_history is None:
        conversation_history = []
    
    # Get EHR summary
    print("getting ehr summary at 1st interview")
    ehr_summary = get_ehr_summary(patient_id, ehr_summary_to_report)
    # print("EHR summary retrieved:", ehr_summary)
    
    # Create system prompt
    system_prompt = get_interview_prompt(ehr_summary)
    
    # Initialize client
    client = MedGemmaClient(system_prompt=system_prompt)
    
    # If no user message, start the interview
    if user_message is None:
        initial_response = client.chat("Hello, I need medical consultation.", conversation_id=conversation_id)
        return {
            'message': initial_response['response'],
            'updated_report': None,
            'patient_id': patient_id,
            'conversation_id': initial_response.get('conversation_id', None)
        }
    
    # Otherwise, process the user's message
    print("processing user message in interview")
    response = client.chat(user_message, conversation_id=conversation_id)
    assistant_message = response['response']
    conv_id = response.get('conversation_id', None)

    # Add user message to history first (without assistant response yet)
    updated_history = conversation_history + [('user', user_message)]
    
    
    # Skip report processing for the first user message
    if len(conversation_history) == 0:
        print("\n" + "="*60)
        print("First message - skipping report processing")
        print("="*60)
        return {
            'message': assistant_message,
            'updated_report': None,
            'patient_id': patient_id,
            'conversation_id': conv_id
        }
    
#     # Process report for subsequent messages
#     current_report = """# Medical Intake Report

# ## Chief Complaint
# To be determined from patient interview.

# ## History of Present Illness (HPI)
# To be filled based on patient interview.

# ## Relevant Medical History
# To be extracted from EHR and interview.

# ## Current Medications
# To be extracted from EHR.

# ## Allergies
# To be extracted from EHR.
# """
    
    print("\n" + "="*60)
    print("current report before update:")
    print(current_report)
    print("="*60)

    # Update report with history (before adding assistant message)
    current_report = report_updater(patient_id, updated_history, current_report=current_report)
    
    # Now add assistant message to history after report is updated
    updated_history = updated_history + [('assistant', assistant_message)]
    
    print("\n" + "="*60)
    print("INTERVIEW MESSAGE PROCESSED")
    print(current_report)
    print("="*60)


    
    return {
        'message': assistant_message,
        'updated_report': current_report,
        'patient_id': patient_id,
        'conversation_id': conv_id
    }


