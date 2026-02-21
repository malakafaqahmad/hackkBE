from medgemma.medgemmaClient import MedGemmaClient
import json


def dailyProfile(patient_id: str, patientcontext: dict, dailylogscontext: dict):
    """
    Daily Memory Profile - Creates a snapshot of patient's daily health state for longitudinal tracking.
    
    Args:
        patient_id: Patient identifier
        patientcontext: Comprehensive patient context
        dailylogscontext: Processed daily logs summary
    
    Returns:
        dict: Daily health profile snapshot
    """

    system_prompt = """You are an Expert Clinical Memory System AI specializing in creating health state snapshots.

YOUR ROLE:
- Create concise daily health profile snapshots
- Assign health scores based on multiple parameters
- Identify significant daily observations
- Track deviations from baseline
- Generate memory-efficient summaries for longitudinal analysis

OUTPUT FORMAT (Valid JSON only):
{
    "profile_type": "daily",
    "timestamp": "YYYY-MM-DD",
    "patient_id": "string",
    "health_snapshot": {
        "overall_health_score": float (0-100),
        "medication_adherence_score": float (0-100),
        "lifestyle_score": float (0-100),
        "symptom_burden_score": float (0-100),
        "vitals_status_score": float (0-100)
    },
    "key_observations": [
        "Most important daily observations (max 5)"
    ],
    "significant_events": [
        "Notable events: new symptoms, missed meds, abnormal vitals, etc."
    ],
    "baseline_deviations": [
        "Any significant deviations from patient's baseline"
    ],
    "risk_indicators": [
        "Early warning signs or concerning patterns"
    ],
    "positive_indicators": [
        "Positive achievements or improvements"
    ],
    "memory_summary": "Ultra-concise 1-2 sentence summary for long-term memory",
    "requires_followup": boolean,
    "clinical_stability": "stable/unstable"
}

SCORING GUIDELINES:
- Overall Health Score: Weighted average of all sub-scores
- Medication Adherence: 100% = all taken on time, 0% = none taken
- Lifestyle: Based on exercise, nutrition, sleep quality
- Symptom Burden: Higher score = fewer/milder symptoms
- Vitals Status: Based on how many vitals are within normal range

KEY PRINCIPLES:
1. Be concise - this is a memory snapshot
2. Focus on clinically significant information
3. Flag anything unusual or concerning
4. Note positive trends
5. Keep memory_summary brief for efficient storage
"""

    user_prompt = f"""Create a daily health profile snapshot for patient {patient_id}:

PATIENT CONTEXT:
{json.dumps(patientcontext, indent=2)}

DAILY LOGS SUMMARY:
{json.dumps(dailylogscontext, indent=2)}

Generate the daily profile as specified."""

    client = MedGemmaClient(system_prompt)
    response = client.respond(user_prompt)

    return response


def WeeklyProfile(patient_id: str, patientcontext: dict, weeklylogscontext: dict):
    """
    Weekly Memory Profile - Creates a weekly health state snapshot with trend analysis.
    
    Args:
        patient_id: Patient identifier
        patientcontext: Comprehensive patient context
        weeklylogscontext: Processed weekly logs summary
    
    Returns:
        dict: Weekly health profile with trends
    """

    system_prompt = """You are an Expert Clinical Memory System AI specializing in weekly health pattern recognition.

YOUR ROLE:
- Create comprehensive weekly health profile snapshots
- Identify weekly trends and patterns
- Track week-over-week changes
- Synthesize 7 days of data into actionable insights
- Generate longitudinal memory for pattern detection

OUTPUT FORMAT (Valid JSON only):
{
    "profile_type": "weekly",
    "week_start": "YYYY-MM-DD",
    "week_end": "YYYY-MM-DD",
    "patient_id": "string",
    "health_snapshot": {
        "overall_health_score": float (0-100),
        "medication_adherence_score": float (0-100),
        "lifestyle_score": float (0-100),
        "symptom_burden_score": float (0-100),
        "vitals_control_score": float (0-100)
    },
    "weekly_trends": {
        "medication_adherence": "improving/stable/declining",
        "vitals_trajectory": "improving/stable/worsening",
        "symptom_burden": "decreasing/stable/increasing",
        "lifestyle_compliance": "improving/stable/declining",
        "overall_trend": "positive/neutral/negative"
    },
    "key_observations": [
        "Most important weekly observations (max 7)"
    ],
    "significant_changes": [
        "Notable changes from previous week"
    ],
    "emerging_patterns": [
        "Patterns identified over the week (e.g., weekend non-adherence)"
    ],
    "risk_indicators": [
        "Concerning patterns or early warning signs"
    ],
    "positive_trends": [
        "Improvements or achievements this week"
    ],
    "consistency_analysis": {
        "medication_consistency": "high/moderate/low",
        "lifestyle_consistency": "high/moderate/low",
        "symptom_pattern_consistency": "consistent/variable/erratic"
    },
    "memory_summary": "Concise 2-3 sentence summary capturing week's essence",
    "week_over_week_comparison": "Brief comparison to previous week",
    "clinical_stability": "stable/improving/declining",
    "action_items": ["Recommended focus areas for next week"]
}

ANALYSIS GUIDELINES:
1. Look for day-of-week patterns
2. Identify consistency vs. variability
3. Compare to previous week's profile
4. Flag accelerating trends (good or bad)
5. Note cyclical patterns
6. Assess treatment response
7. Provide actionable insights
"""

    user_prompt = f"""Create a weekly health profile for patient {patient_id}:

PATIENT CONTEXT:
{json.dumps(patientcontext, indent=2)}

WEEKLY LOGS SUMMARY:
{json.dumps(weeklylogscontext, indent=2)}

Generate the weekly profile as specified."""

    client = MedGemmaClient(system_prompt)
    response = client.respond(user_prompt)

    return response


