"""
Medicine Double Checker Agents

Comprehensive medication safety verification system that validates prescribed medications
against patient's current condition, past history, and clinical guidelines.

Agents:
--------
1. patient_summary_agent: Extracts patient clinical data (demographics, organ function, medications, allergies)
2. prescription_parser_agent: Parses and standardizes prescription data
3. contraindication_agent: Identifies drug contraindications (absolute/relative)
4. interaction_agent: Analyzes drug-drug, drug-food, drug-disease interactions
5. dose_safety_agent: Verifies dosing appropriateness for patient-specific factors
6. clinical_appropriateness_agent: Evaluates clinical appropriateness per evidence-based guidelines
7. risk_aggregation_agent: Aggregates all safety findings into overall risk assessment
8. final_reporter_agent: Generates comprehensive Medicine Safety Report with APPROVE/DISAPPROVE decision

Pipeline:
---------
Use the medicine_double_check_pipeline to orchestrate all agents:

    from orchestrations.medicine_double_check_pipeline import medicineDoubleCheckPipeline
    
    report = medicineDoubleCheckPipeline(
        patient_id="P12345",
        ehr_summary=patient_ehr_data,
        current_report="detailed condition report",
        prescription_data={
            "medications": [...],
            "prescriber": "Dr. Name",
            "date": "2024-01-15"
        }
    )

Output:
-------
Returns comprehensive safety report with:
- Clear APPROVE/DISAPPROVE decision
- Detailed safety analysis (contraindications, interactions, dosing)
- Clinical appropriateness assessment
- Risk-benefit analysis
- Specific recommendations for prescriber, pharmacist, patient, clinical team
- Alternatives for disapproved medications
- Monitoring requirements
"""

from .patient_summary_agent import patientSummaryAgent
from .prescription_parser_agent import prescriptionParserAgent
from .contraindication_agent import contraindicationAgent
from .interaction_agent import interactionAgent
from .dose_safety_agent import doseSafetyAgent
from .clinical_appropriateness_agent import clinicalAppropriatenessAgent
from .risk_aggregation_agent import riskAggregationAgent
from .final_reporter_agent import finalReporterAgent

__all__ = [
    'patientSummaryAgent',
    'prescriptionParserAgent',
    'contraindicationAgent',
    'interactionAgent',
    'doseSafetyAgent',
    'clinicalAppropriatenessAgent',
    'riskAggregationAgent',
    'finalReporterAgent'
]
