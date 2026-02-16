"""
Medicine Double Checker Pipeline

Validates prescribed medications against patient's current condition and past history.
Provides comprehensive safety assessment with clear APPROVE/DISAPPROVE decision.

Pipeline Flow:
1. Patient Summary → Extract clinical data
2. Prescription Parser → Structure prescription data
3. Contraindication Agent → Check contraindications
4. Interaction Agent → Check drug interactions
5. Dose Safety Agent → Verify dosing appropriateness
6. Clinical Appropriateness Agent → Evaluate clinical appropriateness
7. Risk Aggregation Agent → Aggregate all risks
8. Final Reporter Agent → Generate medicine safety report

Usage:
    from orchestrations.medicine_double_check_pipeline import medicineDoubleCheckPipeline
    
    report = medicineDoubleCheckPipeline(
        patient_id="P12345",
        ehr_summary=ehr_data,
        current_report="detailed patient condition report",
        prescription_data={
            "medications": [
                {
                    "name": "Metformin",
                    "dose": "1000mg",
                    "frequency": "BID",
                    "route": "PO",
                    "indication": "Type 2 Diabetes"
                }
            ],
            "prescriber": "Dr. Smith",
            "date": "2024-01-15"
        }
    )
"""

from agents.sAgents.medicineDoubleChecker.patient_summary_agent import patientSummaryAgent
from agents.sAgents.medicineDoubleChecker.prescription_parser_agent import prescriptionParserAgent
from agents.sAgents.medicineDoubleChecker.contraindication_agent import contraindicationAgent
from agents.sAgents.medicineDoubleChecker.interaction_agent import interactionAgent
from agents.sAgents.medicineDoubleChecker.dose_safety_agent import doseSafetyAgent
from agents.sAgents.medicineDoubleChecker.clinical_appropriateness_agent import clinicalAppropriatenessAgent
from agents.sAgents.medicineDoubleChecker.risk_aggregation_agent import riskAggregationAgent
from agents.sAgents.medicineDoubleChecker.final_reporter_agent import finalReporterAgent
import json


