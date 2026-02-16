
from ehrReport import ehr_summary_to_report
from cache import get_ehr_summary
import sys
from pathlib import Path
from typing import Dict, Any
from datetime import date, datetime, timedelta

# Add paths for imports
# Current file: backend/agents/sAgents/ddConversationAgent.py
# Need to get to: backend/

_backend_dir = Path(__file__).parent.parent.parent
_medgemma_dir = _backend_dir / 'medgemma'

if str(_backend_dir) not in sys.path:
    sys.path.insert(0, str(_backend_dir))
if str(_medgemma_dir) not in sys.path:
    sys.path.insert(0, str(_medgemma_dir))

from medgemma.medgemmaClient import MedGemmaClient



def report_updater(patient_id: str, conversation_history: list = None, current_report: str = None) -> str:
    """
    Update the patient report based on the conversation history and the ehrsummary.

    """
    ehrsummary = get_ehr_summary(patient_id, ehr_summary_to_report)


    instructions = f"""<role>
        You are a highly skilled medical assistant with expertise in clinical documentation.
        </role>

        <task>
        Your task is to generate a concise yet clinically comprehensive medical intake report for a Primary Care Physician (PCP). This report will be based on a patient interview and their Electronic Health Record (EHR).
        </task>

        <guiding_principles>
        To ensure the report is both brief and useful, you MUST adhere to the following two principles:

        1.  **Principle of Brevity**:
            * **Use Professional Language**: Rephrase conversational patient language into standard medical terminology (e.g., "it hurts when I breathe deep" becomes "reports pleuritic chest pain").
            * **Omit Filler**: Do not include conversational filler, pleasantries, or repeated phrases from the interview.

        2.  **Principle of Clinical Relevance (What is "Critical Information")**:
            * **Prioritize the HPI**: The History of Present Illness is the most important section. Include key details like onset, duration, quality of symptoms, severity, timing, and modifying factors.
            * **Include "Pertinent Negatives"**: This is critical. You MUST include symptoms the patient **denies** if they are relevant to the chief complaint. For example, if the chief complaint is a cough, denying "fever" or "shortness of breath" is critical information and must be included in the report.
            * **Filter History**: Only include historical EHR data that could reasonably be related to the patient's current complaint. For a cough, a history of asthma or smoking is relevant; a past appendectomy is likely not.
        </guiding_principles>

        <instructions>
        1.  **Primary Objective**: Synthesize the interview and EHR into a clear, organized report, strictly following the <guiding_principles>.
        2.  **Content Focus**:
            * **Main Concern**: State the patient's chief complaint.
            * **Symptoms**: Detail the History of Present Illness, including pertinent negatives.
            * **Relevant History**: Include only relevant information from the EHR.
        3.  **Constraints**:
            * **Factual Information Only**: Report only the facts. No assumptions.
            * **No Diagnosis or Assessment**: Do not provide a diagnosis.
        </instructions>

        <ehr_data>
        <ehr_record_start>
        {ehrsummary}
        <ehr_record_end>
        </ehr_data>

        <output_format>
        The final output MUST be ONLY the full, updated Markdown medical report.
        DO NOT include any introductory phrases, explanations, or any text other than the report itself.
        </output_format>
        <must_not_do>
        Do not add any information that is not explicitly stated in the interview or EHR. Do not make assumptions or inferences beyond the provided data.
        if the user has not answered a question dont not presume an answer. For example, if the user has not answered a question about smoking history, do not include any information about smoking in the report.
        </must_not_do>
    """
    
    # If no existing report is provided, use a default template

    # Construct the user prompt with the specific task and data
    user_prompt = f"""
        <interview_start>
        {conversation_history}
        <interview_end>

        <previous_report>
        {current_report}
        </previous_report>

        <task_instructions>
        Update the report in the `<previous_report>` tags using the new information from the `<interview_start>` section.
        1.  **Integrate New Information**: Add new symptoms or details from the interview into the appropriate sections.
        2.  **Update Existing Information**: If the interview provides more current information, replace outdated details.
        3.  **Maintain Conciseness**: Remove any information that is no longer relevant.
        4.  **Preserve Critical Data**: Do not remove essential historical data (like Hypertension) that could be vital for diagnosis, but ensure it is presented concisely under "Relevant Medical History".
        5.  **Adhere to Section Titles**: Do not change the existing Markdown section titles.
        </task_instructions>

        Now, generate the complete and updated medical report based on all system and user instructions. Your response should be the Markdown text of the report only.
    """

    client = MedGemmaClient(system_prompt=instructions)
    response = client.respond(user_prompt)
    updated_report = response['response']
    
    return updated_report

