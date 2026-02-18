"""
Patient Progress Analysis Pipeline

Comprehensive agentic orchestration for analyzing patient progress based on current conditions,
historical EHR data, reports, imaging, and diagnostics.

This pipeline integrates multiple specialized agents to provide:
- Comprehensive data aggregation and normalization
- Current clinical status assessment
- Longitudinal progress and risk analysis
- Imaging and diagnostics interpretation
- Professional clinical report generation
- Prioritized alerts and actionable recommendations

Pipeline Flow:
1. Data Aggregator Agent → Consolidate and normalize all patient data
2. Current Status Analyzer Agent → Assess current clinical state
3. Progress & Risk Assessor Agent → Analyze trends and stratify risks
4. Imaging & Diagnostics Interpreter Agent → Interpret studies and findings
5. Clinical Report Generator Agent → Create comprehensive clinical report
6. Alert & Recommendation Agent → Generate prioritized alerts and actions

Usage:
    from orchestrations.patient_progress_analysis_pipeline import patientProgressAnalysisPipeline
    
    result = patientProgressAnalysisPipeline(
        patient_id="P12345",
        ehr_summary=ehr_data,
        current_report="detailed current condition report",
        historical_reports=[report1, report2, ...],
        imaging_data=imaging_studies
    )
    
    # Access components:
    print(result['aggregated_data'])
    print(result['current_status'])
    print(result['progress_assessment'])
    print(result['imaging_interpretation'])
    print(result['clinical_report'])
    print(result['alerts_recommendations'])
    print(result['executive_summary'])
"""

from agents.sAgents.progressAnalysis.data_aggregator_agent import dataAggregatorAgent
from agents.sAgents.progressAnalysis.current_status_analyzer_agent import currentStatusAnalyzerAgent
from agents.sAgents.progressAnalysis.progress_risk_assessor_agent import progressRiskAssessorAgent
from agents.sAgents.progressAnalysis.imaging_diagnostics_interpreter_agent import imagingDiagnosticsInterpreterAgent
from agents.sAgents.progressAnalysis.clinical_report_generator_agent import clinicalReportGeneratorAgent
from agents.sAgents.progressAnalysis.alert_recommendation_agent import alertRecommendationAgent
import json
from datetime import datetime


