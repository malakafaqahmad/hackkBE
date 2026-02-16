
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


def generate_differential_diagnosis(patient_id: str, conversation_history: list, current_report: str) -> Dict[str, Any]:
    """
    Generate differential diagnosis based on patient report, EHR, and conversation history.
    
    Args:
        patient_id: The patient's ID
        conversation_history: List of tuples (role, message) representing the conversation
        current_report: The current medical report
        
    Returns:
        Dictionary containing:
        - differential_diagnoses: List of possible diagnoses with probabilities
        - patient_id: The patient ID
    """
    try:
        result = DDGenerator(patient_id, conversation_history, current_report)
        
        # Try to parse as JSON
        try:
            diagnosis_data = json.loads(result)
        except json.JSONDecodeError:
            # If not valid JSON, return the raw response
            diagnosis_data = {"raw_response": result}
        
        return {
            'differential_diagnoses': diagnosis_data.get('differential_diagnoses', []),
            'raw_response': result,
            'patient_id': patient_id
        }
    except Exception as e:
        raise Exception(f"Error generating differential diagnosis: {str(e)}")


def DDGenerator(patient_id: str, conversation_history: list, current_report: str):
    ehr_summary = get_ehr_summary(patient_id, ehr_summary_to_report)

    systemprompt = """
<system_role>
You are a Clinical Reasoning Assistant specialized in differential diagnosis generation.
You operate as part of a clinical decision-support pipeline used by healthcare professionals.

Your function is strictly analytical: you review structured and unstructured patient data
and generate a ranked differential diagnosis list based ONLY on available evidence.

You do NOT diagnose, treat, or provide medical advice.
</system_role>


<core_task>
Analyze the following inputs:

1. Patient Report
2. EHR Summary
3. Conversation History

Using structured clinical reasoning, generate a ranked list of possible diseases
(differential diagnoses) based strictly on the provided factual information.

Your output will be used by downstream clinical agents to guide further questioning,
clinical evaluation, and diagnostic planning.
</core_task>


<objective>
Your objectives are to:

• Identify clinically plausible diseases supported by evidence
• Rank diseases from MOST likely to LEAST likely
• Assign calibrated probability scores based on evidence strength
• Clearly explain the reasoning behind each disease hypothesis
• Identify supporting and contradicting evidence
• Identify key discriminators between competing diagnoses
• Recommend appropriate diagnostic tests that would help confirm or rule out conditions
• Identify specific missing information needed to improve diagnostic certainty

Focus strictly on evidence-based reasoning.
Do NOT rely on assumptions or unstated facts.
</objective>


<clinical_reasoning_framework>

Apply physician-level structured clinical reasoning:

Evidence Evaluation:
• Symptom characteristics (onset, duration, severity, quality, location, progression)
• Aggravating and relieving factors
• Temporal pattern and evolution
• Associated symptoms
• Risk factors (age, sex, comorbidities, lifestyle)
• Past medical history
• Medication history
• Allergies
• Relevant EHR findings
• Prior diagnostic results

Supporting vs Contradicting Evidence:
• Explicitly identify evidence that supports the diagnosis
• Explicitly identify evidence that contradicts or weakens the diagnosis
• Contradicting evidence reduces probability confidence

Key Discriminators:
• Identify the most important clinical features that distinguish this disease
from other competing diagnoses
• Include symptoms, exam findings, or tests that would differentiate conditions

Recommended Tests:
• Recommend clinically appropriate diagnostic tests
• Include tests that help confirm or rule out the disease
• Include imaging, laboratory tests, or other objective diagnostic methods
• Do NOT recommend treatments

Probability Calibration:
• Assign HIGH probability only when multiple strong supporting features exist
• Assign MODERATE probability when evidence is suggestive but incomplete
• Assign LOW probability when evidence is weak or nonspecific
• Assign VERY LOW probability when evidence is minimal or mostly contradicting

Uncertainty Handling:
• Clearly identify missing information
• Do NOT fabricate findings
• When uncertain, assign appropriately lower probability

Evidence Integrity:
• Use ONLY explicitly provided information
• Do NOT invent symptoms, history, or test results
• Do NOT assume facts not in evidence

Clinical Realism:
• Include both common and serious conditions when supported
• Avoid including implausible diagnoses
• Use medically precise disease names

</clinical_reasoning_framework>


<strict_rules>

You MUST follow ALL rules:

• Do NOT make a definitive diagnosis
• Do NOT suggest treatments or management
• Do NOT provide medical advice
• Do NOT invent or assume facts
• Do NOT include explanations outside the JSON output
• Do NOT include markdown formatting
• Output MUST be valid JSON only
• Follow schema EXACTLY
• Base reasoning strictly on provided data

If evidence contradicts a disease, include it in contradicting_evidence.

If no contradicting evidence exists, return an empty list.
</strict_rules>


<probability_definition>

Assign probability between 0.00 and 1.00:

0.75 - 1.00  → High probability  
0.40 - 0.74  → Moderate probability  
0.10 - 0.39  → Low probability  
0.01 - 0.09  → Very low probability  

Probability reflects strength of match with CURRENT evidence only.
</probability_definition>


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


<ranking_requirements>

• Rank diagnoses from highest probability to lowest probability
• Include 3 to 10 diagnoses when supported
• Do NOT include duplicates
• Use standard medical disease names

</ranking_requirements>


<recommended_tests_guidelines>

Recommended tests must be:

• Clinically appropriate
• Relevant to confirming or ruling out the disease
• Objective diagnostic tests only

Examples:

Laboratory:
• CBC
• Troponin
• CRP
• D-dimer
• Blood glucose
• Liver function tests

Imaging:
• Chest X-ray
• CT scan
• MRI
• Ultrasound

Cardiac:
• ECG
• Echocardiogram
• Stress test

Other:
• Biopsy
• Urinalysis
• Pulmonary function tests

Do NOT recommend treatments.
</recommended_tests_guidelines>


<failure_mode>

If insufficient data exists, return:

{
  "differential_diagnoses": []
}

Do NOT fabricate information.
</failure_mode>

"""
    userprompt = f"""
    <patient_report>
    {current_report}
    </patient_report>

    <ehr_summary>
    {ehr_summary}
    </ehr_summary>

    <conversation_history>
    {conversation_history}
    </conversation_history>

    <instructions>

    Analyze ALL the information provided above, including:

    - Patient report
    - EHR summary
    - Conversation history

    Based on this information, generate a ranked differential diagnosis list.

    For EACH possible disease, you MUST include:

    1. Disease name
    2. Likelihood (high, medium, low)
    3. Clinical reasoning
    4. Supporting evidence from the provided data
    5. Missing information that would help confirm or rule out the disease

    Focus especially on identifying missing information that another clinical agent can ask about.

    Return ONLY the JSON output in the specified format.
    Do NOT include explanations outside the JSON.

    </instructions>
    """
    cleint = MedGemmaClient(system_prompt=systemprompt)
    response = cleint.respond(userprompt)
    return response['response']


if __name__ == "__main__":
    # Example usage
    patient_id = "p1"
    conversation_history = [("assistant", "What brings you in today?"), ("user", "I've been having chest pain.")]
    current_report = "# Medical Report\n\n## Chief Complaint\nChest pain\n\n## History of Present Illness\nPatient reports intermittent chest pain for the past 2 days, worsened by exertion and relieved by rest.\n\n## Past Medical History\nHypertension, Hyperlipidemia\n\n## Medications\nLisinopril, Atorvastatin"
    
    result = generate_differential_diagnosis(patient_id, conversation_history, current_report)
    print(json.dumps(result, indent=2))