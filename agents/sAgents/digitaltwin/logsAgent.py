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

OUTPUT FORMAT (Daily Clinical Health Report):
Please provide the daily analysis in a clear, professional report format using Markdown. Use the following structure:

# CLINICAL DAILY MONITORING REPORT
**Date:** [YYYY-MM-DD]
**Overall Day Status:** [Excellent/Good/Concerning/Critical]
**Immediate Attention Required:** [YES/NO]

## 1. MEDICATION ADHERENCE
- **Adherence Rate:** [X]% ([X] Taken / [X] Prescribed)
- **Missed Doses:** [X]
- **Timing Accuracy:** [Excellent/Good/Fair/Poor]
- **Missed Medications Detail:**
    - [Name] (Scheduled for [Time])
    - [Name] (Scheduled for [Time])

## 2. VITAL SIGNS SUMMARY

- **Blood Pressure:** [Systolic]/[Diastolic] mmHg | Status: [Normal/Elevated/Stage 1/Stage 2/Crisis]
- **Heart Rate:** [BPM] | Status: [Normal/Bradycardia/Tachycardia]
- **Blood Glucose:** [Value] mg/dL | Status: [In-range/Hypoglycemia/Hyperglycemia]
- **Temperature:** [Value]°F | Status: [Normal/Fever/Hypothermia]
- **Other Metrics:** Weight: [Value] lbs | Oxygen Saturation: [X]%
- **Vitals Alerts:**
    - [List specific vital sign concerns or "None"]

## 3. SYMPTOMS LOG
(For each reported symptom:)
- **[Symptom Name]:** [Severity: Mild/Moderate/Severe] at [Time]
- **Requires Clinical Attention:** [Yes/No]

## 4. EXERCISE & ACTIVITY
- **Completed:** [Yes/No]
- **Details:** [Minutes] mins of [Type]
- **Intensity:** [Low/Moderate/High]
- **Meets Daily Goal:** [Yes/No]

## 5. NUTRITION & DIETARY ADHERENCE


[Image of the Healthy Eating Plate]

- **Diet Adherence:** [Excellent/Good/Fair/Poor]
- **Nutritional Data:** [Calories] kcal | [Sodium] g | [Sugar] g
- **Dietary Concerns:** [List concerns related to patient conditions]
- **Medication-Food Interactions:** [List any noted interactions]

## 6. CLINICAL OBSERVATIONS
- **Key Observations:**
    - [Important note 1]
    - [Important note 2]

---

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

OUTPUT FORMAT (Structured Weekly Health Trend Report):
Please provide the weekly analysis in a clear, professional report format using Markdown. Use the following structure:

# WEEKLY HEALTH TREND REPORT
**Reporting Period:** [YYYY-MM-DD] to [YYYY-MM-DD]
**Weekly Health Score:** [0-100]
**Overall Status:** [Improving/Stable/Concerning]

## 1. EXECUTIVE INSIGHTS
- **Key Insights:** [List the most important observations from the week]
- **Critical Concerns:** [List any issues requiring immediate attention]

## 2. MEDICATION ADHERENCE TRENDS

- **Weekly Adherence Rate:** [X]% (Trend: [Improving/Stable/Declining])
- **Dose Tracking:** [X] Missed Doses
- **Primary Barrier:** Most missed medication: [Name]
- **Behavioral Pattern:** [e.g., "Tends to miss evening doses on weekends"]

## 3. VITAL SIGNS & PHYSIOLOGICAL DATA

- **Blood Pressure Trend:** - Average: [Systolic]/[Diastolic] mmHg
    - Status: [Improving/Stable/Worsening] | Variability: [Low/Moderate/High]
- **Blood Glucose Trend:**
    - Average: [Value] | In-Range: [X]%
    - Status: [Improving/Stable/Worsening]
- **Other Metrics:**
    - Average Heart Rate: [BPM]
    - Weekly Weight Change: [+/- X] lbs
- **Vitals Trajectory Status:** [Improving/Stable/Concerning]

## 4. SYMPTOM PATTERN ANALYSIS
- **New Symptoms This Week:** [List symptoms or "None"]
- **Resolved Symptoms:** [List symptoms that cleared]
- **Recurring Symptoms & Frequency:**
    - [Symptom Name]: [X] occurrences | Avg Severity: [Mild/Moderate/Severe]
- **Frequency Map:** [List symptoms and their total weekly count]
- **Concerning Clinical Patterns:** [List any patterns requiring medical attention]

## 5. LIFESTYLE & BEHAVIORAL COMPLIANCE
- **Exercise & Activity:**
    - Days Active: [X]/7 | Total Minutes: [X]
    - Daily Average: [X] mins | Compliance Rate: [X]%
    - Consistency: [Excellent/Good/Fair/Poor] | Trend: [Improving/Stable/Declining]
