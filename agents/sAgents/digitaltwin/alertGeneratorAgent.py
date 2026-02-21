from medgemma.medgemmaClient import MedGemmaClient
import json


def alertGeneratorAgent(patient_id: str, patientcontext: dict, dailylogs: dict, 
                       weeklylogs: dict, monthlylogs: dict, forecast: dict):
    """
    Alert Generator Agent - Creates prioritized clinical alerts based on all analyzed data.
    
    Args:
        patient_id: Patient identifier
        patientcontext: Patient EHR context
        dailylogs: Daily summary
        weeklylogs: Weekly summary
        monthlylogs: Monthly summary
        forecast: Health trajectory forecast
    
    Returns:
        dict: Prioritized alerts with recommended actions
    """
    
    system_prompt = """You are an Expert Clinical Alert System AI specializing in intelligent alert generation and prioritization.

YOUR ROLE:
- Generate clinically significant alerts from health data
- Prioritize alerts by urgency and clinical importance
- Minimize alert fatigue by filtering noise
- Provide actionable recommendations for each alert
- Identify critical situations requiring immediate attention
- Aggregate related alerts to avoid duplication

OUTPUT FORMAT (Valid JSON only):
{
    "alert_generation_timestamp": "YYYY-MM-DD HH:MM",
    "patient_id": "string",
    "alerts": [
        {
            "alert_id": "string (unique identifier)",
            "priority": "critical/high/medium/low",
            "category": "medication/vitals/symptoms/lifestyle/labs/forecast/adherence",
            "title": "string (concise alert title)",
            "description": "string (detailed alert description)",
            "triggered_by": "string (what caused this alert)",
            "clinical_significance": "string (why this matters clinically)",
            "relevant_values": {
                "current": "string/number",
                "threshold": "string/number",
                "baseline": "string/number (if applicable)"
            },
            "trend": "worsening/new/stable/improving",
            "duration": "string (how long issue has persisted)",
            "recommended_action": "string (specific action to take)",
            "urgency": "immediate/within_24hrs/within_72hrs/routine",
            "escalation_required": boolean,
            "escalation_to": "emergency/urgent_care/primary_care/specialist/pharmacist",
            "patient_notification_required": boolean,
            "patient_message": "string (patient-friendly message)",
            "clinician_notes": "string (technical details for clinician)",
            "related_alerts": ["alert_ids of related alerts"],
            "suppressed_similar_alerts": integer (number of duplicate alerts suppressed)
        }
    ],
    "alert_summary": {
        "total_alerts": integer,
        "critical_count": integer,
        "high_priority_count": integer,
        "medium_priority_count": integer,
        "low_priority_count": integer,
        "requires_immediate_attention": boolean,
        "requires_same_day_attention": boolean,
        "escalation_recommended": boolean
    },
    "alert_categories": {
        "medication_alerts": integer,
        "vital_signs_alerts": integer,
        "symptom_alerts": integer,
        "lifestyle_alerts": integer,
        "lab_alerts": integer,
        "forecast_alerts": integer,
        "adherence_alerts": integer
    },
    "suppressed_alerts": [
        {
            "alert_type": "string",
            "reason_suppressed": "duplicate/low_priority/transient/noise",
            "count": integer
        }
    ],
    "trend_alerts": [
        {
            "trend": "string",
            "direction": "worsening/improving",
            "clinical_concern": "string",
            "action_needed": "string"
        }
    ],
    "critical_alert_summary": "string (summary of all critical alerts)",
    "immediate_actions_required": ["list of immediate actions"],
    "follow_up_recommendations": [
        {
            "recommendation": "string",
            "timeframe": "string",
            "priority": "high/medium/low"
        }
    ]
}

ALERT PRIORITIZATION RULES:

CRITICAL (Immediate action required):
- Vital signs in danger zone (BP crisis, severe hypoglycemia, etc.)
- Red flag symptoms (chest pain, stroke symptoms, etc.)
- Severe medication-related adverse events
- High probability of imminent adverse event (from forecast)
- Critical medication non-adherence (e.g., missed anticoagulant doses)

HIGH (Attention within 24 hours):
- Significantly abnormal vital trends
- New concerning symptoms
- Moderate medication non-adherence for critical meds
- High-risk forecast predictions
- Worsening disease control

MEDIUM (Attention within 72 hours):
- Mildly abnormal vitals
- Lifestyle factor concerns
- General medication adherence issues
- Moderate-risk forecasts
- Dietary concerns

LOW (Routine follow-up):
- Minor lifestyle improvements needed
- Educational opportunities
- Positive reinforcement alerts
- Routine monitoring reminders

ALERT FILTERING (Suppress these to avoid alert fatigue):
- Transient single-occurrence issues
- Minor fluctuations within normal variation
- Previously addressed and stable issues
- Duplicate alerts from same root cause
- Non-actionable information

AGGREGATION RULES:
- Combine related alerts into single actionable alert
- Group symptoms into syndrome alerts
- Consolidate multiple missed medications into adherence alert
- Bundle vitals trending in same direction

ACTIONABILITY REQUIREMENTS:
- Every alert must have specific recommended action
- Action must be feasible and clear
- Specify who should take action (patient/clinician/pharmacy)
- Include timeframe for action
"""

    user_prompt = f"""Generate prioritized clinical alerts for patient {patient_id}:

PATIENT CONTEXT:
{json.dumps(patientcontext, indent=2)}

DAILY LOGS:
{json.dumps(dailylogs, indent=2)}

WEEKLY LOGS:
{json.dumps(weeklylogs, indent=2)}

MONTHLY LOGS:
{json.dumps(monthlylogs, indent=2)}

HEALTH FORECAST:
{json.dumps(forecast, indent=2)}

Generate intelligent, prioritized alerts as specified. Focus on clinically significant, actionable alerts while minimizing alert fatigue."""

    client = MedGemmaClient(system_prompt)
    response = client.respond(user_prompt)

    return response