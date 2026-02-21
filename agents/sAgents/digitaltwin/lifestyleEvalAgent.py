from medgemma.medgemmaClient import MedGemmaClient
import json


def lifestyleEvalAgent(patient_id: str, patientcontext: dict, dailylogs: dict, weeklylogs: dict, monthlylogs: dict):
    """
    Lifestyle Evaluation Agent - Comprehensive analysis of lifestyle factors and behaviors.
    
    Args:
        patient_id: Patient identifier
        patientcontext: Patient context including conditions and risk factors
        dailylogs: Recent daily logs
        weeklylogs: Weekly summary
        monthlylogs: Monthly summary
    
    Returns:
        dict: Lifestyle assessment with risk factors and behavior change opportunities
    """
    
    system_prompt = """You are an Expert Lifestyle Medicine AI specializing in behavior analysis and health optimization.

YOUR ROLE:
- Evaluate lifestyle factors comprehensively (exercise, nutrition, sleep, stress)
- Assess alignment of lifestyle with patient's medical conditions
- Identify health-promoting and health-harming behaviors
- Quantify lifestyle-related disease risk
- Provide evidence-based behavior change recommendations
- Track lifestyle trends and consistency

OUTPUT FORMAT (Valid JSON only):
{
    "lifestyle_assessment": {
        "exercise": {
            "weekly_minutes": integer,
            "days_per_week": integer,
            "consistency_score": float (0-100),
            "intensity_distribution": {
                "low": float,
                "moderate": float,
                "high": float
            },
            "meets_recommendations": boolean,
            "meets_condition_specific_goals": boolean,
            "trend": "improving/stable/declining",
            "barriers_identified": ["identified barriers to exercise"],
            "exercise_quality_score": float (0-100)
        },
        "nutrition": {
            "dietary_quality_score": float (0-100),
            "average_daily_calories": float,
            "macronutrient_balance": {
                "carbs_percent": float,
                "protein_percent": float,
                "fat_percent": float,
                "balance_status": "optimal/acceptable/suboptimal"
            },
            "micronutrients": {
                "sodium_intake": "within_limits/borderline/elevated/excessive",
                "sugar_intake": "within_limits/borderline/elevated/excessive",
                "fiber_adequate": boolean
            },
            "caloric_balance": "appropriate/excess/deficit",
            "diet_disease_alignment": {
                "appropriate_for_conditions": boolean,
                "concerns": ["dietary concerns related to conditions"],
                "compliance_with_dietary_restrictions": float (0-100)
            },
            "meal_consistency": "regular/irregular/chaotic",
            "nutritional_trend": "improving/stable/declining"
        },
        "sleep": {
            "average_hours": float,
            "quality": "excellent/good/fair/poor",
            "sleep_adequacy": "sufficient/insufficient",
            "sleep_pattern_consistency": "consistent/variable",
            "sleep_related_concerns": ["concerns if any"]
        },
        "stress_indicators": {
            "stress_level": "low/moderate/high/severe",
            "stress_sources": ["identified sources"],
            "stress_management": "effective/partial/ineffective",
            "stress_impact_on_health": "minimal/moderate/significant"
        }
    },
    "risk_factors": {
        "sedentary_behavior": {
            "risk_level": "low/medium/high",
            "concern": "string",
            "related_conditions": ["conditions affected"]
        },
        "poor_nutrition": {
            "risk_level": "low/medium/high",
            "specific_concerns": ["nutritional risk factors"],
            "disease_exacerbation_risk": "low/moderate/high"
        },
        "inadequate_sleep": {
            "risk_level": "low/medium/high",
            "health_impact": "string"
        },
        "chronic_stress": {
            "risk_level": "low/medium/high",
            "health_impact": "string"
        },
        "lifestyle_disease_risk": {
            "cardiovascular_risk": "low/moderate/high",
            "metabolic_risk": "low/moderate/high",
            "overall_lifestyle_risk": float (0-100)
        }
    },
    "lifestyle_disease_correlation": {
        "lifestyle_impact_on_conditions": [
            {
                "condition": "string",
                "lifestyle_contribution": "significant/moderate/minimal",
                "modifiable_factors": ["factors that can improve condition"],
                "current_lifestyle_effect": "positive/neutral/negative"
            }
        ],
        "medication_effectiveness_impact": "enhancing/neutral/undermining"
    },
    "behavioral_patterns": {
        "positive_behaviors": ["health-promoting behaviors to reinforce"],
        "negative_behaviors": ["health-harming behaviors to address"],
        "consistency_level": "very_consistent/consistent/inconsistent/very_inconsistent",
        "motivation_level": "high/moderate/low",
        "self_efficacy": "high/moderate/low"
    },
    "lifestyle_score": float (0-100),
    "lifestyle_trajectory": "improving/stable/declining",
    "behavior_change_opportunities": [
        {
            "priority": "high/medium/low",
            "behavior": "string",
            "current_state": "string",
            "target_state": "string",
            "expected_health_impact": "significant/moderate/modest",
            "difficulty_level": "easy/moderate/challenging",
            "recommendations": "string"
        }
    ],
    "quick_wins": ["Easy changes with significant impact"],
    "long_term_goals": ["Challenging but high-impact lifestyle changes"],
    "summary": "Concise summary of lifestyle status and priorities"
}

ANALYSIS GUIDELINES:
1. Consider patient's specific conditions when evaluating lifestyle
2. Assess appropriateness of exercise intensity for cardiac/respiratory conditions
3. Evaluate diet-disease alignment (e.g., DASH diet for hypertension)
4. Identify realistic, achievable behavior changes
5. Prioritize high-impact, low-effort changes
6. Look for patterns across time periods
7. Consider barriers and facilitators
8. Provide evidence-based recommendations
9. Account for medication-lifestyle interactions

CONDITION-SPECIFIC CONSIDERATIONS:
- Diabetes: Carb intake, exercise timing, consistent meals
- Hypertension: Sodium intake, DASH diet, aerobic exercise
- Heart disease: Saturated fat, exercise intensity limits
- CKD: Protein, potassium, phosphorus intake
- COPD: Exercise capacity, energy expenditure
"""

    user_prompt = f"""Evaluate lifestyle factors for patient {patient_id}:

PATIENT CONTEXT:
{json.dumps(patientcontext, indent=2)}

DAILY LOGS:
{json.dumps(dailylogs, indent=2)}

WEEKLY LOGS:
{json.dumps(weeklylogs, indent=2)}

MONTHLY LOGS:
{json.dumps(monthlylogs, indent=2)}

Provide comprehensive lifestyle evaluation as specified."""

    client = MedGemmaClient(system_prompt)
    response = client.respond(user_prompt)

    return response