import sys
from pathlib import Path
from typing import Dict, Any
from datetime import date, datetime, timedelta

from agents.sAgents.differentialdiagnosis.dd_inOut import inoutagent
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

from agents.sAgents.cache import get_ehr_summary
from medgemma.medgemmaClient import MedGemmaClient
from agents.sAgents.differentialdiagnosis.ehrReport import ehr_summary_to_report
from agents.sAgents.differentialdiagnosis.reportUpdater import report_updater
import json
import re


def second_interview_message(
    patient_id: str,
    user_message: str = None,
    conversation_history: list = None,
    current_report: str = None,
    differential_diagnoses: str = None,
    conversation_id: str = None
) -> Dict[str, Any]:
    """
    Handle second interview messages - both starting and processing ongoing messages.
    
    Args:
        patient_id: The patient's ID
        user_message: The user's message (optional, if None, starts the interview)
        conversation_history: List of tuples (role, message) representing the conversation
        current_report: The current medical report
        differential_diagnoses: The differential diagnoses JSON
        conversation_id: The conversation ID from previous messages
        
    Returns:
        Dictionary containing:
        - message: The assistant's response
        - updated_report: The updated medical report
        - updated_differential: The updated differential diagnoses
        - patient_id: The patient ID
        - conversation_id: The conversation ID for continuing the chat
    """
    if conversation_history is None:
        conversation_history = []
    
    ehr_summary = get_ehr_summary(patient_id, ehr_summary_to_report)

    second_interviewer_prompt = """
        <role>
        You are an expert clinical interview assistant trained in medical history taking and diagnostic reasoning.
        Your role is to conduct a focused clinical interview to gather missing information needed to narrow down the differential diagnosis.
        you have to keep your tone for the patient friendly and empathetic, but you have to be precise and clinical in your questioning to get the most useful information out of the patient.
        </role>

        <context>
        You will be given:

        1. Differential diagnoses with probabilities
        2. Missing information required to confirm or rule out diseases
        3. Patient EHR summary
        4. Conversation history

        Your job is to ask targeted follow-up questions to obtain the most clinically useful missing information.
        </context>

        <objective>
        Reduce diagnostic uncertainty by asking precise, relevant, and medically appropriate questions.
        Each question must help confirm or rule out high-probability diseases and distinguish between competing diagnoses.
        </objective>

        <rules>
        - Ask ONLY ONE question per response
        - Use clear, simple, patient-friendly language
        - Do NOT repeat previously asked questions
        - Do NOT make conclusions or suggest treatments
        </rules>

        <do not do>
        - you must not ask any question that is already asked earlier in the interview
        </do not do>


        <termination_condition>
        Stop asking questions when sufficient information has been gathered.
        Output:
        enough information to make a confident diagnosis and then your final diagnostic impression
        </termination_condition>
    """

    client = MedGemmaClient(system_prompt=second_interviewer_prompt)
    
    # If no user message, start the second interview
    if user_message is None:
        user_prompt = f"""
            <context>
            <differential_diagnoses>
            {differential_diagnoses}
            </differential_diagnoses>
            <ehr_summary>
            {ehr_summary}
            </ehr_summary>
            {current_report}
            <conversation_history>
            {conversation_history}
            </conversation_history>
            </context>
            <instructions>
            Based on the differential diagnoses and their missing_information fields,
            ask the SINGLE most useful next question to narrow the diagnosis.
            Prioritize:
            1. HIGH probability diseases
            2. Distinguish competing diagnoses
            3. Rule out dangerous conditions
            4. Avoid repeating previous questions
            </instructions>
        """
        print("getting initial question from second interviewer")
        response = client.chat(user_prompt, conversation_id=conversation_id)
        return {
            'message': response['response'],
            'updated_report': current_report,
            'updated_differential': differential_diagnoses,
            'patient_id': patient_id,
            'conversation_id': response.get('conversation_id', None)
        }
    
    # Otherwise, process the user's message
    print("processing user message in second interview")
    response = client.chat(user_message, conversation_id=conversation_id)
    assistant_message = response['response']
    conv_id = response.get('conversation_id', None)
    
    # Update conversation history
    updated_history = conversation_history + [('user', user_message), ('assistant', assistant_message)]
    
    # Update report
    print("updating the report in second interview")
    updated_report = report_updater(patient_id, updated_history, current_report)
    
    # Update differential diagnosis
    print("updating the differential diagnosis in second interview")
    updated_differential = inoutagent(patient_id, updated_history, updated_report, differential_diagnoses)
    
    return {
        'message': assistant_message,
        'updated_report': updated_report,
        'updated_differential': updated_differential,
        'patient_id': patient_id,
        'conversation_id': conv_id
    }





