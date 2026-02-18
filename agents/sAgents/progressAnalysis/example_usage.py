"""
Example Usage and Testing for Patient Progress Analysis System

This file demonstrates how to use the patient progress analysis pipeline
with realistic example data.
"""

from orchestrations.patient_progress_analysis_pipeline import (
    patientProgressAnalysisPipeline,
    patientProgressAnalysisPipelineQuick
)
import json


def example_basic_usage():
    """
    Basic example: Diabetes patient with kidney disease follow-up
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Usage - Type 2 Diabetes with CKD Follow-up")
    print("="*80)
    
    patient_id = "P001234"
    
    # EHR Summary
    ehr_summary = {
        "demographics": {
            "name": "John Doe",
            "age": 65,
            "sex": "Male",
            "weight_kg": 85,
            "height_cm": 175,
            "bmi": 27.8
        },
        "diagnoses": [
            {
                "condition": "Type 2 Diabetes Mellitus",
                "onset": "2018-03-15",
                "icd10": "E11.9",
                "status": "active"
            },
            {
                "condition": "Essential Hypertension",
                "onset": "2015-06-20",
                "icd10": "I10",
                "status": "active"
            },
            {
                "condition": "Chronic Kidney Disease Stage 3",
                "onset": "2020-09-10",
                "icd10": "N18.3",
                "status": "active"
            }
        ],
        "medications": [
            {
                "name": "Metformin",
                "dose": "1000mg",
                "frequency": "BID",
                "route": "PO",
                "indication": "Type 2 Diabetes",
                "start_date": "2018-03-15"
            },
            {
                "name": "Lisinopril",
                "dose": "20mg",
                "frequency": "Daily",
                "route": "PO",
                "indication": "Hypertension, renal protection",
                "start_date": "2015-06-20"
            },
            {
                "name": "Atorvastatin",
                "dose": "40mg",
                "frequency": "Daily",
                "route": "PO",
                "indication": "Hyperlipidemia",
                "start_date": "2019-01-10"
            }
        ],
        "allergies": [
            {
                "allergen": "Penicillin",
                "reaction": "Rash",
                "severity": "Moderate"
            }
        ],
        "labs_recent": {
            "date": "2024-01-15",
            "results": {
                "HbA1c": {
                    "value": 7.8,
                    "unit": "%",
                    "reference": "< 7.0%",
                    "status": "High"
                },
                "glucose_fasting": {
                    "value": 145,
                    "unit": "mg/dL",
                    "reference": "70-100 mg/dL",
                    "status": "High"
                },
                "creatinine": {
                    "value": 1.5,
                    "unit": "mg/dL",
                    "reference": "0.7-1.3 mg/dL",
                    "status": "High"
                },
                "eGFR": {
                    "value": 48,
                    "unit": "mL/min/1.73m²",
                    "reference": "> 60 mL/min/1.73m²",
                    "status": "Low"
                },
                "potassium": {
                    "value": 4.8,
                    "unit": "mmol/L",
                    "reference": "3.5-5.0 mmol/L",
                    "status": "Normal"
                },
                "hemoglobin": {
                    "value": 11.2,
                    "unit": "g/dL",
                    "reference": "13.5-17.5 g/dL",
                    "status": "Low"
                }
            }
        },
        "vitals_recent": {
            "blood_pressure": "145/88",
            "heart_rate": 78,
            "respiratory_rate": 16,
            "temperature": 36.8,
            "oxygen_saturation": 98,
            "weight_kg": 87
        }
    }
    
    # Current Clinical Report
    current_report = """
    CHIEF COMPLAINT:
    Patient presents for routine follow-up of Type 2 Diabetes Mellitus and Chronic Kidney Disease.
    
    HISTORY OF PRESENT ILLNESS:
    65-year-old male with established Type 2 Diabetes (6 years), hypertension (9 years), 
    and CKD Stage 3 (4 years) presents for quarterly follow-up.
    
    Patient reports increased fatigue over the past 2 months, rating 6/10 severity. 
    Notes mild bilateral lower extremity edema, worse at end of day. 
    Denies chest pain, shortness of breath, or orthopnea.
    
    Reports good medication adherence but admits to dietary indiscretions during the holiday season, 
    particularly increased carbohydrate intake and sodium consumption.
    
    No hypoglycemic episodes. No changes in vision. No foot ulcers or wounds.
    
    PHYSICAL EXAMINATION:
    - General: Alert, oriented, appears stated age, mildly fatigued
    - Vital Signs: BP 145/88 mmHg, HR 78 bpm regular, RR 16/min, Temp 36.8°C, SpO2 98% on RA
    - Weight: 87 kg (increased 2 kg from 3 months ago)
    - HEENT: Fundoscopic exam shows early diabetic retinopathy changes
    - Cardiovascular: Regular rate and rhythm, no murmurs
    - Respiratory: Clear to auscultation bilaterally
    - Abdomen: Soft, non-tender, no organomegaly
    - Extremities: 1+ bilateral pitting edema to ankles, pedal pulses intact
    - Skin: No diabetic foot ulcers, good foot care
    - Neurological: Intact, mild diminished sensation in feet (known peripheral neuropathy)
    
    LABORATORY REVIEW:
    Recent labs from 2024-01-15 show:
    - HbA1c 7.8% (up from 7.2% three months ago) - suboptimal control
    - Fasting glucose 145 mg/dL
    - Creatinine 1.5 mg/dL (stable from prior)
    - eGFR 48 mL/min/1.73m² (down from 52 three months ago) - concerning trend
    - Potassium 4.8 mmol/L (acceptable on ACE inhibitor)
    - Hemoglobin 11.2 g/dL (mild anemia, likely anemia of CKD)
    
    ASSESSMENT:
    1. Type 2 Diabetes Mellitus - suboptimal control with rising HbA1c
    2. Chronic Kidney Disease Stage 3 - stable creatinine but declining eGFR
    3. Essential Hypertension - borderline control
    4. Anemia of chronic kidney disease - mild
    5. Diabetic retinopathy - early changes
    6. Diabetic peripheral neuropathy - stable
    7. Volume overload - mild, contributing to edema
    """
    
    # Historical Reports
    historical_reports = [
        """
        2023-10-15 Visit Note:
        Patient stable overall. HbA1c 7.2%, eGFR 52. Blood pressure well controlled on current regimen.
        Continues Metformin 1000mg BID, Lisinopril 20mg daily, Atorvastatin 40mg daily.
        Encouraged continued dietary adherence and regular exercise.
        Follow-up in 3 months with labs.
        """,
        """
        2023-07-10 Visit Note:
        Follow-up for diabetes and newly diagnosed CKD Stage 3. 
        Lisinopril increased from 10mg to 20mg daily for renal protection.
        Patient educated on diabetic diet and importance of glycemic control for kidney health.
        Referral to nephrology for CKD management evaluation.
        """,
        """
        2023-04-05 Visit Note:
        Annual comprehensive visit. HbA1c 7.4%. 
        New finding of decreased eGFR to 55, concerning for developing CKD.
        Will monitor closely. Continue current medications.
        Order renal ultrasound to evaluate kidney structure.
        """
    ]
    
    # Imaging Data
    imaging_data = [
        {
            "study": "Renal Ultrasound",
            "date": "2023-11-20",
            "modality": "Ultrasound",
            "indication": "Chronic kidney disease evaluation",
            "findings": """
                Right kidney: 10.2 cm length, normal cortical thickness, increased echogenicity
                Left kidney: 10.0 cm length, normal cortical thickness, increased echogenicity
                No hydronephrosis bilaterally
                No renal masses or stones identified
                Bladder: Normal, post-void residual < 50 mL
            """,
            "impression": "Bilateral increased renal echogenicity consistent with medical renal disease (chronic kidney disease). No obstructive uropathy.",
            "radiologist": "Dr. Sarah Johnson"
        },
        {
            "study": "Chest X-ray",
            "date": "2023-05-10",
            "modality": "X-ray",
            "indication": "Pre-operative evaluation",
            "findings": "Clear lungs, normal heart size, no acute cardiopulmonary process",
            "impression": "Normal chest radiograph",
            "radiologist": "Dr. Michael Chen"
        }
    ]
    
    # Run the full pipeline
    print("\n🔄 Running Full Pipeline...")
    results = patientProgressAnalysisPipeline(
        patient_id=patient_id,
        ehr_summary=ehr_summary,
        current_report=current_report,
        historical_reports=historical_reports,
        imaging_data=imaging_data,
        include_detailed_logs=True
    )
    
    # Display key results
    print("\n" + "="*80)
    print("RESULTS SUMMARY")
    print("="*80)
    print(f"\nPatient ID: {results['patient_id']}")
    print(f"Pipeline Status: {results['pipeline_status']}")
    print(f"Analysis Timestamp: {results['analysis_timestamp']}")
    
    if results['pipeline_status'] == 'completed':
        print("\n✅ Pipeline completed successfully!")
        
        # Show executive summary
        print("\n" + "-"*80)
        print("EXECUTIVE SUMMARY")
        print("-"*80)
        print(json.dumps(results['executive_summary'], indent=2))
        
        # Provide access instructions
        print("\n" + "-"*80)
        print("ACCESS DETAILED OUTPUTS")
        print("-"*80)
        print("• Aggregated Data: results['aggregated_data']")
        print("• Current Status: results['current_status']")
        print("• Progress Assessment: results['progress_assessment']")
        print("• Imaging Interpretation: results['imaging_interpretation']")
        print("• Clinical Report: results['clinical_report']")
        print("• Alerts & Recommendations: results['alerts_recommendations']")
        
    else:
        print("\n❌ Pipeline failed!")
        print(f"Error: {results.get('error', {}).get('message', 'Unknown error')}")
    
    return results


def example_quick_usage():
    """
    Quick version example: Returns only report and alerts
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: Quick Usage - Returns Only Report and Alerts")
    print("="*80)
    
    # Simplified example data
    patient_id = "P005678"
    
    ehr_summary = {
        "demographics": {"age": 72, "sex": "Female", "weight_kg": 68},
        "diagnoses": [
            {"condition": "Hypertension", "icd10": "I10"},
            {"condition": "Atrial Fibrillation", "icd10": "I48.91"}
        ],
        "medications": [
            {"name": "Metoprolol", "dose": "50mg", "frequency": "BID"},
            {"name": "Warfarin", "dose": "5mg", "frequency": "Daily"}
        ],
        "labs_recent": {
            "INR": {"value": 3.5, "reference": "2.0-3.0", "status": "High"}
        }
    }
    
    current_report = "Patient presents for INR check. No bleeding. INR elevated at 3.5."
    
    print("\n🔄 Running Quick Pipeline...")
    quick_results = patientProgressAnalysisPipelineQuick(
        patient_id=patient_id,
        ehr_summary=ehr_summary,
        current_report=current_report
    )
    
    print("\n" + "="*80)
    print("QUICK RESULTS")
    print("="*80)
    print(f"Patient ID: {quick_results['patient_id']}")
    print(f"Status: {quick_results['pipeline_status']}")
    print("\nNote: Quick version returns only clinical_report, alerts_recommendations, and executive_summary")
    
    return quick_results


