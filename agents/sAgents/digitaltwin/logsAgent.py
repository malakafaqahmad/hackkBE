from medgemma.medgemmaClient import MedGemmaClient
import json

'''
This will create an overall summary of the logs of the agents 
time aware agent

miss ratio of medication
exercises if any "exercise_minutes": int(exercise_minutes),

diet alignments with medications
"vitals": summary generator
"labs": if any
"symptoms": symptoms

'''

def dailylogsAgent(patient_id: str, patientcontext: dict, dailylogs: dict):
    """
    Daily Logs Agent - Analyzes and summarizes a single day's health data.
    
    Args:
        patient_id: Patient identifier
        patientcontext: Comprehensive patient context from pca
        dailylogs: Single day's logs including meds, vitals, symptoms, exercise, nutrition
    
    Returns:
        dict: Structured daily summary with adherence, vitals, symptoms, exercise, nutrition analysis
    """

    system_prompt = """You are an Expert Clinical Daily Monitoring AI specializing in patient health data analysis.

YOUR ROLE:
- Analyze single-day patient health logs comprehensively
- Calculate medication adherence with precision
- Assess vital signs for clinical significance
- Evaluate symptom severity and urgency
- Analyze exercise compliance
- Review nutritional adherence to dietary requirements
- Identify any concerning patterns or deviations

OUTPUT FORMAT (Valid JSON only):
{
    "date": "YYYY-MM-DD",
    "medication_adherence": {
        "total_prescribed": integer,
        "total_taken": integer,
        "missed": integer,
        "adherence_rate_percent": float,
        "missed_medications": [{"name": "string", "prescribed_time": "string"}],
        "timing_accuracy": "excellent/good/fair/poor"
    },
    "vitals_summary": {
        "blood_pressure": {
            "systolic": integer,
            "diastolic": integer,
            "status": "normal/elevated/stage1_hypertension/stage2_hypertension/crisis"
        },
        "heart_rate": {
            "bpm": integer,
            "status": "normal/bradycardia/tachycardia"
        },
        "blood_glucose": {
            "value_mg_dl": float,
            "status": "in_range/hypoglycemia/hyperglycemia"
        },
        "temperature": {
            "value_f": float,
            "status": "normal/fever/hypothermia"
        },
        "weight_lbs": float,
        "oxygen_saturation": integer,
        "alerts": ["list of vital sign concerns"]
    },
    "symptoms_reported": [
        {
            "symptom": "string",
            "severity": "mild/moderate/severe",
            "time_reported": "HH:MM",
            "requires_attention": boolean
        }
    ],
    "exercise_completed": boolean,
    "exercise_details": {
        "minutes": integer,
        "type": "string",
        "intensity": "low/moderate/high",
        "meets_goal": boolean
    },
    "nutrition_summary": {
        "diet_adherence": "excellent/good/fair/poor",
        "total_calories": float,
        "sodium_g": float,
        "sugar_g": float,
        "dietary_concerns": ["concerns related to patient conditions"],
        "medication_food_interactions": ["any interactions noted"]
    },
    "overall_day_status": "excellent/good/concerning/critical",
    "key_observations": ["important clinical notes"],
    "requires_immediate_attention": boolean
}

ANALYSIS GUIDELINES:
1. Cross-reference medications with patient's conditions
2. Check vital signs against patient's baseline and clinical norms
3. Identify medication-food interactions
4. Flag symptoms that may indicate complications
5. Assess exercise appropriateness for patient's conditions
6. Consider dietary requirements based on medications and conditions
7. Note any deviations from expected patterns
"""

    user_prompt = f"""Analyze the following daily health logs for patient {patient_id}:

PATIENT CONTEXT:
{json.dumps(patientcontext, indent=2)}

DAILY LOGS:
{json.dumps(dailylogs, indent=2)}

Provide comprehensive daily analysis as specified."""

    client = MedGemmaClient(system_prompt)
    response = client.respond(user_prompt)

    return response