def patientProgressAnalysisPipeline(
    patient_id,
    ehr_summary,
    current_report,
    historical_reports=None,
    imaging_data=None,
    include_detailed_logs=False
):
    """
    Orchestrates comprehensive patient progress analysis using multiple specialized agents.
    
    Args:
        patient_id (str): Unique patient identifier
        ehr_summary (dict or str): Electronic health record summary data
        current_report (str): Current clinical condition report
        historical_reports (list, optional): List of historical clinical reports
        imaging_data (dict or list, optional): Imaging and diagnostic study data
        include_detailed_logs (bool, optional): Include detailed processing logs
        
    Returns:
        dict: Comprehensive analysis results containing all agent outputs and executive summary
        
    Structure of returned dictionary:
        {
            "patient_id": str,
            "analysis_timestamp": str,
            "pipeline_status": "completed" | "completed_with_warnings" | "failed",
            "aggregated_data": str,              # Output from Data Aggregator Agent
            "current_status": str,                # Output from Current Status Analyzer
            "progress_assessment": str,           # Output from Progress & Risk Assessor
            "imaging_interpretation": str,        # Output from Imaging Interpreter
            "clinical_report": str,               # Output from Clinical Report Generator
            "alerts_recommendations": str,        # Output from Alert & Recommendation Agent
            "executive_summary": dict,            # High-level summary for quick review
            "processing_log": list                # Detailed processing information (if enabled)
        }
    """
    
    # Initialize results container
    results = {
        "patient_id": patient_id,
        "analysis_timestamp": datetime.now().isoformat(),
        "pipeline_status": "in_progress",
        "processing_log": [] if include_detailed_logs else None
    }
    
    def log_step(step_name, status, message="", data=None):
        """Helper function to log pipeline steps."""
        if include_detailed_logs:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "step": step_name,
                "status": status,
                "message": message
            }
            if data:
                log_entry["data"] = data
            results["processing_log"].append(log_entry)
    
    try:
        # =================================================================
        # STEP 1: DATA AGGREGATION
        # =================================================================
        log_step(
            "Data Aggregation",
            "started",
            "Consolidating and normalizing patient data from all sources"
        )
        
        print("\n" + "="*70)
        print("PATIENT PROGRESS ANALYSIS PIPELINE")
        print("="*70)
        print(f"Patient ID: {patient_id}")
        print(f"Timestamp: {results['analysis_timestamp']}")
        print("="*70)
        
        print("\n[1/6] Running Data Aggregator Agent...")
        aggregated_data = dataAggregatorAgent(
            patient_id=patient_id,
            ehr_summary=ehr_summary,
            current_report=current_report,
            historical_reports=historical_reports,
            imaging_data=imaging_data
        )
        results["aggregated_data"] = aggregated_data
        log_step("Data Aggregation", "completed", "Data successfully aggregated and normalized")
        print("✓ Data aggregation completed")
        
        # =================================================================
        # STEP 2: CURRENT STATUS ANALYSIS
        # =================================================================
        log_step(
            "Current Status Analysis",
            "started",
            "Analyzing patient's current clinical status"
        )
        
        print("\n[2/6] Running Current Status Analyzer Agent...")
        current_status = currentStatusAnalyzerAgent(
            aggregated_data=aggregated_data,
            patient_id=patient_id
        )
        results["current_status"] = current_status
        log_step("Current Status Analysis", "completed", "Current clinical status assessed")
        print("✓ Current status analysis completed")
        
        # =================================================================
        # STEP 3: PROGRESS & RISK ASSESSMENT
        # =================================================================
        log_step(
            "Progress & Risk Assessment",
            "started",
            "Evaluating patient progress and stratifying risks"
        )
        
        print("\n[3/6] Running Progress & Risk Assessor Agent...")
        progress_assessment = progressRiskAssessorAgent(
            aggregated_data=aggregated_data,
            current_status=current_status,
            patient_id=patient_id
        )
        results["progress_assessment"] = progress_assessment
        log_step("Progress & Risk Assessment", "completed", "Progress analyzed and risks stratified")
        print("✓ Progress and risk assessment completed")
        
        # =================================================================
        # STEP 4: IMAGING & DIAGNOSTICS INTERPRETATION
        # =================================================================
        log_step(
            "Imaging & Diagnostics Interpretation",
            "started",
            "Interpreting imaging and diagnostic studies"
        )
        
        print("\n[4/6] Running Imaging & Diagnostics Interpreter Agent...")
        imaging_interpretation = imagingDiagnosticsInterpreterAgent(
            aggregated_data=aggregated_data,
            imaging_data=imaging_data,
            patient_id=patient_id
        )
        results["imaging_interpretation"] = imaging_interpretation
        log_step("Imaging & Diagnostics Interpretation", "completed", "Imaging and diagnostics interpreted")
        print("✓ Imaging and diagnostics interpretation completed")
        
        # =================================================================
        # STEP 5: CLINICAL REPORT GENERATION
        # =================================================================
        log_step(
            "Clinical Report Generation",
            "started",
            "Generating comprehensive clinical progress report"
        )
        
        print("\n[5/6] Running Clinical Report Generator Agent...")
        clinical_report = clinicalReportGeneratorAgent(
            aggregated_data=aggregated_data,
            current_status=current_status,
            progress_risk=progress_assessment,
            imaging_interpretation=imaging_interpretation,
            patient_id=patient_id
        )
        results["clinical_report"] = clinical_report
        log_step("Clinical Report Generation", "completed", "Comprehensive clinical report generated")
        print("✓ Clinical report generation completed")
        
        # =================================================================
        # STEP 6: ALERTS & RECOMMENDATIONS
        # =================================================================
        log_step(
            "Alerts & Recommendations",
            "started",
            "Generating prioritized alerts and actionable recommendations"
        )
        
        print("\n[6/6] Running Alert & Recommendation Agent...")
        alerts_recommendations = alertRecommendationAgent(
            aggregated_data=aggregated_data,
            current_status=current_status,
            progress_risk=progress_assessment,
            imaging_interpretation=imaging_interpretation,
            clinical_report=clinical_report,
            patient_id=patient_id
        )
        results["alerts_recommendations"] = alerts_recommendations
        log_step("Alerts & Recommendations", "completed", "Alerts and recommendations generated")
        print("✓ Alerts and recommendations completed")
        
        # =================================================================
        # EXECUTIVE SUMMARY GENERATION
        # =================================================================
        print("\n[*] Generating Executive Summary...")
        
        # Try to extract key information for executive summary
        executive_summary = {
            "patient_id": patient_id,
            "analysis_date": results["analysis_timestamp"],
            "pipeline_completion_status": "All agents completed successfully",
            "summary": "Comprehensive patient progress analysis completed. Review detailed outputs for full clinical picture.",
            "critical_alerts_count": "See alerts_recommendations output",
            "overall_status": "See current_status output",
            "trajectory": "See progress_assessment output",
            "immediate_actions_required": "Review alerts_recommendations for prioritized action items"
        }
        
        results["executive_summary"] = executive_summary
        results["pipeline_status"] = "completed"
        log_step("Pipeline", "completed", "All agents executed successfully")
        
        print("\n" + "="*70)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print("="*70)
        print(f"Total steps executed: 6/6")
        print(f"Status: {results['pipeline_status']}")
        print("="*70 + "\n")
        
        return results
        
    except Exception as e:
        # Handle pipeline failures
        error_message = f"Pipeline failed: {str(e)}"
        log_step("Pipeline", "failed", error_message)
        
        results["pipeline_status"] = "failed"
        results["error"] = {
            "message": str(e),
            "type": type(e).__name__,
            "timestamp": datetime.now().isoformat()
        }
        
        print("\n" + "="*70)
        print("PIPELINE FAILED")
        print("="*70)
        print(f"Error: {error_message}")
        print("="*70 + "\n")
        
        return results


