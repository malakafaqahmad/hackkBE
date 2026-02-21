"""
Patient Data Manager Module

Provides centralized functions to load and save patient-specific data files.

Quick Usage:
    from ehr_store.patientdata import load_daily_logs, save_daily_logs
    
    logs = load_daily_logs("p1")
    save_daily_logs("p1", logs)
"""

from .data_manager import (
    # Load functions
    load_conversation,
    load_daily_logs,
    load_diet,
    load_exercise,
    load_firstaid,
    load_report,
    load_twin_state,
    load_twin_forecast,
    load_twin_forecast_contra,
    
    # Save functions
    save_conversation,
    save_daily_logs,
    save_diet,
    save_exercise,
    save_firstaid,
    save_report,
    save_twin_state,
    save_twin_forecast,
    save_twin_forecast_contra,
    
    # Special functions
    append_daily_log,
    
    # Utility functions
    get_all_patient_data,
    patient_data_exists,
    list_all_patients,
    delete_patient_data,
    
    # Convenience aliases
    get_conversation,
    set_conversation,
    get_daily_logs,
    set_daily_logs,
    get_diet,
    set_diet,
    get_exercise,
    set_exercise,
    get_firstaid,
    set_firstaid,
    get_report,
    set_report,
    get_twin_state,
    set_twin_state,
    get_twin_forecast,
    set_twin_forecast,
    get_twin_forecast_contra,
    set_twin_forecast_contra,
)

__all__ = [
    # Load functions
    'load_conversation',
    'load_daily_logs',
    'load_diet',
    'load_exercise',
    'load_firstaid',
    'load_report',
    'load_twin_state',
    'load_twin_forecast',
    'load_twin_forecast_contra',
    
    # Save functions
    'save_conversation',
    'save_daily_logs',
    'save_diet',
    'save_exercise',
    'save_firstaid',
    'save_report',
    'save_twin_state',
    'save_twin_forecast',
    'save_twin_forecast_contra',
    
    # Special functions
    'append_daily_log',
    
    # Utility functions
    'get_all_patient_data',
    'patient_data_exists',
    'list_all_patients',
    'delete_patient_data',
    
    # Convenience aliases
    'get_conversation',
    'set_conversation',
    'get_daily_logs',
    'set_daily_logs',
    'get_diet',
    'set_diet',
    'get_exercise',
    'set_exercise',
    'get_firstaid',
    'set_firstaid',
    'get_report',
    'set_report',
    'get_twin_state',
    'set_twin_state',
    'get_twin_forecast',
    'set_twin_forecast',
    'get_twin_forecast_contra',
    'set_twin_forecast_contra',
]

__version__ = '1.0.0'
__author__ = 'Healthcare System'
