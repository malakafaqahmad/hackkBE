import sys
from pathlib import Path
from typing import Dict, Any
from datetime import date, datetime, timedelta
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
from cache import get_ehr_summary
from ehrReport import ehr_summary_to_report
import json
import re

def dPredictor(patient_id: str, conversation_history: str, current_report: str):
  
    # differential diagnosis agent that predicts the top 1 most likely diagnosis 
    # or it shows what more shall be there like tests or xrays etc and updates that to final report
    ehr_summary = get_ehr_summary(patient_id, ehr_summary_to_report)

    system_prompt = """
You are a top-tier clinical differential diagnosis agent.

Your job:
1. Predict the SINGLE most likely diagnosis.
2. If insufficient information is present, suggest the most important missing test.
3. Consider EHR risk factors, labs, imaging, and conversation history.
4. Be medically precise and concise.
5. Do not list multiple diagnoses.

Return strictly valid JSON.
"""
    user_prompt = f"""
<current_report>
{current_report}
</current_report>
<conversation_history>
{conversation_history}
</conversation_history>
<ehr_summary>
{ehr_summary}
</ehr_summary>
Based on the above information, predict the single most likely diagnosis for the patient.

Return your answer in the following JSON format:
{{
    "predicted_diagnosis": "Your predicted diagnosis here",
    "confidence": "Your confidence level here (e.g., high, medium, low)",
    "rationale": "Brief explanation of why you made this prediction"
}}
"""

    client = MedGemmaClient(system_prompt=system_prompt)
    response = client.respond(user_prompt)
    
    return response