def patientProgressAnalysisPipelineQuick(
    patient_id,
    ehr_summary,
    current_report,
    historical_reports=None,
    imaging_data=None
):
    """
    Quick version of the pipeline that returns only the final clinical report and alerts.
    
    Useful when you only need the actionable outputs without intermediate agent results.
    
    Args:
        patient_id (str): Unique patient identifier
        ehr_summary (dict or str): Electronic health record summary data
        current_report (str): Current clinical condition report
        historical_reports (list, optional): List of historical clinical reports
        imaging_data (dict or list, optional): Imaging and diagnostic study data
        
    Returns:
        dict: Simplified results with clinical report and alerts only
    """
    
    full_results = patientProgressAnalysisPipeline(
        patient_id=patient_id,
        ehr_summary=ehr_summary,
        current_report=current_report,
        historical_reports=historical_reports,
        imaging_data=imaging_data,
        include_detailed_logs=False
    )
    
    # Return only the most actionable outputs
    quick_results = {
        "patient_id": full_results["patient_id"],
        "analysis_timestamp": full_results["analysis_timestamp"],
        "pipeline_status": full_results["pipeline_status"],
        "clinical_report": full_results.get("clinical_report", "Not available"),
        "alerts_recommendations": full_results.get("alerts_recommendations", "Not available"),
        "executive_summary": full_results.get("executive_summary", {})
    }
    
    if "error" in full_results:
        quick_results["error"] = full_results["error"]
    
    return quick_results


