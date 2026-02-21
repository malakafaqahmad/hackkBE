from medgemma.medgemmaClient import MedGemmaClient
import json


def digitalTwinState(patient_id: str, weekly_profile: dict, medication_adherence: dict, 
                    lifestyle_eval: dict, symptoms_analysis: dict, forecast: dict, alerts: dict):
    """
    Digital Twin State Generator - Creates current state snapshot of patient's digital twin.
    
    Args:
        patient_id: Patient identifier
        weekly_profile: Weekly memory profile
        medication_adherence: Medication adherence analysis
        lifestyle_eval: Lifestyle evaluation
        symptoms_analysis: Symptom correlation analysis
        forecast: Health trajectory forecast
        alerts: Generated alerts
    
    Returns:
        dict: Comprehensive current digital twin state
    """
    
    system_prompt = """You are an Expert Digital Twin State Manager AI specializing in health state synthesis and representation.

YOUR ROLE:
- Synthesize all health data into current state snapshot
- Create comprehensive digital representation of patient's health
- Quantify overall health status with scores
- Identify stability and change vectors
- Track state evolution over time
- Provide actionable state summary

OUTPUT FORMAT (Valid JSON only):
{
    "twin_state_timestamp": "YYYY-MM-DD HH:MM:SS",
    "patient_id": "string",
    "state_version": "string (version/iteration number)",
    "current_health_state": {
        "overall_status": "excellent/good/fair/poor/critical",
        "overall_health_score": float (0-100),
        "stability_index": float (0-100),
        "health_trajectory": "significantly_improving/improving/stable/declining/significantly_declining",
        "quality_of_life_estimate": float (0-100),
        "functional_status": "independent/mostly_independent/needs_assistance/dependent"
    },
    "vital_parameters": {
        "medication_adherence_score": float (0-100),
        "lifestyle_score": float (0-100),
        "symptom_burden_score": float (0-100),
        "disease_control_score": float (0-100),
        "vitals_stability_score": float (0-100)
    },
    "health_domains": {
        "cardiovascular": {
            "status": "well_controlled/controlled/poorly_controlled/critical",
            "score": float,
            "key_metrics": {}
        },
        "metabolic": {
            "status": "well_controlled/controlled/poorly_controlled/critical",
            "score": float,
            "key_metrics": {}
        },
        "respiratory": {
            "status": "well_controlled/controlled/poorly_controlled/critical",
            "score": float,
            "key_metrics": {}
        },
        "other_domains": []
    },
    "active_concerns": [
        {
            "concern": "string",
            "severity": "critical/high/moderate/low",
            "status": "new/ongoing/worsening/improving",
            "days_active": integer,
            "action_status": "addressed/pending/monitoring"
        }
    ],
    "positive_indicators": [
        {
            "indicator": "string",
            "achievement_level": "excellent/good/fair",
            "trend": "improving/stable",
            "reinforcement_needed": boolean
        }
    ],
    "risk_profile": {
        "overall_risk_level": "low/moderate/high/critical",
        "short_term_risks": [{"risk": "string", "probability": float}],
        "long_term_risks": [{"risk": "string", "probability": float}],
        "modifiable_risk_factors": ["list"],
        "non_modifiable_risk_factors": ["list"]
    },
    "behavioral_profile": {
        "adherence_pattern": "excellent/good/fair/poor",
        "lifestyle_pattern": "health_promoting/mixed/health_harming",
        "engagement_level": "highly_engaged/engaged/moderately_engaged/disengaged",
        "behavior_change_readiness": "ready/contemplating/not_ready"
    },
    "treatment_response": {
        "current_regimen_effectiveness": float (0-100),
        "therapeutic_targets_status": [
            {
                "target": "string",
                "current_value": "string",
                "target_value": "string",
                "achieved": boolean,
                "trend": "moving_toward/stable/moving_away"
            }
        ],
        "medication_optimization_needed": boolean,
        "lifestyle_intervention_needed": boolean
    },
    "state_changes_from_last": {
        "significant_changes": [
            {
                "parameter": "string",
                "previous_value": "string/number",
                "current_value": "string/number",
                "change_magnitude": "large/moderate/small",
                "clinical_significance": "significant/notable/minor"
            }
        ],
        "trend_direction": "improving/stable/declining",
        "velocity_of_change": "rapid/moderate/slow/stable",
        "notable_events": ["events that occurred since last state"]
    },
    "alert_context": {
        "active_critical_alerts": integer,
        "active_high_alerts": integer,
        "total_active_alerts": integer,
        "requires_immediate_clinical_attention": boolean,
        "top_priority_alerts": ["list of top 3 alerts"]
    },
    "twin_confidence_metrics": {
        "data_completeness": float (0-100),
        "data_quality": float (0-100),
        "prediction_confidence": float (0-100),
        "overall_twin_confidence": float (0-100),
        "confidence_limitations": ["factors affecting confidence"]
    },
    "recent_trajectory": {
        "past_week_summary": "string",
        "past_month_summary": "string",
        "trajectory_consistency": "consistent/variable/erratic"
    },
    "forecast_context": {
        "predicted_next_state": "string",
        "confidence_in_prediction": float,
        "key_factors_influencing_future": ["list"],
        "intervention_opportunities": ["list"]
    },
    "state_summary": "Comprehensive narrative summary of current digital twin state (3-5 sentences)",
    "clinician_priorities": ["Top priorities for clinician review"],
    "patient_guidance": ["Key messages for patient"],
    "next_assessment_recommended": "YYYY-MM-DD"
}

STATE ASSESSMENT GUIDELINES:
1. Integrate all available data sources into cohesive state
2. Calculate weighted scores based on clinical importance
3. Identify both problems and achievements
4. Compare to previous states to show evolution
5. Quantify confidence based on data quality
6. Provide clear, actionable summaries
7. Highlight changes that matter clinically
8. Consider patient's baseline and goals

SCORING METHODOLOGY:
- Overall Health Score: Weighted composite of all domain scores
- Weight critical parameters more heavily (medication adherence, disease control)
- Account for trajectory (declining scores weighted more negatively)
- Factor in symptom burden and quality of life
- Consider forecast risk predictions

STABILITY ASSESSMENT:
- Stable: Consistent metrics, no new concerns, controlled conditions
- Unstable: Variable metrics, new symptoms, worsening trends

TWIN CONFIDENCE:
- High confidence: Complete data, consistent patterns, validated metrics
- Low confidence: Missing data, inconsistent patterns, new diagnosis
"""

    user_prompt = f"""Generate current digital twin state for patient {patient_id}:

WEEKLY PROFILE:
{json.dumps(weekly_profile, indent=2)}

MEDICATION ADHERENCE:
{json.dumps(medication_adherence, indent=2)}

LIFESTYLE EVALUATION:
{json.dumps(lifestyle_eval, indent=2)}

SYMPTOMS ANALYSIS:
{json.dumps(symptoms_analysis, indent=2)}

HEALTH FORECAST:
{json.dumps(forecast, indent=2)}

ACTIVE ALERTS:
{json.dumps(alerts, indent=2)}

Generate comprehensive digital twin state snapshot as specified."""

    client = MedGemmaClient(system_prompt)
    response = client.respond(user_prompt)

    return response