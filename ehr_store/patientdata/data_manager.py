"""
Patient Data Loader/Saver Module

Provides centralized functions to load and save patient-specific data files.
All files follow the naming pattern: {patient_id}_{data_type}.json

Usage:
    from ehr_store.patientdata.data_manager import (
        load_conversation, save_conversation,
        load_daily_logs, save_daily_logs,
        load_diet, save_diet,
        # ... etc
    )
    
    # Load data
    conversation = load_conversation("p1")
    
    # Save data
    save_conversation("p1", conversation_data)
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from datetime import datetime


# Base directory for patient data
PATIENT_DATA_DIR = Path(__file__).parent


def _get_file_path(patient_id: str, data_type: str) -> Path:
    """
    Get the file path for a specific patient data file.
    
    Args:
        patient_id: Patient identifier (e.g., "p1", "p2")
        data_type: Type of data (e.g., "conversation", "daily_logs")
    
    Returns:
        Path: Full path to the data file
    """
    filename = f"{patient_id}_{data_type}.json"
    return PATIENT_DATA_DIR / filename


def _load_json(patient_id: str, data_type: str, default: Any = None) -> Any:
    """
    Generic function to load JSON data from a patient file.
    
    Args:
        patient_id: Patient identifier
        data_type: Type of data to load
        default: Default value to return if file doesn't exist or is empty
    
    Returns:
        Loaded data or default value
    """
    file_path = _get_file_path(patient_id, data_type)
    
    try:
        if not file_path.exists():
            print(f"⚠️  File not found: {file_path}, returning default value")
            return default if default is not None else {}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                print(f"⚠️  File is empty: {file_path}, returning default value")
                return default if default is not None else {}
            
            data = json.loads(content)
            return data
            
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error in {file_path}: {e}")
        return default if default is not None else {}
    except Exception as e:
        print(f"❌ Error loading {file_path}: {e}")
        return default if default is not None else {}


def _save_json(patient_id: str, data_type: str, data: Any, create_backup: bool = True) -> bool:
    """
    Generic function to save JSON data to a patient file.
    
    Args:
        patient_id: Patient identifier
        data_type: Type of data to save
        data: Data to save (will be JSON serialized)
        create_backup: Whether to create a backup of existing file
    
    Returns:
        bool: True if save was successful, False otherwise
    """
    file_path = _get_file_path(patient_id, data_type)
    
    try:
        # Create backup if file exists and backup is requested
        if create_backup and file_path.exists():
            backup_path = file_path.with_suffix(f'.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
            try:
                import shutil
                shutil.copy2(file_path, backup_path)
            except Exception as e:
                print(f"⚠️  Could not create backup: {e}")
        
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write data
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
        
    except Exception as e:
        print(f"❌ Error saving to {file_path}: {e}")
        return False


# ============================================================================
# CONVERSATION DATA
# ============================================================================

def load_conversation(patient_id: str) -> List[Dict[str, Any]]:
    """
    Load conversation history for a patient.
    
    Args:
        patient_id: Patient identifier (e.g., "p1")
    
    Returns:
        List of conversation messages (empty list if not found)
    
    Example:
        >>> conversation = load_conversation("p1")
        >>> print(conversation)
        [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi"}]
    """
    return _load_json(patient_id, "conversation", default=[])


def save_conversation(patient_id: str, conversation: List[Dict[str, Any]], create_backup: bool = True) -> bool:
    """
    Save conversation history for a patient.
    
    Args:
        patient_id: Patient identifier
        conversation: List of conversation messages
        create_backup: Whether to create a backup of existing file
    
    Returns:
        bool: True if save was successful
    
    Example:
        >>> messages = [{"role": "user", "content": "Hello"}]
        >>> save_conversation("p1", messages)
        True
    """
    return _save_json(patient_id, "conversation", conversation, create_backup)


# ============================================================================
# DAILY LOGS DATA
# ============================================================================

def load_daily_logs(patient_id: str) -> List[Dict[str, Any]]:
    """
    Load daily health logs for a patient.
    
    Args:
        patient_id: Patient identifier
    
    Returns:
        List of daily log entries (empty list if not found)
    
    Example:
        >>> logs = load_daily_logs("p1")
        >>> print(logs[0])
        {
            "day": 1,
            "diet": {"morning": [...], "lunch": [...], "dinner": [...]},
            "exercise_minutes": 30,
            "medications_taken": [...],
            "vitals": {...},
            "labs": {...},
            "symptoms": []
        }
    """
    return _load_json(patient_id, "daily_logs", default=[])


def save_daily_logs(patient_id: str, daily_logs: List[Dict[str, Any]], create_backup: bool = True) -> bool:
    """
    Save daily health logs for a patient.
    
    Args:
        patient_id: Patient identifier
        daily_logs: List of daily log entries
        create_backup: Whether to create a backup
    
    Returns:
        bool: True if save was successful
    """
    return _save_json(patient_id, "daily_logs", daily_logs, create_backup)


def append_daily_log(patient_id: str, log_entry: Dict[str, Any]) -> bool:
    """
    Append a single daily log entry to existing logs.
    
    Args:
        patient_id: Patient identifier
        log_entry: New log entry to append
    
    Returns:
        bool: True if append was successful
    
    Example:
        >>> new_log = {"day": 2, "vitals": {...}, ...}
        >>> append_daily_log("p1", new_log)
        True
    """
    logs = load_daily_logs(patient_id)
    logs.append(log_entry)
    return save_daily_logs(patient_id, logs, create_backup=False)


def get_recent_daily_logs(patient_id: str, number_of_days: int) -> List[Dict[str, Any]]:
    """
    Fetch the last N days of daily logs for a patient.
    
    Args:
        patient_id: Patient identifier (e.g., "p1", "p2")
        number_of_days: Number of recent days to retrieve
    
    Returns:
        List of the most recent daily log entries (up to number_of_days)
        Returns empty list if file doesn't exist or no logs available
    
    Example:
        >>> # Get last 7 days of logs for patient p1
        >>> recent_logs = get_recent_daily_logs("p1", 7)
        >>> print(f"Retrieved {len(recent_logs)} days of logs")
        Retrieved 7 days of logs
        
        >>> # Get last 3 days only
        >>> last_3_days = get_recent_daily_logs("p1", 3)
        >>> for log in last_3_days:
        ...     print(f"Day {log['day']}: BP {log['vitals']['SBP']}/{log['vitals']['DBP']}")
    """
    # Load all daily logs for the patient
    all_logs = load_daily_logs(patient_id)
    
    # Return the last N entries
    # If number_of_days is greater than available logs, return all logs
    if not all_logs:
        return []
    
    return all_logs[-number_of_days:] if number_of_days > 0 else []


# ============================================================================
# DIET DATA
# ============================================================================

def load_diet(patient_id: str) -> Dict[str, Any]:
    """
    Load diet plan/history for a patient.
    
    Args:
        patient_id: Patient identifier
    
    Returns:
        Dict containing diet information (empty dict if not found)
    
    Example:
        >>> diet = load_diet("p1")
        >>> print(diet)
        {"meal_plan": [...], "restrictions": [...], ...}
    """
    return _load_json(patient_id, "diet", default={})


def save_diet(patient_id: str, diet_data: Dict[str, Any], create_backup: bool = True) -> bool:
    """
    Save diet plan/history for a patient.
    
    Args:
        patient_id: Patient identifier
        diet_data: Diet information to save
        create_backup: Whether to create a backup
    
    Returns:
        bool: True if save was successful
    """
    return _save_json(patient_id, "diet", diet_data, create_backup)


# ============================================================================
# EXERCISE DATA
# ============================================================================

def load_exercise(patient_id: str) -> Dict[str, Any]:
    """
    Load exercise plan/history for a patient.
    
    Args:
        patient_id: Patient identifier
    
    Returns:
        Dict containing exercise information (empty dict if not found)
    
    Example:
        >>> exercise = load_exercise("p1")
        >>> print(exercise)
        {"workout_plan": [...], "restrictions": [...], ...}
    """
    return _load_json(patient_id, "exercize", default={})


def save_exercise(patient_id: str, exercise_data: Dict[str, Any], create_backup: bool = True) -> bool:
    """
    Save exercise plan/history for a patient.
    
    Args:
        patient_id: Patient identifier
        exercise_data: Exercise information to save
        create_backup: Whether to create a backup
    
    Returns:
        bool: True if save was successful
    """
    return _save_json(patient_id, "exercize", exercise_data, create_backup)


# ============================================================================
# FIRST AID DATA
# ============================================================================

def load_firstaid(patient_id: str) -> Dict[str, Any]:
    """
    Load first aid history/guidance for a patient.
    
    Args:
        patient_id: Patient identifier
    
    Returns:
        Dict containing first aid information (empty dict if not found)
    
    Example:
        >>> firstaid = load_firstaid("p1")
        >>> print(firstaid)
        {"incidents": [...], "guidance": [...], ...}
    """
    return _load_json(patient_id, "firstaid", default={})


def save_firstaid(patient_id: str, firstaid_data: Dict[str, Any], create_backup: bool = True) -> bool:
    """
    Save first aid history/guidance for a patient.
    
    Args:
        patient_id: Patient identifier
        firstaid_data: First aid information to save
        create_backup: Whether to create a backup
    
    Returns:
        bool: True if save was successful
    """
    return _save_json(patient_id, "firstaid", firstaid_data, create_backup)


# ============================================================================
# MEDICAL REPORT DATA
# ============================================================================

def load_report(patient_id: str) -> Dict[str, Any]:
    """
    Load medical report for a patient.
    
    Args:
        patient_id: Patient identifier
    
    Returns:
        Dict containing medical report (empty dict if not found)
    
    Example:
        >>> report = load_report("p1")
        >>> print(report)
        {"diagnosis": "...", "medications": [...], ...}
    """
    return _load_json(patient_id, "report", default={})


def save_report(patient_id: str, report_data: Dict[str, Any], create_backup: bool = True) -> bool:
    """
    Save medical report for a patient.
    
    Args:
        patient_id: Patient identifier
        report_data: Medical report to save
        create_backup: Whether to create a backup
    
    Returns:
        bool: True if save was successful
    """
    return _save_json(patient_id, "report", report_data, create_backup)


# ============================================================================
# DIGITAL TWIN STATE DATA
# ============================================================================

def load_twin_state(patient_id: str) -> Dict[str, Any]:
    """
    Load digital twin state for a patient.
    
    Args:
        patient_id: Patient identifier
    
    Returns:
        Dict containing twin state (empty dict if not found)
    
    Example:
        >>> state = load_twin_state("p1")
        >>> print(state)
        {"overall_health_status": "stable", "health_score": 85, ...}
    """
    return _load_json(patient_id, "twinState", default={})


def save_twin_state(patient_id: str, state_data: Dict[str, Any], create_backup: bool = True) -> bool:
    """
    Save digital twin state for a patient.
    
    Args:
        patient_id: Patient identifier
        state_data: Twin state to save
        create_backup: Whether to create a backup
    
    Returns:
        bool: True if save was successful
    """
    return _save_json(patient_id, "twinState", state_data, create_backup)


# ============================================================================
# DIGITAL TWIN FORECAST DATA
# ============================================================================

def load_twin_forecast(patient_id: str) -> Dict[str, Any]:
    """
    Load digital twin forecast for a patient.
    
    Args:
        patient_id: Patient identifier
    
    Returns:
        Dict containing forecast data (empty dict if not found)
    
    Example:
        >>> forecast = load_twin_forecast("p1")
        >>> print(forecast)
        {"one_week_forecast": {...}, "one_month_forecast": {...}, ...}
    """
    return _load_json(patient_id, "twinforecast", default={})


def save_twin_forecast(patient_id: str, forecast_data: Dict[str, Any], create_backup: bool = True) -> bool:
    """
    Save digital twin forecast for a patient.
    
    Args:
        patient_id: Patient identifier
        forecast_data: Forecast data to save
        create_backup: Whether to create a backup
    
    Returns:
        bool: True if save was successful
    """
    return _save_json(patient_id, "twinforecast", forecast_data, create_backup)


# ============================================================================
# DIGITAL TWIN FORECAST CONTRAINDICATIONS DATA
# ============================================================================

def load_twin_forecast_contra(patient_id: str) -> Dict[str, Any]:
    """
    Load digital twin forecast contraindications for a patient.
    
    Args:
        patient_id: Patient identifier
    
    Returns:
        Dict containing contraindication data (empty dict if not found)
    
    Example:
        >>> contra = load_twin_forecast_contra("p1")
        >>> print(contra)
        {"risk_factors": [...], "warnings": [...], ...}
    """
    return _load_json(patient_id, "twinforecastcontra", default={})


def save_twin_forecast_contra(patient_id: str, contra_data: Dict[str, Any], create_backup: bool = True) -> bool:
    """
    Save digital twin forecast contraindications for a patient.
    
    Args:
        patient_id: Patient identifier
        contra_data: Contraindication data to save
        create_backup: Whether to create a backup
    
    Returns:
        bool: True if save was successful
    """
    return _save_json(patient_id, "twinforecastcontra", contra_data, create_backup)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_all_patient_data(patient_id: str) -> Dict[str, Any]:
    """
    Load all data files for a patient.
    
    Args:
        patient_id: Patient identifier
    
    Returns:
        Dict containing all patient data
    
    Example:
        >>> all_data = get_all_patient_data("p1")
        >>> print(all_data.keys())
        dict_keys(['conversation', 'daily_logs', 'diet', 'exercise', 'firstaid', 
                   'report', 'twin_state', 'twin_forecast', 'twin_forecast_contra'])
    """
    return {
        'conversation': load_conversation(patient_id),
        'daily_logs': load_daily_logs(patient_id),
        'diet': load_diet(patient_id),
        'exercise': load_exercise(patient_id),
        'firstaid': load_firstaid(patient_id),
        'report': load_report(patient_id),
        'twin_state': load_twin_state(patient_id),
        'twin_forecast': load_twin_forecast(patient_id),
        'twin_forecast_contra': load_twin_forecast_contra(patient_id),
    }


def patient_data_exists(patient_id: str) -> Dict[str, bool]:
    """
    Check which data files exist for a patient.
    
    Args:
        patient_id: Patient identifier
    
    Returns:
        Dict mapping data types to existence status
    
    Example:
        >>> exists = patient_data_exists("p1")
        >>> print(exists)
        {'conversation': True, 'daily_logs': True, 'diet': False, ...}
    """
    data_types = [
        'conversation', 'daily_logs', 'diet', 'exercize', 'firstaid',
        'report', 'twinState', 'twinforecast', 'twinforecastcontra'
    ]
    
    return {
        dtype: _get_file_path(patient_id, dtype).exists()
        for dtype in data_types
    }


def list_all_patients() -> List[str]:
    """
    List all patient IDs that have data files.
    
    Returns:
        List of unique patient IDs
    
    Example:
        >>> patients = list_all_patients()
        >>> print(patients)
        ['p1', 'p2', 'p3']
    """
    patient_ids = set()
    
    for file in PATIENT_DATA_DIR.glob("*.json"):
        # Extract patient ID from filename (e.g., "p1_conversation.json" -> "p1")
        parts = file.stem.split('_', 1)
        if len(parts) == 2:
            patient_ids.add(parts[0])
    
    return sorted(list(patient_ids))


def delete_patient_data(patient_id: str, data_type: Optional[str] = None, create_backup: bool = True) -> bool:
    """
    Delete patient data file(s).
    
    Args:
        patient_id: Patient identifier
        data_type: Specific data type to delete (None = delete all)
        create_backup: Whether to create backup before deletion
    
    Returns:
        bool: True if deletion was successful
    
    Example:
        >>> # Delete specific file
        >>> delete_patient_data("p1", "conversation")
        True
        
        >>> # Delete all files for patient
        >>> delete_patient_data("p1")
        True
    """
    try:
        if data_type:
            # Delete specific file
            file_path = _get_file_path(patient_id, data_type)
            if file_path.exists():
                if create_backup:
                    backup_path = file_path.with_suffix(f'.deleted_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
                    import shutil
                    shutil.move(file_path, backup_path)
                else:
                    file_path.unlink()
                return True
            return False
        else:
            # Delete all files for patient
            data_types = [
                'conversation', 'daily_logs', 'diet', 'exercize', 'firstaid',
                'report', 'twinState', 'twinforecast', 'twinforecastcontra'
            ]
            
            success = True
            for dtype in data_types:
                file_path = _get_file_path(patient_id, dtype)
                if file_path.exists():
                    try:
                        if create_backup:
                            backup_path = file_path.with_suffix(f'.deleted_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
                            import shutil
                            shutil.move(file_path, backup_path)
                        else:
                            file_path.unlink()
                    except Exception as e:
                        print(f"❌ Error deleting {file_path}: {e}")
                        success = False
            
            return success
            
    except Exception as e:
        print(f"❌ Error in delete_patient_data: {e}")
        return False


# ============================================================================
# CONVENIENCE ALIASES
# ============================================================================

# Shorter function names
get_conversation = load_conversation
set_conversation = save_conversation
get_daily_logs = load_daily_logs
set_daily_logs = save_daily_logs
get_diet = load_diet
set_diet = save_diet
get_exercise = load_exercise
set_exercise = save_exercise
get_firstaid = load_firstaid
set_firstaid = save_firstaid
get_report = load_report
set_report = save_report
get_twin_state = load_twin_state
set_twin_state = save_twin_state
get_twin_forecast = load_twin_forecast
set_twin_forecast = save_twin_forecast
get_twin_forecast_contra = load_twin_forecast_contra
set_twin_forecast_contra = save_twin_forecast_contra


if __name__ == "__main__":
    # Test the module
    print("="*80)
    print("PATIENT DATA MANAGER - TEST")
    print("="*80)
    
    # List all patients
    patients = list_all_patients()
    print(f"\n📋 Found {len(patients)} patients: {patients}")
    
    # Test loading data for first patient
    if patients:
        patient_id = patients[0]
        print(f"\n🔍 Testing data for patient: {patient_id}")
        
        exists = patient_data_exists(patient_id)
        print(f"\n📂 Data files existence:")
        for data_type, exists_flag in exists.items():
            status = "✅" if exists_flag else "❌"
            print(f"  {status} {data_type}")
        
        # Try loading a file
        daily_logs = load_daily_logs(patient_id)
        print(f"\n📊 Daily logs entries: {len(daily_logs)}")
        if daily_logs:
            print(f"  First entry day: {daily_logs[0].get('day', 'N/A')}")
