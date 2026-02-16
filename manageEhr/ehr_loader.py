"""
EHR Data Loader Module
Provides functions to load various EHR data from JSON files.
"""

import json
import os
from typing import List, Dict, Any, Optional
from pathlib import Path


class EHRLoader:
    """Class to load EHR data from JSON files."""
    
    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize the EHR Loader.
        
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
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
        """
        file_path = self.base_path / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_patients(self) -> List[Dict[str, Any]]:
        """Load all patient records."""
        return self._load_json_file('patients.json')
    
    def load_patient_by_id(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """
        Load a specific patient by ID.
        
        Args:
            patient_id: The patient ID to search for
            
        Returns:
            Patient dictionary if found, None otherwise
        """
        patients = self.load_patients()
        return next((p for p in patients if p['id'] == patient_id), None)
    
    def load_doctors(self) -> List[Dict[str, Any]]:
        """Load all doctor records."""
        return self._load_json_file('doctors.json')
    
    def load_doctor_by_id(self, doctor_id: str) -> Optional[Dict[str, Any]]:
        """
        Load a specific doctor by ID.
        
        Args:
            doctor_id: The doctor ID to search for
            
        Returns:
            Doctor dictionary if found, None otherwise
        """
        doctors = self.load_doctors()
        return next((d for d in doctors if d['id'] == doctor_id), None)
    
    def load_allergies(self, patient_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Load allergy records.
        
        Args:
            patient_id: Optional patient ID to filter allergies
            
        Returns:
            List of allergy records
        """
        allergies = self._load_json_file('allergies.json')
        
        if patient_id:
            return [a for a in allergies if a['patient_id'] == patient_id]
        
        return allergies
    
    def load_medications(self, patient_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Load medication records.
        
        Args:
            patient_id: Optional patient ID to filter medications
            
        Returns:
            List of medication records
        """
        medications = self._load_json_file('medications.json')
        
        if patient_id:
            return [m for m in medications if m['patient_id'] == patient_id]
        
        return medications
    
    def load_appointments(self, patient_id: Optional[str] = None, 
                         doctor_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Load appointment records.
        
        Args:
            patient_id: Optional patient ID to filter appointments
            doctor_id: Optional doctor ID to filter appointments
            
        Returns:
            List of appointment records
        """
        appointments = self._load_json_file('appointments.json')
        
        if patient_id:
            appointments = [a for a in appointments if a['patient_id'] == patient_id]
        
        if doctor_id:
            appointments = [a for a in appointments if a['doctor_id'] == doctor_id]
        
        return appointments
    
    def load_encounters(self, patient_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Load encounter records.
        
        Args:
            patient_id: Optional patient ID to filter encounters
            
        Returns:
            List of encounter records
        """
        encounters = self._load_json_file('encounters.json')
        
        if patient_id:
            return [e for e in encounters if e['patient_id'] == patient_id]
        
        return encounters
    
    def load_lab_results(self, patient_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Load lab result records.
        
        Args:
            patient_id: Optional patient ID to filter lab results
            
        Returns:
            List of lab result records
        """
        lab_results = self._load_json_file('lab_results.json')
        
        if patient_id:
            return [l for l in lab_results if l['patient_id'] == patient_id]
        
        return lab_results
    
    def load_medical_history(self, patient_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Load medical history records.
        
        Args:
            patient_id: Optional patient ID to filter medical history
            
        Returns:
            List of medical history records
        """
        history = self._load_json_file('medical_history.json')
        
        if patient_id:
            return [h for h in history if h['patient_id'] == patient_id]
        
        return history
    
    def load_imaging(self, patient_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Load imaging records.
        
        Args:
            patient_id: Optional patient ID to filter imaging records
            
        Returns:
            List of imaging records
        """
        imaging = self._load_json_file('imaging.json')
        
        if patient_id:
            return [i for i in imaging if i['patient_id'] == patient_id]
        
        return imaging
    
    def load_observations(self, patient_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Load observation records.
        
        Args:
            patient_id: Optional patient ID to filter observations
            
        Returns:
            List of observation records
        """
        observations = self._load_json_file('observations.json')
        
        if patient_id:
            return [o for o in observations if o['patient_id'] == patient_id]
        
        return observations
    
    def load_patient_complete_record(self, patient_id: str) -> Dict[str, Any]:
        """
        Load complete medical record for a patient.
        
        Args:
            patient_id: The patient ID to load complete record for
            
        Returns:
            Dictionary containing all patient data
        """
        return {
            'patient': self.load_patient_by_id(patient_id),
            'allergies': self.load_allergies(patient_id),
            'medications': self.load_medications(patient_id),
            'appointments': self.load_appointments(patient_id=patient_id),
            'encounters': self.load_encounters(patient_id),
            'lab_results': self.load_lab_results(patient_id),
            'medical_history': self.load_medical_history(patient_id),
            'imaging': self.load_imaging(patient_id),
            'observations': self.load_observations(patient_id)
        }


# Convenience functions for quick access
def load_patients(base_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Load all patient records."""
    return EHRLoader(base_path).load_patients()


def load_patient_by_id(patient_id: str, base_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Load a specific patient by ID."""
    return EHRLoader(base_path).load_patient_by_id(patient_id)


def load_doctors(base_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Load all doctor records."""
    return EHRLoader(base_path).load_doctors()


def load_patient_complete_record(patient_id: str, base_path: Optional[str] = None) -> Dict[str, Any]:
    """Load complete medical record for a patient."""
    return EHRLoader(base_path).load_patient_complete_record(patient_id)