def medicineDoubleCheckPipeline(patient_id, ehr_summary, current_report, prescription_data):
    """
    Orchestrates comprehensive medication safety verification.
    
    Args:
        patient_id: Unique patient identifier
        ehr_summary: Complete EHR data from get_ehr_summary()
        current_report: Detailed report of patient's current condition
        prescription_data: Structured prescription information
    
    Returns:
        dict: Complete medicine safety report with APPROVE/DISAPPROVE decision
    """
    
    print("\n" + "="*80)
    print("🔍 MEDICINE DOUBLE CHECKER PIPELINE")
    print("="*80)
    print(f"Patient ID: {patient_id}")
    print(f"Prescription contains: {len(prescription_data.get('medications', []))} medication(s)")
    print("="*80 + "\n")
    
    results = {}
    
    # Step 1: Patient Summary
    print("📋 Step 1/8: Extracting Patient Clinical Summary...")
    try:
        patient_summary = patientSummaryAgent(patient_id, ehr_summary, current_report)
        results['patient_summary'] = patient_summary
        print("✓ Patient summary extracted")
        print(f"   Key factors: Demographics, organ function, current medications")
    except Exception as e:
        print(f"✗ Error in patient summary: {e}")
        return {"error": "Patient summary failed", "details": str(e)}
    
    # Step 2: Prescription Parser
    print("\n💊 Step 2/8: Parsing Prescription Data...")
    try:
        parsed_prescription = prescriptionParserAgent(prescription_data)
        results['parsed_prescription'] = parsed_prescription
        print("✓ Prescription parsed and standardized")
        print(f"   High-alert medications identified: {parsed_prescription.count('high_alert_medication')}")
    except Exception as e:
        print(f"✗ Error in prescription parsing: {e}")
        return {"error": "Prescription parsing failed", "details": str(e)}
    
    # Step 3: Contraindication Check
    print("\n⚠️  Step 3/8: Checking Contraindications...")
    try:
        contraindication = contraindicationAgent(patient_summary, parsed_prescription)
        results['contraindication'] = contraindication
        
        # Count critical contraindications
        absolute_count = contraindication.count('"type": "ABSOLUTE"')
        relative_count = contraindication.count('"type": "RELATIVE"')
        
        print("✓ Contraindication analysis complete")
        print(f"   Absolute contraindications: {absolute_count}")
        print(f"   Relative contraindications: {relative_count}")
        
        if absolute_count > 0:
            print("   ⚠️  CRITICAL: Absolute contraindications detected!")
    except Exception as e:
        print(f"✗ Error in contraindication check: {e}")
        return {"error": "Contraindication check failed", "details": str(e)}
    
    # Step 4: Drug Interaction Analysis
    print("\n🔄 Step 4/8: Analyzing Drug Interactions...")
    try:
        interactions = interactionAgent(patient_summary, parsed_prescription)
        results['interactions'] = interactions
        
        # Count interaction severities
        contraindicated = interactions.count('"severity": "CONTRAINDICATED"')
        major = interactions.count('"severity": "MAJOR"')
        moderate = interactions.count('"severity": "MODERATE"')
        
        print("✓ Interaction analysis complete")
        print(f"   Contraindicated interactions: {contraindicated}")
        print(f"   Major interactions: {major}")
        print(f"   Moderate interactions: {moderate}")
        
        if contraindicated > 0:
            print("   ⚠️  CRITICAL: Contraindicated interactions detected!")
    except Exception as e:
        print(f"✗ Error in interaction analysis: {e}")
        return {"error": "Interaction analysis failed", "details": str(e)}
    
    # Step 5: Dose Safety Check
    print("\n💉 Step 5/8: Verifying Dose Safety...")
    try:
        dose_check = doseSafetyAgent(patient_summary, parsed_prescription)
        results['dose_check'] = dose_check
        
        # Check for unsafe doses
        unsafe_count = dose_check.count('"safety_assessment": "UNSAFE"')
        adjustment_count = dose_check.count('"requires_adjustment": true')
        
        print("✓ Dose safety verification complete")
        print(f"   Unsafe doses: {unsafe_count}")
        print(f"   Doses requiring adjustment: {adjustment_count}")
        
        if unsafe_count > 0:
            print("   ⚠️  CRITICAL: Unsafe dosing detected!")
    except Exception as e:
        print(f"✗ Error in dose safety check: {e}")
        return {"error": "Dose safety check failed", "details": str(e)}
    
    # Step 6: Clinical Appropriateness
    print("\n📊 Step 6/8: Evaluating Clinical Appropriateness...")
    try:
        appropriateness = clinicalAppropriatenessAgent(patient_summary, parsed_prescription)
        results['appropriateness'] = appropriateness
        
        # Check appropriateness status
        inappropriate_count = appropriateness.count('"appropriateness": "INAPPROPRIATE"')
        questionable_count = appropriateness.count('"appropriateness": "QUESTIONABLE"')
        
        print("✓ Clinical appropriateness assessed")
        print(f"   Inappropriate prescriptions: {inappropriate_count}")
        print(f"   Questionable prescriptions: {questionable_count}")
        
        if inappropriate_count > 0:
            print("   ⚠️  WARNING: Inappropriate prescribing detected!")
    except Exception as e:
        print(f"✗ Error in appropriateness evaluation: {e}")
        return {"error": "Appropriateness evaluation failed", "details": str(e)}
    
    # Step 7: Risk Aggregation
    print("\n⚖️  Step 7/8: Aggregating Overall Risk Assessment...")
    try:
        risk_aggregation = riskAggregationAgent(
            contraindication,
            interactions,
            dose_check,
            appropriateness,
            patient_summary
        )
        results['risk_aggregation'] = risk_aggregation
        
        # Parse risk level
        if '"prescription_safety_level": "CRITICAL_RISK"' in risk_aggregation:
            print("✓ Risk aggregation complete: ⚠️  CRITICAL RISK")
        elif '"prescription_safety_level": "HIGH_RISK"' in risk_aggregation:
            print("✓ Risk aggregation complete: ⚠️  HIGH RISK")
        elif '"prescription_safety_level": "MODERATE_RISK"' in risk_aggregation:
            print("✓ Risk aggregation complete: ⚠️  MODERATE RISK")
        else:
            print("✓ Risk aggregation complete: ✓ LOW RISK")
        
    except Exception as e:
        print(f"✗ Error in risk aggregation: {e}")
        return {"error": "Risk aggregation failed", "details": str(e)}
    
    # Step 8: Final Report Generation
    print("\n📝 Step 8/8: Generating Medicine Safety Report...")
    try:
        final_report = finalReporterAgent(
            risk_aggregation,
            patient_summary,
            json.dumps(prescription_data),
            contraindication,
            interactions,
            dose_check,
            appropriateness
        )
        results['final_report'] = final_report
        
        # Parse final decision
        if '"overall_determination": "APPROVE"' in final_report and 'APPROVE_WITH' not in final_report:
            decision = "✅ APPROVED"
            decision_color = "green"
        elif '"overall_determination": "APPROVE_WITH_MODIFICATIONS"' in final_report:
            decision = "⚠️  APPROVED WITH MODIFICATIONS"
            decision_color = "yellow"
        else:
            decision = "❌ DISAPPROVED"
            decision_color = "red"
        
        print("✓ Final report generated")
        
    except Exception as e:
        print(f"✗ Error in report generation: {e}")
        return {"error": "Report generation failed", "details": str(e)}
    
    # Pipeline Summary
    print("\n" + "="*80)
    print("MEDICINE SAFETY REPORT - FINAL DECISION")
    print("="*80)
    print(f"Decision: {decision}")
    print("="*80)
    
    # Extract key metrics from final report
    try:
        report_json = json.loads(final_report)
        exec_summary = report_json.get('executive_summary', {})
        stats = exec_summary.get('prescription_statistics', {})
        findings = exec_summary.get('findings_summary', {})
        
        print("\nPrescription Statistics:")
        print(f"  • Total medications reviewed: {stats.get('total_medications_reviewed', 0)}")
        print(f"  • Approved as prescribed: {stats.get('approved_as_prescribed', 0)}")
        print(f"  • Approved with modifications: {stats.get('approved_with_modifications', 0)}")
        print(f"  • Disapproved: {stats.get('disapproved', 0)}")
        
        print("\nSafety Findings:")
        print(f"  • Critical issues: {findings.get('critical_issues', 0)}")
        print(f"  • High priority issues: {findings.get('high_priority_issues', 0)}")
        print(f"  • Moderate issues: {findings.get('moderate_issues', 0)}")
        
        print(f"\nPrimary Reason: {exec_summary.get('primary_reason_for_determination', 'N/A')}")
        
        if exec_summary.get('prescriber_action_required'):
            print("\n⚠️  PRESCRIBER ACTION REQUIRED")
            immediate = exec_summary.get('immediate_action_items', [])
            if immediate:
                print("\nImmediate Actions:")
                for action in immediate[:3]:  # Show first 3
                    print(f"  • {action}")
        
    except:
        pass  # If JSON parsing fails, skip detailed metrics
    
    print("\n" + "="*80)
    print("Pipeline completed successfully")
    print("="*80 + "\n")
    
    return results