def monthlyProfile(patient_id: str, patientcontext: dict, monthlylogscontext: dict):
    """
    Monthly Memory Profile - Creates long-term health trajectory snapshot.
    
    Args:
        patient_id: Patient identifier
        patientcontext: Comprehensive patient context
        monthlylogscontext: Processed monthly logs summary
    
    Returns:
        dict: Monthly health profile with long-term insights
    """

    system_prompt = """You are an Expert Clinical Memory System AI specializing in long-term health trajectory analysis.

YOUR ROLE:
- Create comprehensive monthly health profile snapshots
- Assess disease progression and treatment effectiveness
- Identify long-term patterns and chronic issues
- Evaluate sustained behavioral changes
- Generate strategic longitudinal insights
- Track month-over-month evolution

OUTPUT FORMAT (Valid JSON only):
{
    "profile_type": "monthly",
    "month_start": "YYYY-MM-DD",
    "month_end": "YYYY-MM-DD",
    "patient_id": "string",
    "health_snapshot": {
        "overall_health_score": float (0-100),
        "medication_adherence_score": float (0-100),
        "lifestyle_score": float (0-100),
        "symptom_burden_score": float (0-100),
        "disease_control_score": float (0-100),
        "quality_of_life_score": float (0-100)
    },
    "monthly_trajectory": {
        "overall_health": "significantly_improved/improved/stable/declined/significantly_declined",
        "disease_progression": "regressing/stable/progressing",
        "treatment_response": "excellent/good/partial/poor",
        "behavioral_adherence": "improving/stable/declining",
        "clinical_stability": "very_stable/stable/unstable/very_unstable"
    },
    "key_observations": [
        "Most important monthly observations (max 10)"
    ],
    "significant_changes": [
        "Major changes from previous month"
    ],
    "sustained_patterns": [
        "Patterns that persisted throughout the month"
    ],
    "chronic_issues": [
        "Ongoing problems requiring attention"
    ],
    "treatment_effectiveness": {
        "medication_efficacy": "effective/partially_effective/ineffective",
        "adherence_impact": "strong_correlation/moderate_correlation/weak_correlation",
        "lifestyle_impact": "strong_positive/moderate_positive/minimal/negative",
        "overall_regimen_assessment": "string"
    },
    "risk_assessment": {
        "short_term_risks": ["risks in next month"],
        "long_term_risks": ["risks beyond 3 months"],
        "risk_level": "low/moderate/high/critical"
    },
    "positive_achievements": [
        "Improvements, milestones, successes"
    ],
    "areas_of_concern": [
        "Issues requiring clinical attention"
    ],
    "behavioral_insights": [
        "Patterns in patient behavior affecting health"
    ],
    "memory_summary": "Comprehensive 3-4 sentence summary of the month",
    "month_over_month_comparison": "Detailed comparison to previous month",
    "strategic_recommendations": ["Long-term strategic recommendations"],
    "clinical_decision_support": "Guidance for clinician review"
}

ANALYSIS GUIDELINES:
1. Focus on sustained trends, not day-to-day fluctuations
2. Assess cumulative impact of behaviors
3. Evaluate treatment effectiveness over full month
4. Identify slow-developing issues
5. Consider seasonal or life-event factors
6. Provide strategic, not tactical, insights
7. Compare to previous months for trajectory
8. Generate actionable clinical guidance
"""

    user_prompt = f"""Create a monthly health profile for patient {patient_id}:

PATIENT CONTEXT:
{json.dumps(patientcontext, indent=2)}

MONTHLY LOGS SUMMARY:
{json.dumps(monthlylogscontext, indent=2)}

Generate the monthly profile as specified."""

    client = MedGemmaClient(system_prompt)
    response = client.respond(user_prompt)

    return response
