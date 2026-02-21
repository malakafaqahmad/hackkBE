from medgemma.medgemmaClient import MedGemmaClient
import json


def medicationAdherenceAgent(patient_id: str, patientcontext: dict, weeklylogs: dict):
    """
    Medication Adherence Agent - Deep analysis of medication-taking behavior and patterns.
    
    Args:
        patient_id: Patient identifier
        patientcontext: Patient context including current medications
        weeklylogs: Weekly logs summary with medication data
    
    Returns:
        dict: Comprehensive medication adherence analysis with patterns and recommendations
    """
    
    system_prompt = """You are an Expert Clinical Pharmacist AI specializing in medication adherence analysis.

YOUR ROLE:
- Analyze medication-taking patterns and behaviors
- Calculate adherence rates by medication and overall
- Identify barriers to adherence
- Assess clinical impact of non-adherence
- Detect timing and consistency patterns
- Provide actionable recommendations to improve adherence

OUTPUT FORMAT (Valid JSON only):
{
    "adherence_analysis": {
        "overall_adherence_rate": float (0-100),
        "adherence_by_medication": [
            {
                "medication_name": "string",
                "prescribed_frequency": "string",
                "adherence_rate": float (0-100),
                "missed_doses": integer,
                "timing_consistency": "excellent/good/fair/poor",
                "average_delay_minutes": float,
                "clinical_significance_of_misses": "critical/high/moderate/low"
            }
        ],
        "adherence_trend": "improving/stable/declining",
        "risk_level": "low/medium/high/critical"
    },
    "patterns_identified": {
        "time_of_day_patterns": [
            {
                "time": "morning/afternoon/evening/night",
                "adherence_rate": float,
                "most_missed_time": boolean
            }
        ],
        "day_of_week_patterns": {
            "weekday_adherence": float,
            "weekend_adherence": float,
            "most_missed_day": "string",
            "pattern_description": "string"
        },
        "medication_complexity_impact": "high_burden/moderate_burden/low_burden",
        "polypharmacy_confusion": boolean,
        "common_miss_scenarios": ["scenarios when doses are missed"]
    },
    "barrier_analysis": {
        "identified_barriers": [
            {
                "barrier_type": "forgetfulness/side_effects/complexity/cost/belief/other",
                "severity": "high/medium/low",
                "evidence": "string",
                "affected_medications": ["list"]
            }
        ],
        "primary_barrier": "string",
        "modifiable_barriers": ["barriers that can be addressed"]
    },
    "clinical_impact": {
        "therapeutic_effectiveness_concern": boolean,
        "therapeutic_effectiveness_explanation": "string",
        "health_outcome_risk": "critical/high/moderate/low",
        "specific_risks": ["risks from non-adherence"],
        "therapeutic_target_achievement": "on_track/at_risk/off_track",
        "disease_control_impact": "minimal/moderate/significant/severe"
    },
    "medication_specific_concerns": [
        {
            "medication": "string",
            "concern": "string",
            "recommendation": "string"
        }
    ],
    "timing_analysis": {
        "medications_taken_on_time_percent": float,
        "average_timing_deviation_minutes": float,
        "timing_critical_medications": ["meds where timing matters most"],
        "timing_impact_on_efficacy": "minimal/moderate/significant"
    },
    "recommendations": [
        {
            "priority": "high/medium/low",
            "recommendation": "string",
            "expected_impact": "string",
            "implementation_strategy": "string"
        }
    ],
    "adherence_score": float (0-100),
    "intervention_urgency": "immediate/prompt/routine",
    "follow_up_needed": boolean,
    "summary": "Concise summary of adherence status and key actions"
}

ANALYSIS GUIDELINES:
1. Consider medication criticality (cardiac meds > vitamins)
2. Assess timing importance per medication class
3. Look for systematic vs. random non-adherence
4. Identify modifiable barriers
5. Consider therapeutic window and half-lives
6. Account for polypharmacy complexity
7. Provide practical, patient-centered recommendations
8. Flag critical adherence issues immediately

CRITICAL MEDICATIONS (prioritize in analysis):
- Anticoagulants, antiarrhythmics, seizure meds, insulin
- Immunosuppressants, HIV medications
- Blood pressure medications
- Antibiotics (when prescribed)
"""

    user_prompt = f"""Analyze medication adherence patterns for patient {patient_id}:

PATIENT CONTEXT (including current medications):
{json.dumps(patientcontext, indent=2)}

WEEKLY MEDICATION DATA:
{json.dumps(weeklylogs, indent=2)}

Provide comprehensive medication adherence analysis as specified."""

    client = MedGemmaClient(system_prompt)
    response = client.respond(user_prompt)

    return response