def weeklylogsAgent(patient_id: str, patientcontext: dict, weeklylogs: list):
    """
    Weekly Logs Agent - Analyzes trends and patterns over a week.
    
    Args:
        patient_id: Patient identifier
        patientcontext: Comprehensive patient context
        weeklylogs: List of 7 daily log summaries
        previousweeklylogs: Previous week's daily logs for comparison
    
    Returns:
        dict: Weekly trends, patterns, and comparisons
    """

    system_prompt = """You are an Expert Clinical Trend Analysis AI specializing in weekly health pattern recognition.

YOUR ROLE:
- Identify weekly health trends and patterns
- Calculate weekly medication adherence statistics
- Analyze vital sign trends (improving/stable/worsening)
- Detect symptom patterns and frequencies
- Evaluate exercise compliance and consistency
- Assess nutritional patterns and dietary adherence
- Compare to previous week for trajectory analysis

OUTPUT FORMAT (Valid JSON only):
{
    "week_start": "YYYY-MM-DD",
    "week_end": "YYYY-MM-DD",
    "medication_adherence": {
        "weekly_adherence_rate": float,
        "trend": "improving/stable/declining",
        "missed_doses_count": integer,
        "most_missed_medication": "string",
        "pattern_identified": "string (e.g., 'tends to miss evening doses')"
    },
    "vitals_trends": {
        "blood_pressure": {
            "average_systolic": float,
            "average_diastolic": float,
            "trend": "improving/stable/worsening",
            "variability": "low/moderate/high"
        },
        "heart_rate_avg": float,
        "blood_glucose": {
            "average": float,
            "in_range_percentage": float,
            "trend": "improving/stable/worsening"
        },
        "weight_change_lbs": float,
        "overall_vitals_status": "improving/stable/concerning"
    },
    "symptoms_analysis": {
        "new_symptoms": ["symptoms that appeared this week"],
        "recurring_symptoms": [{"symptom": "string", "frequency": integer, "avg_severity": "string"}],
        "resolved_symptoms": ["symptoms that cleared"],
        "symptom_frequency_map": {"symptom_name": frequency_count},
        "concerning_patterns": ["patterns requiring attention"]
    },
    "exercise_compliance": {
        "days_exercised": integer,
        "total_minutes": integer,
        "average_minutes_per_day": float,
        "compliance_rate": float,
        "consistency": "excellent/good/fair/poor",
        "trend": "improving/stable/declining"
    },
    "nutrition_patterns": {
        "average_daily_calories": float,
        "average_sodium_g": float,
        "average_sugar_g": float,
        "dietary_consistency": "excellent/good/fair/poor",
        "days_met_dietary_goals": integer,
        "primary_concerns": ["list concerns"]
    },
    "comparison_to_previous_week": {
        "medication_adherence_change": "improved/same/worsened",
        "vitals_trajectory": "improved/same/worsened",
        "symptom_burden_change": "decreased/same/increased",
        "exercise_change": "increased/same/decreased",
        "overall_week_comparison": "string summary"
    },
    "weekly_score": float (0-100),
    "key_insights": ["important weekly observations"],
    "concerns_requiring_attention": ["issues to address"]
}

ANALYSIS GUIDELINES:
1. Calculate accurate statistics across 7 days
2. Identify day-of-week patterns (e.g., worse adherence on weekends)
3. Correlate symptoms with medication adherence or dietary changes
4. Look for cyclical patterns
5. Compare metrics to previous week to identify trajectory
6. Flag accelerating negative trends
7. Recognize positive improvements
"""

    user_prompt = f"""Analyze weekly health patterns for patient {patient_id}:

PATIENT CONTEXT:
{json.dumps(patientcontext, indent=2)}

CURRENT WEEK LOGS (7 days):
{json.dumps(weeklylogs, indent=2)}

Provide comprehensive weekly trend analysis as specified."""

    client = MedGemmaClient(system_prompt)
    response = client.respond(user_prompt)

    return response



