"""
Shared cache for agent data to avoid repeated API calls.
"""

# Cache for EHR summaries to avoid repeated API calls
ehr_summary_cache = {}

def get_ehr_summary(patient_id: str, generator_func):
    """
    Get EHR summary from cache or generate it.
    
    Args:
        patient_id: The patient ID
        generator_func: Function to call if not in cache (takes patient_id as argument)
    
    Returns:
        The EHR summary
    """
    if patient_id not in ehr_summary_cache:
        print("cache miss for the patient report, generating new summary...")
        ehr_summary_cache[patient_id] = generator_func(patient_id)
        print("EHR summary cached.")
        # print(ehr_summary_cache[patient_id])
    else:
        print("cache hit for the patient ehr summary.")
    return ehr_summary_cache[patient_id]

def clear_ehr_cache(patient_id: str = None):
    """
    Clear the EHR cache.
    
    Args:
        patient_id: If provided, clear only this patient's cache. 
                   If None, clear entire cache.
    """
    if patient_id:
        ehr_summary_cache.pop(patient_id, None)
    else:
        ehr_summary_cache.clear()
