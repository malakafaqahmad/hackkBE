"""
EHR Data Inserter Module
Provides functions to insert and update EHR data in JSON files.
"""

import json
import os
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime


class EHRInserter:
    """Class to insert and update EHR data in JSON files."""
    
    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize the EHR Inserter.
        
        Args:
            base_path: Base path to the ehr_store directory. 
                      If None, uses ehr_store directory.
        """
        if base_path is None:
            # Default to ehr_store directory
            self.base_path = Path(__file__).parent.parent / 'ehr_store'
        else:
            self.base_path = Path(base_path)
    
    def _load_json_file(self, filename: str) -> List[Dict[str, Any]]:
        """
        Load data from a JSON file.
        
        Args:
            filename: Name of the JSON file to load
            
        Returns:
            List of dictionaries containing the loaded data
        """
        file_path = self.base_path / filename
        
        if not file_path.exists():
            return []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    
    def _save_json_file(self, filename: str, data: List[Dict[str, Any]]) -> None:
        """
        Save data to a JSON file.
        
        Args:
            filename: Name of the JSON file to save
            data: List of dictionaries to save
        """
        file_path = self.base_path / filename
        
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _add_timestamps(self, data: Dict[str, Any], update: bool = False) -> Dict[str, Any]:
        """
        Add or update timestamps in the data.
        
        Args:
            data: The data dictionary to add timestamps to
            update: If True, updates updated_at. If False, sets both created_at and updated_at
            
        Returns:
            Data dictionary with timestamps
        """
        current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        
        if not update and 'created_at' not in data:
            data['created_at'] = current_time
        
        data['updated_at'] = current_time
        
        return data
    
    def insert_patient(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insert a new patient record.
        
        Args:
            patient_data: Dictionary containing patient information
            
        Returns:
            The inserted patient record with timestamps
            
        Raises:
            ValueError: If patient ID already exists
        """
        patients = self._load_json_file('patients.json')
        
        # Check if patient ID already exists
        if any(p['id'] == patient_data.get('id') for p in patients):
            raise ValueError(f"Patient with ID {patient_data.get('id')} already exists")
        
        # Add timestamps
        patient_data = self._add_timestamps(patient_data)
        
        # Add to list and save
        patients.append(patient_data)
        self._save_json_file('patients.json', patients)
        
        return patient_data
    
    def update_patient(self, patient_id: str, patient_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing patient record.
        
        Args:
            patient_id: ID of the patient to update
            patient_data: Dictionary containing updated patient information
            
        Returns:
            The updated patient record or None if not found
        """
        patients = self._load_json_file('patients.json')
        
        for i, patient in enumerate(patients):
            if patient['id'] == patient_id:
                # Preserve ID and created_at
                patient_data['id'] = patient_id
                if 'created_at' in patient:
                    patient_data['created_at'] = patient['created_at']
                
                # Update timestamps
                patient_data = self._add_timestamps(patient_data, update=True)
                
                patients[i] = patient_data
                self._save_json_file('patients.json', patients)
                
                return patient_data
        
        return None
    
    def insert_doctor(self, doctor_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insert a new doctor record.
        
        Args:
            doctor_data: Dictionary containing doctor information
            
        Returns:
            The inserted doctor record with timestamps
            
        Raises:
            ValueError: If doctor ID already exists
        """
        doctors = self._load_json_file('doctors.json')
        
        if any(d['id'] == doctor_data.get('id') for d in doctors):
            raise ValueError(f"Doctor with ID {doctor_data.get('id')} already exists")
        
        doctor_data = self._add_timestamps(doctor_data)
        doctors.append(doctor_data)
        self._save_json_file('doctors.json', doctors)
        
        return doctor_data
    
    def insert_allergy(self, allergy_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insert a new allergy record.
        
        Args:
            allergy_data: Dictionary containing allergy information
            
        Returns:
            The inserted allergy record with timestamps
            
        Raises:
            ValueError: If allergy ID already exists
        """
        allergies = self._load_json_file('allergies.json')
        
        if any(a['id'] == allergy_data.get('id') for a in allergies):
            raise ValueError(f"Allergy with ID {allergy_data.get('id')} already exists")
        
        allergy_data = self._add_timestamps(allergy_data)
        allergies.append(allergy_data)
        self._save_json_file('allergies.json', allergies)
        
        return allergy_data
    
    def insert_medication(self, medication_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insert a new medication record.
        
        Args:
            medication_data: Dictionary containing medication information
            
        Returns:
            The inserted medication record with timestamps
            
        Raises:
            ValueError: If medication ID already exists
        """
        medications = self._load_json_file('medications.json')
        
        if any(m['id'] == medication_data.get('id') for m in medications):
            raise ValueError(f"Medication with ID {medication_data.get('id')} already exists")
        
        medication_data = self._add_timestamps(medication_data)
        medications.append(medication_data)
        self._save_json_file('medications.json', medications)
        
        return medication_data
    
    def update_medication(self, medication_id: str, medication_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing medication record.
        
        Args:
            medication_id: ID of the medication to update
            medication_data: Dictionary containing updated medication information
            
        Returns:
            The updated medication record or None if not found
        """
        medications = self._load_json_file('medications.json')
        
        for i, medication in enumerate(medications):
            if medication['id'] == medication_id:
                medication_data['id'] = medication_id
                if 'created_at' in medication:
                    medication_data['created_at'] = medication['created_at']
                
                medication_data = self._add_timestamps(medication_data, update=True)
                medications[i] = medication_data
                self._save_json_file('medications.json', medications)
                
                return medication_data
        
        return None
    
    def insert_appointment(self, appointment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insert a new appointment record.
        
        Args:
            appointment_data: Dictionary containing appointment information
            
        Returns:
            The inserted appointment record with timestamps
            
        Raises:
            ValueError: If appointment ID already exists
        """
        appointments = self._load_json_file('appointments.json')
        
        if any(a['id'] == appointment_data.get('id') for a in appointments):
            raise ValueError(f"Appointment with ID {appointment_data.get('id')} already exists")
        
        appointment_data = self._add_timestamps(appointment_data)
        appointments.append(appointment_data)
        self._save_json_file('appointments.json', appointments)
        
        return appointment_data
    
    def update_appointment(self, appointment_id: str, appointment_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing appointment record.
        
        Args:
            appointment_id: ID of the appointment to update
            appointment_data: Dictionary containing updated appointment information
            
        Returns:
            The updated appointment record or None if not found
        """
        appointments = self._load_json_file('appointments.json')
        
        for i, appointment in enumerate(appointments):
            if appointment['id'] == appointment_id:
                appointment_data['id'] = appointment_id
                if 'created_at' in appointment:
                    appointment_data['created_at'] = appointment['created_at']
                
                appointment_data = self._add_timestamps(appointment_data, update=True)
                appointments[i] = appointment_data
                self._save_json_file('appointments.json', appointments)
                
                return appointment_data
        
        return None
    
    def insert_encounter(self, encounter_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insert a new encounter record.
        
        Args:
            encounter_data: Dictionary containing encounter information
            
        Returns:
            The inserted encounter record with timestamps
            
        Raises:
            ValueError: If encounter ID already exists
        """
        encounters = self._load_json_file('encounters.json')
        
        if any(e['id'] == encounter_data.get('id') for e in encounters):
            raise ValueError(f"Encounter with ID {encounter_data.get('id')} already exists")
        
        encounter_data = self._add_timestamps(encounter_data)
        encounters.append(encounter_data)
        self._save_json_file('encounters.json', encounters)
        
        return encounter_data
    
    def insert_lab_result(self, lab_result_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insert a new lab result record.
        
        Args:
            lab_result_data: Dictionary containing lab result information
            
        Returns:
            The inserted lab result record with timestamps
            
        Raises:
            ValueError: If lab result ID already exists
        """
        lab_results = self._load_json_file('lab_results.json')
        
        if any(l['id'] == lab_result_data.get('id') for l in lab_results):
            raise ValueError(f"Lab result with ID {lab_result_data.get('id')} already exists")
        
        lab_result_data = self._add_timestamps(lab_result_data)
        lab_results.append(lab_result_data)
        self._save_json_file('lab_results.json', lab_results)
        
        return lab_result_data
    
    def insert_medical_history(self, history_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insert a new medical history record.
        
        Args:
            history_data: Dictionary containing medical history information
            
        Returns:
            The inserted medical history record with timestamps
            
        Raises:
            ValueError: If medical history ID already exists
        """
        history = self._load_json_file('medical_history.json')
        
        if any(h['id'] == history_data.get('id') for h in history):
            raise ValueError(f"Medical history with ID {history_data.get('id')} already exists")
        
        history_data = self._add_timestamps(history_data)
        history.append(history_data)
        self._save_json_file('medical_history.json', history)
        
        return history_data
    
    def update_medical_history(self, history_id: str, history_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing medical history record.
        
        Args:
            history_id: ID of the medical history to update
            history_data: Dictionary containing updated medical history information
            
        Returns:
            The updated medical history record or None if not found
        """
        history = self._load_json_file('medical_history.json')
        
        for i, record in enumerate(history):
            if record['id'] == history_id:
                history_data['id'] = history_id
                if 'created_at' in record:
                    history_data['created_at'] = record['created_at']
                
                history_data = self._add_timestamps(history_data, update=True)
                history[i] = history_data
                self._save_json_file('medical_history.json', history)
                
                return history_data
        
        return None
    
    def insert_imaging(self, imaging_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insert a new imaging record.
        
        Args:
            imaging_data: Dictionary containing imaging information
            
        Returns:
            The inserted imaging record with timestamps
            
        Raises:
            ValueError: If imaging ID already exists
        """
        imaging = self._load_json_file('imaging.json')
        
        if any(i.get('id') == imaging_data.get('id') for i in imaging if i.get('id') is not None):
            raise ValueError(f"Imaging with ID {imaging_data.get('id')} already exists")
        
        imaging_data = self._add_timestamps(imaging_data)
        imaging.append(imaging_data)
        self._save_json_file('imaging.json', imaging)
        
        return imaging_data
    
    def insert_observation(self, observation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insert a new observation record.
        
        Args:
            observation_data: Dictionary containing observation information
            
        Returns:
            The inserted observation record
        """
        observations = self._load_json_file('observations.json')
        
        # Check if patient already has observations
        patient_id = observation_data.get('patient_id')
        patient_obs = next((o for o in observations if o['patient_id'] == patient_id), None)
        
        if patient_obs:
            # Add to existing patient's observations
            if 'observations' not in patient_obs:
                patient_obs['observations'] = []
            patient_obs['observations'].extend(observation_data.get('observations', []))
        else:
            # Create new patient observation record
            observations.append(observation_data)
        
        self._save_json_file('observations.json', observations)
        
        return observation_data
    
    def delete_record(self, filename: str, record_id: str) -> bool:
        """
        Delete a record from a JSON file.
        
        Args:
            filename: Name of the JSON file
            record_id: ID of the record to delete
            
        Returns:
            True if record was deleted, False otherwise
        """
        records = self._load_json_file(filename)
        original_length = len(records)
        
        records = [r for r in records if r.get('id') != record_id]
        
        if len(records) < original_length:
            self._save_json_file(filename, records)
            return True
        
        return False


# Convenience functions for quick access
def insert_patient(patient_data: Dict[str, Any], base_path: Optional[str] = None) -> Dict[str, Any]:
    """Insert a new patient record."""
    return EHRInserter(base_path).insert_patient(patient_data)


def insert_medication(medication_data: Dict[str, Any], base_path: Optional[str] = None) -> Dict[str, Any]:
    """Insert a new medication record."""
    return EHRInserter(base_path).insert_medication(medication_data)


def insert_appointment(appointment_data: Dict[str, Any], base_path: Optional[str] = None) -> Dict[str, Any]:
    """Insert a new appointment record."""
    return EHRInserter(base_path).insert_appointment(appointment_data)


def update_patient(patient_id: str, patient_data: Dict[str, Any], 
                   base_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Update an existing patient record."""
    return EHRInserter(base_path).update_patient(patient_id, patient_data)