# Test Cases
if __name__ == "__main__":
    print("\n" + "="*80)
    print("MEDICINE DOUBLE CHECKER - TEST CASES")
    print("="*80 + "\n")
    
    # Test Case 1: Safe Prescription - Should APPROVE
    print("\n" + "="*80)
    print("TEST CASE 1: SAFE PRESCRIPTION (Expected: APPROVE)")
    print("="*80)
    
    test1_ehr = {
        "patient": {
            "id": "P001",
            "name": "John Smith",
            "age": 55,
            "sex": "M",
            "weight": 80,
            "height": 175
        },
        "conditions": ["Type 2 Diabetes Mellitus", "Hypertension"],
        "allergies": [],
        "current_medications": [],
        "lab_results": {
            "creatinine": 1.0,
            "eGFR": 85,
            "ALT": 25,
            "AST": 28,
            "HbA1c": 8.2,
            "blood_pressure": "145/92"
        }
    }
    
    test1_report = """
Patient presents for routine diabetes management. Type 2 diabetes diagnosed 2 years ago, 
currently uncontrolled with HbA1c 8.2%. Hypertension also present with BP 145/92. 
No complications. Renal function normal (eGFR 85). Liver function normal. 
Patient has been managing with lifestyle modifications alone, now requires medication.
"""
    
    test1_prescription = {
        "prescriber": "Dr. Johnson",
        "date": "2024-01-15",
        "medications": [
            {
                "name": "Metformin",
                "dose": "500mg",
                "frequency": "BID",
                "route": "PO",
                "indication": "Type 2 Diabetes"
            },
            {
                "name": "Lisinopril",
                "dose": "10mg",
                "frequency": "daily",
                "route": "PO",
                "indication": "Hypertension"
            }
        ]
    }
    
    result1 = medicineDoubleCheckPipeline(
        patient_id="P001",
        ehr_summary=test1_ehr,
        current_report=test1_report,
        prescription_data=test1_prescription
    )
    
    # Test Case 2: Contraindication - Should DISAPPROVE
    print("\n\n" + "="*80)
    print("TEST CASE 2: ABSOLUTE CONTRAINDICATION (Expected: DISAPPROVE)")
    print("="*80)
    
    test2_ehr = {
        "patient": {
            "id": "P002",
            "name": "Sarah Williams",
            "age": 45,
            "sex": "F",
            "weight": 65,
            "height": 165
        },
        "conditions": ["Community-Acquired Pneumonia"],
        "allergies": [
            {
                "allergen": "Penicillin",
                "reaction": "Anaphylaxis",
                "severity": "severe",
                "date": "2020-03-15"
            }
        ],
        "current_medications": [],
        "lab_results": {
            "creatinine": 0.9,
            "eGFR": 90,
            "WBC": 14500
        }
    }
    
    test2_report = """
45-year-old female presents with community-acquired pneumonia. Symptoms include fever,
productive cough, shortness of breath for 3 days. Chest X-ray confirms right lower lobe
infiltrate. CRITICAL HISTORY: Patient has documented penicillin anaphylaxis from 2020.
Requires alternative antibiotic therapy.
"""
    
    test2_prescription = {
        "prescriber": "Dr. Martinez",
        "date": "2024-01-15",
        "medications": [
            {
                "name": "Amoxicillin",
                "dose": "500mg",
                "frequency": "TID",
                "route": "PO",
                "indication": "Pneumonia"
            }
        ]
    }
    
    result2 = medicineDoubleCheckPipeline(
        patient_id="P002",
        ehr_summary=test2_ehr,
        current_report=test2_report,
        prescription_data=test2_prescription
    )
    
    # Test Case 3: Multiple Issues - Should APPROVE WITH MODIFICATIONS
    print("\n\n" + "="*80)
    print("TEST CASE 3: MULTIPLE SAFETY CONCERNS (Expected: APPROVE WITH MODIFICATIONS)")
    print("="*80)
    
    test3_ehr = {
        "patient": {
            "id": "P003",
            "name": "Robert Chen",
            "age": 72,
            "sex": "M",
            "weight": 75,
            "height": 170
        },
        "conditions": [
            "Atrial Fibrillation",
            "Chronic Kidney Disease Stage 3",
            "Osteoarthritis"
        ],
        "allergies": [],
        "current_medications": [
            {
                "name": "Warfarin",
                "dose": "5mg",
                "frequency": "daily"
            }
        ],
        "lab_results": {
            "creatinine": 1.8,
            "eGFR": 38,
            "INR": 2.5
        }
    }
    
    test3_report = """
72-year-old male with atrial fibrillation on warfarin (INR therapeutic at 2.5). 
Also has CKD stage 3 with eGFR 38 ml/min. Presents with worsening knee osteoarthritis pain.
Currently on warfarin for stroke prevention. Renal function impaired requiring dose
adjustments for renally-cleared medications. Patient reports pain limiting mobility.
"""
    
    test3_prescription = {
        "prescriber": "Dr. Thompson",
        "date": "2024-01-15",
        "medications": [
            {
                "name": "Ibuprofen",
                "dose": "600mg",
                "frequency": "TID",
                "route": "PO",
                "indication": "Osteoarthritis pain"
            },
            {
                "name": "Metformin",
                "dose": "1000mg",
                "frequency": "BID",
                "route": "PO",
                "indication": "Type 2 Diabetes"
            }
        ]
    }
    
    result3 = medicineDoubleCheckPipeline(
        patient_id="P003",
        ehr_summary=test3_ehr,
        current_report=test3_report,
        prescription_data=test3_prescription
    )
    
    print("\n" + "="*80)
    print("ALL TEST CASES COMPLETED")
    print("="*80)
    print("\nTest Case 1: Safe prescription → Should APPROVE")
    print("Test Case 2: Penicillin allergy + Amoxicillin → Should DISAPPROVE")
    print("Test Case 3: NSAID+Warfarin + Metformin+CKD → Should APPROVE WITH MODIFICATIONS")
    print("="*80 + "\n")
