"""
First Aid Emergency Response Agents

This package contains specialized AI agents for emergency first-aid detection,
assessment, and response planning.

Agents:
- emergency_risk_analyzer: Analyzes patient EHR for immediate emergency risks
- red_flag_detector: Identifies critical red flags requiring immediate attention
- first_aid_prescriptor: Generates actionable first-aid instructions
- contraindication_safety: Validates interventions against patient contraindications
- escalation_agent: Determines escalation level and notification requirements
- event_logger: Logs emergency events for audit trail
- validation_agent: Validates entire emergency response plan
- final_reporter: Generates comprehensive emergency report

Pipeline:
The complete workflow is orchestrated in orchestrations/first_aid_pipeline.py
"""

__version__ = "1.0.0"
__author__ = "Emergency Response AI Team"

from .emergency_risk_analyzer import emergencyRiskAnalyzer
from .red_flag_detector import redFlagDetector
from .first_aid_prescriptor import firstAidPrescriptor
from .contraindication_safety import contraindicationSafetyChecker
from .escalation_agent import escalationAgent
from .event_logger import eventLogger
from .validation_agent import validationAgent
from .final_reporter import finalReporter

__all__ = [
    'emergencyRiskAnalyzer',
    'redFlagDetector',
    'firstAidPrescriptor',
    'contraindicationSafetyChecker',
    'escalationAgent',
    'eventLogger',
    'validationAgent',
    'finalReporter'
]
