from agents.sAgents.digitaltwin.alertGeneratorAgent import alertGeneratorAgent
from agents.sAgents.digitaltwin.lifestyleEvalAgent import lifestyleEvalAgent
from agents.sAgents.digitaltwin.medicationAdherenceAgent import medicationAdherenceAgent
from agents.sAgents.digitaltwin.nutritionalAgent import nutritionalAgent
from agents.sAgents.digitaltwin.finalreport import digitalTwinState
from agents.sAgents.digitaltwin.logsAgent import dailylogsAgent, weeklylogsAgent, monthlylogsAgent
from agents.sAgents.digitaltwin.forecastAgent import forecastAgent
from agents.sAgents.digitaltwin.memoryAgents import dailyProfile, WeeklyProfile, monthlyProfile
from agents.sAgents.digitaltwin.patientContextAgent import pca
from agents.sAgents.digitaltwin.symptomsCorelatorAgent import symptomsCorelatorAgent
from agents.sAgents.digitaltwin.diffReasoner import diffreasoner
from ehr_store.patientdata.data_manager import append_daily_log, load_report
from ehr_store.patientdata.data_manager import get_recent_daily_logs
import json

def digitaltwinpipeline(patient_id: str, input_logs: dict):
    """
    Digital Twin Pipeline - Comprehensive health monitoring and predictive analytics system.
    
    Pipeline Architecture:
    
                    ┌────────────────────┐
                    │   Daily Log Input  │
                    └─────────┬──────────┘
                              ↓
    ┌─────────────────────────────────────────────────────────────┐
    │  STAGE 1: CONTEXT & DATA PREPARATION                        │
    ├─────────────────────────────────────────────────────────────┤
    │  1. patientContextAgent → Load EHR baseline                 │
    │  2. nutritionalAgent → Enrich logs with nutritional data    │
    │  3. logsAgent (daily/weekly/monthly) → Temporal summaries   │
    └──────────────────────────┬──────────────────────────────────┘
                               ↓
    ┌─────────────────────────────────────────────────────────────┐
    │  STAGE 2: MEMORY LAYER                                      │
    ├─────────────────────────────────────────────────────────────┤
    │  memoryAgents (daily/weekly/monthly) → Update profiles      │
    └──────────────────────────┬──────────────────────────────────┘
                               ↓
    ┌─────────────────────────────────────────────────────────────┐
    │  STAGE 3: PARALLEL ANALYSIS (Concurrent execution)          │
    ├─────────────────────────────────────────────────────────────┤
    │  ├─→ medicationAdherenceAgent                               │
    │  ├─→ lifestyleEvalAgent                                     │
    │  └─→ symptomsCorelatorAgent                                 │
    └──────────────────────────┬──────────────────────────────────┘
                               ↓
    ┌─────────────────────────────────────────────────────────────┐
    │  STAGE 4: PREDICTIVE LAYER                                  │
    ├─────────────────────────────────────────────────────────────┤
    │  forecastAgent → Generate health trajectory predictions     │
    └──────────────────────────┬──────────────────────────────────┘
                               ↓
    ┌─────────────────────────────────────────────────────────────┐
    │  STAGE 5: ALERT GENERATION                                  │
    ├─────────────────────────────────────────────────────────────┤
    │  alertGeneratorAgent → Create actionable alerts             │
    └──────────────────────────┬──────────────────────────────────┘
                               ↓
    ┌─────────────────────────────────────────────────────────────┐
    │  STAGE 6: STATE CONSOLIDATION                               │
    ├─────────────────────────────────────────────────────────────┤
    │  digitalTwinState → Generate current twin state snapshot    │
    └──────────────────────────┬──────────────────────────────────┘
                               ↓
    ┌─────────────────────────────────────────────────────────────┐
    │  STAGE 7: DEVIATION ANALYSIS                                │
    ├─────────────────────────────────────────────────────────────┤
    │  diffReasoner → Analyze WHY/HOW patient deviated from       │
    │                 forecast and provide corrective insights    │
    └──────────────────────────┬──────────────────────────────────┘
                               ↓
    ┌─────────────────────────────────────────────────────────────┐
    │  OUTPUT: Final Report + EHR Update                          │
    └─────────────────────────────────────────────────────────────┘
    
    Args:
        patient_id: Unique patient identifier
        input_logs: Dictionary containing:
            {
                "daily_logs": {
                    "date": "YYYY-MM-DD",
                    "medications_taken": [...],
                    "vitals": {...},
                    "symptoms": [...],
                    "exercise": {...},
                    "nutrition": {...},
                    "labs": [...],
                    "notes": "string"
                },
                "weekly_logs": [list of 7 daily logs],
                "previous_weekly_logs": [list of previous week],
                "monthly_logs": [list of ~30 daily logs],
                "previous_monthly_logs": [list of previous month]
            }
    
    Returns:
        dict: Comprehensive digital twin report including:
            - Patient context
            - Processed logs summaries
            - Memory profiles
            - Analysis outputs (adherence, lifestyle, symptoms)
            - Health forecast
            - Alerts
            - Current twin state
            - Deviation analysis
    """
    
    print(f"🚀 Starting Digital Twin Pipeline for Patient: {patient_id}")
    print("=" * 80)

    weekly_logs = get_recent_daily_logs(patient_id, number_of_days=7)
    monthly_logs = get_recent_daily_logs(patient_id, number_of_days=30)

    patient_report = load_report(patient_id)  # Load previous patient report for context (if available)

    # =============================================================================
    # STAGE 1: CONTEXT & DATA PREPARATION
    # =============================================================================
    print("\n📋 STAGE 1: CONTEXT & DATA PREPARATION")
    print("-" * 80)
    
    # 1.1 Load Patient Context from EHR
    print("  [1/3] Loading patient context from EHR...")
    try:
        patient_context = pca(patient_id)
        patient_context = json.loads(patient_context) if isinstance(patient_context, str) else patient_context
        print("  ✅ Patient context loaded successfully")
    except Exception as e:
        print(f"  ❌ Error loading patient context: {e}")
        raise
    
    # 1.2 Enrich Nutrition Data
    print("  [2/3] Enriching nutrition data...")
    try:


        if "nutrition" in input_logs:
            print("  🔍 Nutrition data found, analyzing...")
            print(f"  📊 Original Nutrition Data: {input_logs.get('nutrition', 'None')}")
            nutrition_analysis = nutritionalAgent(input_logs.get("nutrition", None))
            nutrition_analysis = json.loads(nutrition_analysis) if isinstance(nutrition_analysis, str) else nutrition_analysis
            # Update daily logs with enriched nutrition data
            input_logs["nutrition_enriched"] = nutrition_analysis
            
            print("  ✅ Nutrition data enriched successfully")
            print("new dailylogs are ")

            # appent these logs to daily logs
            append_daily_log(patient_id, input_logs)


        else:
            print(" ⚠️  No nutrition data provided, skipping enrichment")
            nutrition_analysis = None
    except Exception as e:
        print(f"  ⚠️  Error enriching nutrition data: {e}")
        nutrition_analysis = None
    
    # 1.3 Process Logs at Different Time Scales
    print("  [3/3] Processing temporal logs...")
    try:
        # Daily logs processing
        daily_logs_summary = dailylogsAgent(
            patient_id,
            patient_context,
            input_logs
        )
        daily_logs_summary = json.loads(daily_logs_summary) if isinstance(daily_logs_summary, str) else daily_logs_summary
        
        # Weekly logs processing
        weekly_logs_summary = weeklylogsAgent(
            patient_id,
            patient_context,
            weekly_logs
        )
        weekly_logs_summary = json.loads(weekly_logs_summary) if isinstance(weekly_logs_summary, str) else weekly_logs_summary
        
        # Monthly logs processing
        monthly_logs_summary = monthlylogsAgent(
            patient_id,
            patient_context,
            monthly_logs
        )
        monthly_logs_summary = json.loads(monthly_logs_summary) if isinstance(monthly_logs_summary, str) else monthly_logs_summary
        
        print("  ✅ All temporal logs processed successfully")
    except Exception as e:
        print(f"  ❌ Error processing logs: {e}")
        raise
    
    # =============================================================================
    # STAGE 2: MEMORY LAYER
    # =============================================================================
    print("\n🧠 STAGE 2: MEMORY LAYER")
    print("-" * 80)
    
    try:
        # Daily memory profile
        print("  [1/3] Creating daily memory profile...")
        daily_memory_profile = dailyProfile(patient_id, patient_context, weekly_logs_summary, patient_report)
        daily_memory_profile = json.loads(daily_memory_profile) if isinstance(daily_memory_profile, str) else daily_memory_profile
        
        # Weekly memory profile
        print("  [2/3] Creating weekly memory profile...")
        weekly_memory_profile = WeeklyProfile(patient_id, patient_context, weekly_logs_summary, patient_report)
        weekly_memory_profile = json.loads(weekly_memory_profile) if isinstance(weekly_memory_profile, str) else weekly_memory_profile
        
        # Monthly memory profile
        print("  [3/3] Creating monthly memory profile...")
        monthly_memory_profile = monthlyProfile(patient_id, patient_context, monthly_logs_summary, patient_report)
        monthly_memory_profile = json.loads(monthly_memory_profile) if isinstance(monthly_memory_profile, str) else monthly_memory_profile
        
        print("  ✅ All memory profiles created successfully")
    except Exception as e:
        print(f"  ❌ Error creating memory profiles: {e}")
        raise
    
    # =============================================================================
    # STAGE 3: PARALLEL ANALYSIS
    # =============================================================================
    print("\n🔬 STAGE 3: PARALLEL ANALYSIS")
    print("-" * 80)
    
    try:
        # Medication Adherence Analysis
        print("  [1/3] Analyzing medication adherence...")
        med_adherence_analysis = medicationAdherenceAgent(
            patient_id,
            patient_context,
            weekly_logs_summary
        )
        med_adherence_analysis = json.loads(med_adherence_analysis) if isinstance(med_adherence_analysis, str) else med_adherence_analysis
        
        # Lifestyle Evaluation
        print("  [2/3] Evaluating lifestyle factors...")
        lifestyle_evaluation = lifestyleEvalAgent(
            patient_id,
            patient_context,
            monthly_logs_summary,
            patient_report
        )
        lifestyle_evaluation = json.loads(lifestyle_evaluation) if isinstance(lifestyle_evaluation, str) else lifestyle_evaluation
        
        # Symptoms Correlation
        print("  [3/3] Correlating symptom patterns...")
        symptoms_correlation = symptomsCorelatorAgent(
            patient_id,
            patient_context,
            weekly_logs_summary,
            patient_report,
            weekly_memory_profile
        )
        symptoms_correlation = json.loads(symptoms_correlation) if isinstance(symptoms_correlation, str) else symptoms_correlation
        
        print("  ✅ All parallel analyses completed successfully")
    except Exception as e:
        print(f"  ❌ Error in parallel analysis: {e}")
        raise
    
    
    # =============================================================================
    # STAGE 4: PREDICTIVE LAYER
    # =============================================================================
    print("\n🔮 STAGE 4: PREDICTIVE LAYER")
    print("-" * 80)
    
    try:
        print("  [1/1] Generating health trajectory forecast...")
        health_forecast = forecastAgent(
            patient_id,
            patient_context,
            daily_logs_summary,
            weekly_logs_summary,
            monthly_logs_summary,
            med_adherence_analysis,
            lifestyle_evaluation,
            symptoms_correlation
        )
        health_forecast = json.loads(health_forecast) if isinstance(health_forecast, str) else health_forecast
        print("  ✅ Health forecast generated successfully")
    except Exception as e:
        print(f"  ❌ Error generating forecast: {e}")
        raise
    
    # =============================================================================
    # STAGE 5: ALERT GENERATION
    # =============================================================================
    print("\n🚨 STAGE 5: ALERT GENERATION")
    print("-" * 80)
    
    try:
        print("  [1/1] Generating clinical alerts...")
        clinical_alerts = alertGeneratorAgent(
            patient_id,
            patient_context,
            daily_logs_summary,
            weekly_logs_summary,
            monthly_logs_summary,
            health_forecast
        )
        clinical_alerts = json.loads(clinical_alerts) if isinstance(clinical_alerts, str) else clinical_alerts
        
        # Display alert summary
        alert_summary = clinical_alerts.get("alert_summary", {})
        print(f"  📊 Alert Summary:")
        print(f"     • Critical: {alert_summary.get('critical_count', 0)}")
        print(f"     • High: {alert_summary.get('high_priority_count', 0)}")
        print(f"     • Medium: {alert_summary.get('medium_priority_count', 0)}")
        print(f"     • Low: {alert_summary.get('low_priority_count', 0)}")
        print("  ✅ Clinical alerts generated successfully")
    except Exception as e:
        print(f"  ❌ Error generating alerts: {e}")
        raise
    
    # =============================================================================
    # STAGE 6: STATE CONSOLIDATION
    # =============================================================================
    print("\n🎯 STAGE 6: STATE CONSOLIDATION")
    print("-" * 80)
    
    try:
        print("  [1/1] Generating digital twin state...")
        twin_state = digitalTwinState(
            patient_id,
            weekly_memory_profile,
            med_adherence_analysis,
            lifestyle_evaluation,
            symptoms_correlation,
            health_forecast,
            clinical_alerts
        )
        twin_state = json.loads(twin_state) if isinstance(twin_state, str) else twin_state
        
        # Display state summary
        current_state = twin_state.get("current_health_state", {})
        print(f"  📊 Twin State Summary:")
        print(f"     • Overall Status: {current_state.get('overall_status', 'N/A')}")
        print(f"     • Health Score: {current_state.get('overall_health_score', 'N/A')}")
        print(f"     • Trajectory: {current_state.get('health_trajectory', 'N/A')}")
        print("  ✅ Digital twin state generated successfully")
    except Exception as e:
        print(f"  ❌ Error generating twin state: {e}")
        raise
    
    # =============================================================================
    # STAGE 7: DEVIATION ANALYSIS
    # =============================================================================
    print("\n📊 STAGE 7: DEVIATION ANALYSIS")
    print("-" * 80)
    
    try:
        print("  [1/1] Analyzing trajectory deviations...")
        deviation_analysis = diffreasoner(
            patient_id,
            patient_context,
            health_forecast,
            twin_state,
            weekly_memory_profile,
            monthly_memory_profile,
            clinical_alerts,
            med_adherence_analysis,
            lifestyle_evaluation,
            symptoms_correlation
        )
        deviation_analysis = json.loads(deviation_analysis) if isinstance(deviation_analysis, str) else deviation_analysis
        
        # Display deviation summary
        deviation_status = deviation_analysis.get("deviation_analysis", {})
        print(f"  📊 Deviation Analysis:")
        print(f"     • Status: {deviation_status.get('overall_deviation_status', 'N/A')}")
        print(f"     • Severity: {deviation_status.get('deviation_severity_score', 'N/A')}")
        alignment = deviation_status.get('trajectory_comparison', {}).get('alignment', 'N/A')
        print(f"     • Alignment: {alignment}")
        print("  ✅ Deviation analysis completed successfully")
    except Exception as e:
        print(f"  ❌ Error in deviation analysis: {e}")
        raise
    
    # =============================================================================
    # FINAL OUTPUT
    # =============================================================================
    print("\n" + "=" * 80)
    print("✅ DIGITAL TWIN PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 80)
    
    # Compile final comprehensive report
    final_report = {
        "pipeline_metadata": {
            "patient_id": patient_id,
            "execution_timestamp": input_logs.get("daily_logs", {}).get("date", ""),
            "pipeline_version": "1.0.0",
            "stages_completed": 7
        },
        "patient_context": patient_context,
        "processed_logs": {
            "daily_summary": daily_logs_summary,
            "weekly_summary": weekly_logs_summary,
            "monthly_summary": monthly_logs_summary
        },
        "memory_profiles": {
            "daily": daily_memory_profile,
            "weekly": weekly_memory_profile,
            "monthly": monthly_memory_profile
        },
        "analysis_results": {
            "medication_adherence": med_adherence_analysis,
            "lifestyle_evaluation": lifestyle_evaluation,
            "symptoms_correlation": symptoms_correlation
        },
        "health_forecast": health_forecast,
        "clinical_alerts": clinical_alerts,
        "digital_twin_state": twin_state,
        "deviation_analysis": deviation_analysis,
        "executive_summary": {
            "overall_health_status": twin_state.get("current_health_state", {}).get("overall_status", "N/A"),
            "health_score": twin_state.get("current_health_state", {}).get("overall_health_score", 0),
            "trajectory": twin_state.get("current_health_state", {}).get("health_trajectory", "N/A"),
            "deviation_status": deviation_analysis.get("deviation_analysis", {}).get("overall_deviation_status", "N/A"),
            "critical_alerts": clinical_alerts.get("alert_summary", {}).get("critical_count", 0),
            "requires_immediate_attention": clinical_alerts.get("alert_summary", {}).get("requires_immediate_attention", False),
            "key_recommendations": deviation_analysis.get("corrective_insights", {}).get("intervention_opportunities", [])[:3]
        }
    }
    
    print(f"\n📝 Executive Summary:")
    print(f"   • Health Status: {final_report['executive_summary']['overall_health_status']}")
    print(f"   • Health Score: {final_report['executive_summary']['health_score']}/100")
    print(f"   • Trajectory: {final_report['executive_summary']['trajectory']}")
    print(f"   • Deviation: {final_report['executive_summary']['deviation_status']}")
    print(f"   • Critical Alerts: {final_report['executive_summary']['critical_alerts']}")
    print(f"   • Immediate Attention Required: {final_report['executive_summary']['requires_immediate_attention']}")
    
    # TODO: Write back to EHR
    # save_to_ehr(patient_id, final_report)
    
    return final_report