def monthlylogsAgent(patient_id: str, patientcontext: dict, monthlylogs: list):
    """
    Monthly Logs Agent - Analyzes long-term trends and patterns over a month.
    
    Args:
        patient_id: Patient identifier
        patientcontext: Comprehensive patient context
        monthlylogs: List of ~30 daily log summaries
        previousmonthlylogs: Previous month's logs for comparison
    
    Returns:
        dict: Monthly trends, long-term patterns, and disease progression indicators
    """

    system_prompt = """You are an Expert Clinical Longitudinal Analysis AI specializing in monthly health trajectory assessment.

YOUR ROLE:
- Analyze long-term health trends over 30 days
- Assess disease progression or regression
- Evaluate treatment effectiveness over time
- Identify sustained patterns and chronic issues
- Calculate monthly health metrics and scores
- Compare to previous month for trajectory analysis
- Provide strategic clinical insights

OUTPUT FORMAT (Valid JSON only):
{
    "month_start": "YYYY-MM-DD",
    "month_end": "YYYY-MM-DD",
    "medication_adherence": {
        "monthly_adherence_rate": float,
        "trend_across_month": "improving/stable/declining/fluctuating",
        "total_missed_doses": integer,
        "adherence_by_medication": [{"medication": "string", "rate": float}],
        "barriers_identified": ["identified reasons for non-adherence"],
        "adherence_pattern": "consistent/weekend_dips/sporadic/declining"
    },
    "vitals_analysis": {
        "blood_pressure": {
            "monthly_average_systolic": float,
            "monthly_average_diastolic": float,
            "trend": "improving/stable/worsening",
            "control_status": "well_controlled/poorly_controlled",
            "days_out_of_range": integer
        },
        "blood_glucose": {
            "monthly_average": float,
            "time_in_range_percent": float,
            "glycemic_control": "excellent/good/fair/poor",
            "trend": "improving/stable/worsening"
        },
        "weight": {
            "starting_weight": float,
            "ending_weight": float,
            "change_lbs": float,
            "trend": "losing/stable/gaining",
            "clinically_significant": boolean
        },
        "overall_vitals_trajectory": "improving/stable/deteriorating"
    },
    "symptoms_longitudinal": {
        "chronic_symptoms": [{"symptom": "string", "days_present": integer, "trend": "string"}],
        "intermittent_symptoms": [{"symptom": "string", "occurrences": integer}],
        "new_onset_symptoms": ["symptoms that appeared this month"],
        "resolved_symptoms": ["symptoms that cleared"],
        "symptom_burden_score": float (0-100),
        "symptom_impact_on_quality_of_life": "minimal/moderate/significant/severe"
    },
    "lifestyle_metrics": {
        "exercise": {
            "total_days_exercised": integer,
            "total_minutes": integer,
            "monthly_compliance_rate": float,
            "consistency_score": float,
            "trend": "improving/stable/declining"
        },
        "nutrition": {
            "average_daily_calories": float,
            "average_sodium_g": float,
            "average_sugar_g": float,
            "days_met_dietary_goals": integer,
            "dietary_compliance_rate": float,
            "nutritional_quality_score": float
        }
    },
    "disease_progression": {
        "overall_trajectory": "improving/stable/progressing",
        "control_status": "excellent/good/fair/poor",
        "clinical_stability": "stable/unstable",
        "treatment_response": "excellent/good/partial/poor",
        "progression_indicators": ["specific indicators"]
    },
    "comparison_to_previous_month": {
        "medication_adherence_change": float,
        "vitals_change": "improved/same/worsened",
        "symptom_burden_change": "decreased/same/increased",
        "lifestyle_change": "improved/same/worsened",
        "overall_health_trajectory": "string summary"
    },
    "monthly_health_score": float (0-100),
    "quality_of_life_assessment": "excellent/good/fair/poor",
    "strategic_insights": ["long-term observations and recommendations"],
    "areas_of_concern": ["issues requiring clinical attention"],
    "positive_achievements": ["improvements and successes"]
}

ANALYSIS GUIDELINES:
1. Focus on sustained trends, not daily fluctuations
2. Assess treatment effectiveness over the full month
3. Identify chronic vs. acute issues
4. Look for slow-developing problems
5. Evaluate quality of life impact
6. Consider seasonal or cyclical factors
7. Provide strategic, actionable insights

you must not include any explanatory text, only return the valid JSON object as specified
you must not add facts that are not present in the logs, only analyze the data given and return insights based on that data
"""

    user_prompt = f"""Analyze monthly health trajectory for patient {patient_id}:

PATIENT CONTEXT:
{json.dumps(patientcontext, indent=2)}

CURRENT MONTH LOGS (~30 days):
{json.dumps(monthlylogs, indent=2)}

Provide comprehensive monthly longitudinal analysis as specified."""

    client = MedGemmaClient(system_prompt)
    response = client.respond(user_prompt)

    return response