# Example usage and testing
if __name__ == "__main__":
    """
    Example usage of the Patient Progress Analysis Pipeline.
    """
    
    # Example patient data
    example_patient_id = "P001234"
    
    example_ehr = {
        "demographics": {
            "age": 65,
            "sex": "Male",
            "weight_kg": 85,
            "height_cm": 175
        },
        "diagnoses": [
            {"condition": "Type 2 Diabetes Mellitus", "onset": "2018-03-15", "icd10": "E11.9"},
            {"condition": "Hypertension", "onset": "2015-06-20", "icd10": "I10"},
            {"condition": "Chronic Kidney Disease Stage 3", "onset": "2020-09-10", "icd10": "N18.3"}
        ],
        "medications": [
            {"name": "Metformin", "dose": "1000mg", "frequency": "BID", "start_date": "2018-03-15"},
            {"name": "Lisinopril", "dose": "20mg", "frequency": "Daily", "start_date": "2015-06-20"}
        ],
        "allergies": [
            {"allergen": "Penicillin", "reaction": "Rash"}
        ],
        "labs_recent": {
            "HbA1c": {"value": 7.8, "date": "2024-01-15", "reference": "< 7.0%"},
            "creatinine": {"value": 1.5, "date": "2024-01-15", "reference": "0.7-1.3 mg/dL"},
            "eGFR": {"value": 48, "date": "2024-01-15", "reference": "> 60 mL/min/1.73m²"}
        }
    }
    
    example_current_report = """
    Patient presents for routine follow-up of Type 2 Diabetes and Chronic Kidney Disease.
    
    Current complaints: Increased fatigue over past 2 months, mild peripheral edema.
    
    Vital signs: BP 145/88, HR 78, RR 16, Temp 36.8°C, SpO2 98% on room air, Weight 87kg (up 2kg from 3 months ago)
    
    Recent labs show HbA1c 7.8% (up from 7.2% three months ago), creatinine 1.5 mg/dL (stable), eGFR 48 (down from 52).
    
    Patient reports good medication adherence but admits to dietary indiscretions during holidays.
    """
    
    example_historical_reports = [
        "2023-10-15: Patient stable, HbA1c 7.2%, eGFR 52, BP well controlled on current regimen.",
        "2023-07-10: Added Lisinopril for renal protection. Patient educated on diabetic diet."
    ]
    
    example_imaging = [
        {
            "study": "Renal Ultrasound",
            "date": "2023-11-20",
            "findings": "Bilateral kidneys normal size, increased echogenicity consistent with medical renal disease, no hydronephrosis",
            "impression": "Findings consistent with chronic kidney disease"
        }
    ]
    
    print("="*70)
    print("EXAMPLE: Running Patient Progress Analysis Pipeline")
    print("="*70)
    
    # Run full pipeline
    results = patientProgressAnalysisPipeline(
        patient_id=example_patient_id,
        ehr_summary=example_ehr,
        current_report=example_current_report,
        historical_reports=example_historical_reports,
        imaging_data=example_imaging,
        include_detailed_logs=True
    )
    
    print("\n" + "="*70)
    print("EXAMPLE RESULTS SUMMARY")
    print("="*70)
    print(f"Patient ID: {results['patient_id']}")
    print(f"Status: {results['pipeline_status']}")
    print(f"\nExecutive Summary:")
    print(json.dumps(results['executive_summary'], indent=2))
    
    # Demonstrate quick version
    print("\n\n" + "="*70)
    print("EXAMPLE: Running Quick Version")
    print("="*70)
    
    quick_results = patientProgressAnalysisPipelineQuick(
        patient_id=example_patient_id,
        ehr_summary=example_ehr,
        current_report=example_current_report,
        historical_reports=example_historical_reports,
        imaging_data=example_imaging
    )
    
    print(f"\nQuick Results - Patient {quick_results['patient_id']}:")
    print(f"Status: {quick_results['pipeline_status']}")
