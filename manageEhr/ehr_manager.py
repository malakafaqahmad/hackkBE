"""
EHR Manager Module
Main interface for loading and managing EHR data.
"""

from typing import Dict, Any, List, Optional
from .ehr_loader import EHRLoader
from .ehr_inserter import EHRInserter


class EHRManager:
    """
    Unified interface for EHR data management.
    Combines loading and inserting capabilities.
    """
    
    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize the EHR Manager.
        
        Args:
            base_path: Base path to the ehr_store directory. 
                      If None, uses current directory.
        """
        self.loader = EHRLoader(base_path)
        self.inserter = EHRInserter(base_path)
    
    # Patient operations
    def get_patients(self) -> List[Dict[str, Any]]:
        """Get all patients."""
        return self.loader.load_patients()
    
    def get_patient(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific patient by ID."""
        return self.loader.load_patient_by_id(patient_id)
    
    def get_patient_full_record(self, patient_id: str) -> Dict[str, Any]:
        """Get complete medical record for a patient."""
        return self.loader.load_patient_complete_record(patient_id)
    
    def get_all_patient_ehr_data(self, patient_id: str) -> Dict[str, Any]:
        """
        Get all EHR data for a specific patient.
        
        Args:
            patient_id: The ID of the patient
            
        Returns:
            Dictionary containing all patient EHR data including:
            - patient: Patient demographics and basic info
            - allergies: All allergy records
            - medications: All medication records
            - appointments: All appointment records
            - encounters: All encounter records
            - lab_results: All lab result records
            - medical_history: All medical history records
            - imaging: All imaging records
            - observations: All observation records
        """
        return {
            "patient": self.get_patient(patient_id),
            "allergies": self.get_allergies(patient_id),
            "medications": self.get_medications(patient_id),
            "appointments": self.get_appointments(patient_id=patient_id),
            "encounters": self.get_encounters(patient_id),
            "lab_results": self.get_lab_results(patient_id),
            "medical_history": self.get_medical_history(patient_id),
            "imaging": self.get_imaging(patient_id),
            "observations": self.get_observations(patient_id)
        }
    
    def add_patient(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new patient."""
        return self.inserter.insert_patient(patient_data)
    
    def update_patient(self, patient_id: str, patient_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing patient."""
        return self.inserter.update_patient(patient_id, patient_data)
    
    # Doctor operations
    def get_doctors(self) -> List[Dict[str, Any]]:
        """Get all doctors."""
        return self.loader.load_doctors()
    
    def get_doctor(self, doctor_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific doctor by ID."""
        return self.loader.load_doctor_by_id(doctor_id)
    
    def add_doctor(self, doctor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new doctor."""
        return self.inserter.insert_doctor(doctor_data)
    
    # Allergy operations
    def get_allergies(self, patient_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get allergy records, optionally filtered by patient."""
        return self.loader.load_allergies(patient_id)
    
    def add_allergy(self, allergy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new allergy record."""
        return self.inserter.insert_allergy(allergy_data)
    
    # Medication operations
    def get_medications(self, patient_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get medication records, optionally filtered by patient."""
        return self.loader.load_medications(patient_id)
    
    def add_medication(self, medication_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new medication record."""
        return self.inserter.insert_medication(medication_data)
    
    def update_medication(self, medication_id: str, 
                         medication_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing medication record."""
        return self.inserter.update_medication(medication_id, medication_data)
    
    # Appointment operations
    def get_appointments(self, patient_id: Optional[str] = None, 
                        doctor_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get appointment records, optionally filtered by patient or doctor."""
        return self.loader.load_appointments(patient_id, doctor_id)
    
    def add_appointment(self, appointment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new appointment record."""
        return self.inserter.insert_appointment(appointment_data)
    
    def update_appointment(self, appointment_id: str, 
                          appointment_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing appointment record."""
        return self.inserter.update_appointment(appointment_id, appointment_data)
    
    # Encounter operations
    def get_encounters(self, patient_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get encounter records, optionally filtered by patient."""
        return self.loader.load_encounters(patient_id)
    
    def add_encounter(self, encounter_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new encounter record."""
        return self.inserter.insert_encounter(encounter_data)
    
    # Lab result operations
    def get_lab_results(self, patient_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get lab result records, optionally filtered by patient."""
        return self.loader.load_lab_results(patient_id)
    
    def add_lab_result(self, lab_result_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new lab result record."""
        return self.inserter.insert_lab_result(lab_result_data)
    
    # Medical history operations
    def get_medical_history(self, patient_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get medical history records, optionally filtered by patient."""
        return self.loader.load_medical_history(patient_id)
    
    def add_medical_history(self, history_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new medical history record."""
        return self.inserter.insert_medical_history(history_data)
    
    def update_medical_history(self, history_id: str, 
                              history_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing medical history record."""
        return self.inserter.update_medical_history(history_id, history_data)
    
    # Imaging operations
    def get_imaging(self, patient_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get imaging records, optionally filtered by patient."""
        return self.loader.load_imaging(patient_id)
    
    def add_imaging(self, imaging_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new imaging record."""
        return self.inserter.insert_imaging(imaging_data)
    
    # Observation operations
    def get_observations(self, patient_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get observation records, optionally filtered by patient."""
        return self.loader.load_observations(patient_id)
    
    def add_observation(self, observation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new observation record."""
        return self.inserter.insert_observation(observation_data)
    
    # Delete operations
    def delete_record(self, record_type: str, record_id: str) -> bool:
        """
        Delete a record by type and ID.
        
        Args:
            record_type: Type of record (e.g., 'patient', 'medication', 'appointment')
            record_id: ID of the record to delete
            
        Returns:
            True if record was deleted, False otherwise
        """
        filename_map = {
            'patient': 'patients.json',
            'doctor': 'doctors.json',
            'allergy': 'allergies.json',
            'medication': 'medications.json',
            'appointment': 'appointments.json',
            'encounter': 'encounters.json',
            'lab_result': 'lab_results.json',
            'medical_history': 'medical_history.json',
            'imaging': 'imaging.json'
        }
        
        filename = filename_map.get(record_type)
        if not filename:
            raise ValueError(f"Unknown record type: {record_type}")
        
        return self.inserter.delete_record(filename, record_id)


# Create a default manager instance
_default_manager = None


def get_manager(base_path: Optional[str] = None) -> EHRManager:
    """
    Get or create the default EHR manager instance.
    
    Args:
        base_path: Optional base path. If None and no default manager exists,
                  creates one with default path.
    
    Returns:
        EHRManager instance
    """
    global _default_manager
    
    if _default_manager is None or base_path is not None:
        _default_manager = EHRManager(base_path)
    
    return _default_manager