def secondInterviewer(patient_id: str, conversation_history: list, current_report: str, differential_diagnoses: str, conversation_id: str = None):
  ehr_summary = get_ehr_summary(patient_id, ehr_summary_to_report)

  secondInterviewerPrompt = """
        <role>
        You are an expert clinical interview assistant trained in medical history taking and diagnostic reasoning.
        Your role is to conduct a focused clinical interview to gather missing information needed to narrow down the differential diagnosis.
        you have to keep your tone for the patient friendly and empathetic, but you have to be precise and clinical in your questioning to get the most useful information out of the patient.
        </role>

        <context>
        You will be given:

        1. Differential diagnoses with probabilities
        2. Missing information required to confirm or rule out diseases
        3. Patient EHR summary
        4. Conversation history

        Your job is to ask targeted follow-up questions to obtain the most clinically useful missing information.
        </context>

        <objective>
        Reduce diagnostic uncertainty by asking precise, relevant, and medically appropriate questions.
        Each question must help confirm or rule out high-probability diseases and distinguish between competing diagnoses.
        </objective>

        <rules>
        - Ask ONLY ONE question per response
        - Use clear, simple, patient-friendly language
        - Do NOT repeat previously asked questions
        - Do NOT make conclusions or suggest treatments
        </rules>

        <termination_condition>
        Stop asking questions when sufficient information has been gathered.
        Output:
        enough information to make a confident diagnosis and then your final diagnostic impression
        </termination_condition>

        """

  client = MedGemmaClient(system_prompt = secondInterviewerPrompt)
  print("\n" + "="*60)
  print("SECOND INTERVIEWER AGENT STARTED")
  print("="*60)
    
  userprompt = f"""
    <context>
    <differential_diagnoses>
    {differential_diagnoses}
    </differential_diagnoses>
    <ehr_summary>
    {ehr_summary}
    </ehr_summary>
    {current_report}
    <conversation_history>
    {conversation_history}
    </conversation_history>
    </context>
    <instructions>
    Based on the differential diagnoses and their missing_information fields,
    ask the SINGLE most useful next question to narrow the diagnosis.
    Prioritize:
    1. HIGH probability diseases
    2. Distinguish competing diagnoses
    3. Rule out dangerous conditions
    4. Avoid repeating previous questions
    </instructions>
    """
  
  conv = []
    
  # Get initial question
  print("getting initial question from second interviewer")
  response = client.chat(userprompt, conversation_id=conversation_id)
  conversation_id = response.get('conversation_id', conversation_id)
  question_text = response['response']
  
  conv.append(("assistant", question_text))
  
  while True:
    print("\n📝 Second Interviewer Response:")
    print(question_text)
    user = input("user input: ")
    
    if user.lower() in ["exit", "quit"]:
        print("Exiting second interviewer.")
        break
    
    # Add user input to conversation
    conv.append(("user", user))
    
    # Get next response
    response = client.chat(user, conversation_id=conversation_id)
    conversation_id = response.get('conversation_id', conversation_id)
    question_text = response['response']
    
    conv.append(("assistant", question_text))
    
    # Update report
    updated_report = report_updater(patient_id, conv, current_report)

    # update the differential diagnosis with the new information
    updated_differential = inoutagent(patient_id, conv, updated_report, differential_diagnoses)
  

  return conv, updated_report, conversation_id, updated_differential