def example_with_minimal_data():
    """
    Example with minimal required data
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: Minimal Data - Only Required Fields")
    print("="*80)
    
    patient_id = "P009999"
    
    # Minimal EHR data
    ehr_summary = {
        "demographics": {"age": 45, "sex": "Male"},
        "diagnoses": [{"condition": "Hypertension", "icd10": "I10"}],
        "medications": [{"name": "Lisinopril", "dose": "10mg", "frequency": "Daily"}]
    }
    
    # Minimal current report
    current_report = "Patient presents for blood pressure check. BP 138/82. Feeling well."
    
    print("\n🔄 Running Pipeline with Minimal Data...")
    results = patientProgressAnalysisPipelineQuick(
        patient_id=patient_id,
        ehr_summary=ehr_summary,
        current_report=current_report
        # Note: historical_reports and imaging_data are optional
    )
    
    print(f"\nStatus: {results['pipeline_status']}")
    print("Pipeline can run with minimal data, though more complete data provides better analysis.")
    
    return results


def main():
    """
    Run all examples
    """
    print("\n" + "="*80)
    print("PATIENT PROGRESS ANALYSIS SYSTEM - EXAMPLE USAGE")
    print("="*80)
    print("\nThis script demonstrates various usage patterns of the system.")
    print("Each example shows different scenarios and data completeness levels.")
    
    # Example 1: Full detailed usage
    example1_results = example_basic_usage()
    
    # Example 2: Quick version
    example2_results = example_quick_usage()
    
    # Example 3: Minimal data
    example3_results = example_with_minimal_data()
    
    print("\n" + "="*80)
    print("ALL EXAMPLES COMPLETED")
    print("="*80)
    print("\nYou can now:")
    print("1. Examine the results objects returned by each example")
    print("2. Modify the example data to test different scenarios")
    print("3. Integrate the pipeline into your application")
    print("\nSee README.md for complete documentation.")
    print("="*80 + "\n")


if __name__ == "__main__":
    """
    Run examples when script is executed directly
    """
    main()