- **Nutritional Patterns:**
    - Avg Daily Calories: [X] kcal
    - Avg Sodium: [X] g | Avg Sugar: [X] g
    - Dietary Consistency: [Excellent/Good/Fair/Poor]
    - Goals Met: [X]/7 Days
    - Primary Dietary Concerns: [List concerns]

## 6. WEEK-OVER-WEEK COMPARISON

- **Adherence Change:** [Improved/Same/Worsened]
- **Vitals Trajectory:** [Improved/Same/Worsened]
- **Symptom Burden Change:** [Decreased/Same/Increased]
- **Activity Level Change:** [Increased/Same/Decreased]
- **Comparative Summary:** [Provide a narrative summary comparing this week to the previous one]

---

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

OUTPUT FORMAT (Structured Monthly Trajectory Report):
Please provide the analysis in a clear, professional report format using Markdown. Use the following structure:

# MONTHLY CLINICAL TRAJECTORY REPORT
**Reporting Period:** [YYYY-MM-DD] to [YYYY-MM-DD]
**Monthly Health Score:** [0-100]
**Quality of Life Assessment:** [Excellent/Good/Fair/Poor]

## 1. STRATEGIC CLINICAL OVERVIEW
- **Strategic Insights:** [Long-term observations and recommendations]
- **Positive Achievements:** [List improvements and successes from the month]
- **Areas of Concern:** [Issues requiring clinical attention or adjustment]

## 2. LONG-TERM MEDICATION ADHERENCE
- **Monthly Adherence Rate:** [X]% 
- **Adherence Trend:** [Improving/Stable/Declining/Fluctuating]
- **Total Missed Doses:** [X]
- **Adherence Pattern:** [Consistent/Weekend dips/Sporadic/Declining]
- **Medication Breakdown:**
    - [Medication Name]: [X]% Adherence Rate
- **Barrier Analysis:** [List identified reasons for non-adherence]

## 3. PHYSIOLOGICAL TREND ANALYSIS (30-DAY)
### Cardiovascular & Metabolic Trends
- **Blood Pressure:**
    - Monthly Avg: [Systolic]/[Diastolic] mmHg
    - Status: [Well-controlled/Poorly-controlled] | Trend: [X]
    - Days Out of Range: [X]
- **Blood Glucose:**
    - Monthly Avg: [Value] | Time in Range: [X]%
    - Glycemic Control: [Excellent/Good/Fair/Poor] | Trend: [X]
- **Weight Tracking:**
    - Starting: [Value] lbs → Ending: [Value] lbs (Change: [+/- X] lbs)
    - Trend: [Losing/Stable/Gaining] | Clinically Significant: [Yes/No]

**Overall Vitals Trajectory:** [Improving/Stable/Deteriorating]

## 4. SYMPTOM BURDEN & EVOLUTION
- **Symptom Burden Score:** [0-100] | **QoL Impact:** [Minimal/Moderate/Significant/Severe]
- **Chronic Symptoms:** [Symptom Name] ([X] days present) - Trend: [X]
- **Intermittent Symptoms:** [Symptom Name] ([X] occurrences)
- **Resolved Symptoms:** [List symptoms that cleared during this month]
- **New Onset Symptoms:** [List any symptoms that first appeared this month]

## 5. LIFESTYLE & BEHAVIORAL CONSISTENCY
### Exercise Metrics
- **Activity Level:** [X] total days | [X] total minutes
- **Compliance Rate:** [X]% | Consistency Score: [0-100]
- **Trend:** [Improving/Stable/Declining]
### Nutritional Quality
- **Daily Averages:** [Calories] kcal | [Sodium] g | [Sugar] g
- **Compliance:** [X] days met goals | Compliance Rate: [X]%
- **Nutritional Quality Score:** [0-100]

## 6. DISEASE PROGRESSION & STABILITY
- **Overall Trajectory:** [Improving/Stable/Progressing]
- **Control Status:** [Excellent/Good/Fair/Poor]
- **Clinical Stability:** [Stable/Unstable]
- **Treatment Response:** [Excellent/Good/Partial/Poor]
- **Progression Indicators:** [List specific indicators observed]

## 7. MONTH-OVER-MONTH COMPARISON
- **Adherence Change:** [+/- X]% vs Previous Month
- **Vitals Change:** [Improved/Same/Worsened]
- **Symptom Burden Change:** [Decreased/Same/Increased]
- **Lifestyle Change:** [Improved/Same/Worsened]
- **Health Trajectory Summary:** [Summary of how this month compared to last]

---

ANALYSIS GUIDELINES:
1. Focus on sustained trends, not daily fluctuations
2. Assess treatment effectiveness over the full month
3. Identify chronic vs. acute issues
4. Look for slow-developing problems
5. Evaluate quality of life impact
6. Consider seasonal or cyclical factors
7. Provide strategic, actionable insights
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
