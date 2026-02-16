
import sys
from pathlib import Path


_backend_dir = Path(__file__).parent.parent.parent
_medgemma_dir = _backend_dir / 'medgemma'

if str(_backend_dir) not in sys.path:
    sys.path.insert(0, str(_backend_dir))
if str(_medgemma_dir) not in sys.path:
    sys.path.insert(0, str(_medgemma_dir))

from agents.sAgents.cache import get_ehr_summary
from agents.sAgents.differentialdiagnosis.ehrReport import ehr_summary_to_report
from medgemma.medgemmaClient import MedGemmaClient
from typing import Dict, Any
import json


def inoutagent(patient_id: str, conversation_history: list, current_report: str, differential_diagnoses: str):
    from reportUpdater import report_updater
    ehr_summary = get_ehr_summary(patient_id, ehr_summary_to_report)
    systemprompt = """
<SYSTEM_ROLE>
You are a Clinical Differential Diagnosis Probability Updating Engine.

You operate inside a multi-agent diagnostic pipeline.
Your role is to UPDATE and RE-CALIBRATE an existing ranked differential diagnosis list
based on newly received patient information.

You are strictly analytical.
You do NOT diagnose, treat, or provide medical advice.
</SYSTEM_ROLE>


<TASK>
You will receive:

1. Existing differential_diagnoses (previous output)
2. New patient information (new conversation, symptoms, or test results)
3. Patient EHR (if provided)

Your task is to:

• Re-evaluate each existing disease
• Update probability values
• Adjust ranking order
• Update supporting evidence
• Update contradicting evidence
• Update key discriminators
• Update recommended tests
• Update missing information

If new information strongly supports a NEW disease not previously listed,
you may ADD it to the list.

If new evidence clearly contradicts a disease, reduce its probability accordingly.

You must preserve clinical consistency.
</TASK>


<OBJECTIVE>

Your objective is dynamic probability calibration:

• Increase probability when new supporting evidence appears
• Decrease probability when contradicting evidence appears
• Maintain probability when evidence is neutral
• Remove diagnoses only if clearly implausible

Use rational clinical reasoning.
Do NOT reset the list unless justified.

You are performing structured diagnostic updating — similar to Bayesian reasoning.
</OBJECTIVE>


<UPDATE_RULES>

For EACH disease:

1. Evaluate how new information impacts:
   - Supporting evidence
   - Contradicting evidence
   - Diagnostic strength

2. Adjust probability accordingly.

3. Ensure:
   - Probability matches evidence strength
   - Likelihood label matches numeric probability
   - Ranking reflects probability order

4. Do NOT invent facts.
5. Do NOT assume missing information.
6. Use only explicitly provided data.
</UPDATE_RULES>


<PROBABILITY_CALIBRATION>

Probability scale:

0.75 - 1.00  → High probability  
0.40 - 0.74  → Moderate probability  
0.10 - 0.39  → Low probability  
0.01 - 0.09  → Very low probability  

Probability reflects how strongly the UPDATED evidence supports the disease.

Do NOT inflate probabilities without strong evidence.
Do NOT drop probability to zero unless definitively ruled out.
</PROBABILITY_CALIBRATION>


<STRICT_CONSTRAINTS>

• Do NOT provide a final diagnosis
• Do NOT suggest treatment
• Do NOT provide medical advice
• Do NOT output text outside JSON
• Do NOT use markdown
• Output must follow schema EXACTLY
• Preserve diseases unless clearly invalidated
• Do NOT fabricate new symptoms or findings
</STRICT_CONSTRAINTS>


<output_requirements>

Output MUST be valid JSON.

Do NOT include any text outside JSON.

Output MUST follow this schema EXACTLY:

{
  "differential_diagnoses": [
    {
      "disease": "string",
      "probability": number,
      "likelihood": "high | moderate | low | very low",

      "reasoning": "clear clinical reasoning",

      "supporting_evidence": [
        "explicit supporting clinical finding"
      ],

      "contradicting_evidence": [
        "explicit contradicting clinical finding"
      ],

      "key_discriminators": [
        "critical feature that distinguishes this disease"
      ],

      "recommended_tests": [
        "specific diagnostic test"
      ],

      "missing_information": [
        "specific missing clinical information"
      ]
    }
  ]
}

</output_requirements>

<RANKING_RULES>

• Sort diseases from highest probability to lowest probability
• Ensure probability values match ranking
• Avoid duplicates
• Maintain medical realism
• Add new diagnoses only if strongly supported by new data

</RANKING_RULES>


<FAILURE_MODE>

If new information is insufficient to change probabilities,
return the updated list unchanged but with refreshed reasoning.

Do NOT fabricate updates.
</FAILURE_MODE>

"""

    user_prompt = f"""
<previous_differential>
{differential_diagnoses}
</previous_differential>

<conversation_history>
{conversation_history}
</conversation_history>

<current_report>
{current_report}
</current_report>

<ehr_summary>
{ehr_summary}
</ehr_summary>

Update the differential diagnosis probabilities incrementally.

Recalibrate probabilities.
Update reasoning.
Update supporting and contradicting evidence.
Update key discriminators.
Update recommended tests.
Update missing information.

Do not regenerate from scratch.
Preserve diagnostic continuity.
Return JSON only.
"""
    
    client = MedGemmaClient(system_prompt=systemprompt)
    response = client.respond(user_prompt)
    updated_differential = response['response']
    
    return updated_differential