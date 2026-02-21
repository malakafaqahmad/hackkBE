"""
Test script for Patient Data Manager

Tests all loader and saver functions.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ehr_store.patientdata.data_manager import (
    # Load functions
    load_conversation, load_daily_logs, load_diet, load_exercise,
    load_firstaid, load_report, load_twin_state, load_twin_forecast,
    load_twin_forecast_contra,
    
    # Save functions
    save_conversation, save_daily_logs, save_diet, save_exercise,
    save_firstaid, save_report, save_twin_state, save_twin_forecast,
    save_twin_forecast_contra,
    
    # Utility functions
    get_all_patient_data, patient_data_exists, list_all_patients,
    append_daily_log
)


def test_list_patients():
    """Test listing all patients."""
    print("\n" + "="*80)
    print("TEST 1: List All Patients")
    print("="*80)
    
    patients = list_all_patients()
    print(f"\n✅ Found {len(patients)} patients: {patients}")
    return patients


def test_check_existence(patient_id):
    """Test checking which files exist for a patient."""
    print("\n" + "="*80)
    print(f"TEST 2: Check File Existence for {patient_id}")
    print("="*80)
    
    exists = patient_data_exists(patient_id)
    print(f"\n📂 File existence status:")
    for data_type, exists_flag in exists.items():
        status = "✅ EXISTS" if exists_flag else "❌ MISSING"
        print(f"  {status:12} {data_type}")


def test_load_functions(patient_id):
    """Test all load functions."""
    print("\n" + "="*80)
    print(f"TEST 3: Load Functions for {patient_id}")
    print("="*80)
    
    # Test conversation
    print("\n📞 Loading conversation...")
    conversation = load_conversation(patient_id)
    print(f"  Type: {type(conversation)}, Length: {len(conversation)}")
    
    # Test daily logs
    print("\n📊 Loading daily logs...")
    daily_logs = load_daily_logs(patient_id)
    print(f"  Type: {type(daily_logs)}, Length: {len(daily_logs)}")
    if daily_logs:
        print(f"  First entry day: {daily_logs[0].get('day', 'N/A')}")
        print(f"  Keys: {list(daily_logs[0].keys())}")
    
    # Test diet
    print("\n🍎 Loading diet...")
    diet = load_diet(patient_id)
    print(f"  Type: {type(diet)}, Keys: {list(diet.keys()) if diet else 'empty'}")
    
    # Test exercise
    print("\n🏃 Loading exercise...")
    exercise = load_exercise(patient_id)
    print(f"  Type: {type(exercise)}, Keys: {list(exercise.keys()) if exercise else 'empty'}")
    
    # Test firstaid
    print("\n🚑 Loading firstaid...")
    firstaid = load_firstaid(patient_id)
    print(f"  Type: {type(firstaid)}, Keys: {list(firstaid.keys()) if firstaid else 'empty'}")
    
    # Test report
    print("\n📋 Loading report...")
    report = load_report(patient_id)
    print(f"  Type: {type(report)}, Keys: {list(report.keys()) if report else 'empty'}")
    
    # Test twin state
    print("\n🤖 Loading twin state...")
    twin_state = load_twin_state(patient_id)
    print(f"  Type: {type(twin_state)}, Keys: {list(twin_state.keys()) if twin_state else 'empty'}")
    
    # Test twin forecast
    print("\n🔮 Loading twin forecast...")
    twin_forecast = load_twin_forecast(patient_id)
    print(f"  Type: {type(twin_forecast)}, Keys: {list(twin_forecast.keys()) if twin_forecast else 'empty'}")
    
    # Test twin forecast contra
    print("\n⚠️  Loading twin forecast contraindications...")
    twin_forecast_contra = load_twin_forecast_contra(patient_id)
    print(f"  Type: {type(twin_forecast_contra)}, Keys: {list(twin_forecast_contra.keys()) if twin_forecast_contra else 'empty'}")


def test_save_functions(patient_id):
    """Test save functions with sample data."""
    print("\n" + "="*80)
    print(f"TEST 4: Save Functions for {patient_id}")
    print("="*80)
    
    test_patient = f"{patient_id}_test"
    
    # Test save conversation
    print("\n💾 Testing save_conversation...")
    test_conversation = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
    ]
    result = save_conversation(test_patient, test_conversation, create_backup=False)
    print(f"  Result: {'✅ SUCCESS' if result else '❌ FAILED'}")
    
    # Verify by loading
    loaded = load_conversation(test_patient)
    print(f"  Verification: {'✅ MATCH' if loaded == test_conversation else '❌ MISMATCH'}")
    
    # Test save diet
    print("\n💾 Testing save_diet...")
    test_diet = {
        "meal_plan": ["breakfast", "lunch", "dinner"],
        "restrictions": ["no sugar", "low sodium"]
    }
    result = save_diet(test_patient, test_diet, create_backup=False)
    print(f"  Result: {'✅ SUCCESS' if result else '❌ FAILED'}")
    
    # Test save report
    print("\n💾 Testing save_report...")
    test_report = {
        "diagnosis": "Test diagnosis",
        "medications": ["med1", "med2"],
        "last_updated": "2026-02-22"
    }
    result = save_report(test_patient, test_report, create_backup=False)
    print(f"  Result: {'✅ SUCCESS' if result else '❌ FAILED'}")
    
    print("\n⚠️  Note: Test files created with patient ID: " + test_patient)


def test_append_daily_log(patient_id):
    """Test appending to daily logs."""
    print("\n" + "="*80)
    print(f"TEST 5: Append Daily Log for {patient_id}")
    print("="*80)
    
    test_patient = f"{patient_id}_test"
    
    # Get current logs
    current_logs = load_daily_logs(test_patient)
    initial_count = len(current_logs)
    print(f"\n📊 Current log entries: {initial_count}")
    
    # Append new log
    new_log = {
        "day": initial_count + 1,
        "vitals": {"BP": "120/80", "HR": 72},
        "medications_taken": ["test_med"],
        "notes": "Test log entry"
    }
    
    print(f"\n➕ Appending new log entry (day {new_log['day']})...")
    result = append_daily_log(test_patient, new_log)
    print(f"  Result: {'✅ SUCCESS' if result else '❌ FAILED'}")
    
    # Verify
    updated_logs = load_daily_logs(test_patient)
    new_count = len(updated_logs)
    print(f"  New log entries: {new_count}")
    print(f"  Verification: {'✅ SUCCESS' if new_count == initial_count + 1 else '❌ FAILED'}")


def test_get_all_data(patient_id):
    """Test getting all patient data at once."""
    print("\n" + "="*80)
    print(f"TEST 6: Get All Patient Data for {patient_id}")
    print("="*80)
    
    all_data = get_all_patient_data(patient_id)
    
    print(f"\n📦 Retrieved data for {len(all_data)} categories:")
    for category, data in all_data.items():
        data_type = type(data).__name__
        if isinstance(data, (list, dict)):
            size = len(data)
            print(f"  • {category:20} : {data_type} (size: {size})")
        else:
            print(f"  • {category:20} : {data_type}")


def main():
    """Run all tests."""
    print("="*80)
    print("PATIENT DATA MANAGER - COMPREHENSIVE TEST SUITE")
    print("="*80)
    
    # Test 1: List patients
    patients = test_list_patients()
    
    if not patients:
        print("\n⚠️  No patients found. Cannot proceed with tests.")
        return
    
    # Use first patient for testing
    patient_id = patients[0]
    print(f"\n🔬 Running tests with patient: {patient_id}")
    
    # Test 2: Check file existence
    test_check_existence(patient_id)
    
    # Test 3: Load functions
    test_load_functions(patient_id)
    
    # Test 4: Save functions
    test_save_functions(patient_id)
    
    # Test 5: Append daily log
    test_append_daily_log(patient_id)
    
    # Test 6: Get all data
    test_get_all_data(patient_id)
    
    print("\n" + "="*80)
    print("✅ ALL TESTS COMPLETED")
    print("="*80)
    print("\nℹ️  Test files were created with '_test' suffix")
    print("   You can safely delete them if needed.")


if __name__ == "__main__":
    main()
