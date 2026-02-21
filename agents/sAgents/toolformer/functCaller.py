from medgemma.medgemmaClient import MedGemmaClient



def function_caller(question):
    """
    Identifies which medical tool to use and extracts the necessary parameters.
    """
    system_prompt = """
    You are a Medical Dispatcher Agent for a clinical system.
    Your task is to analyze the user's query and return a JSON object indicating the tool to call and its parameters.
    
    TOOLS:
    1. get_drug_interactions(drug_list: list): Use when the user asks about mixing medications.
    2. get_clinical_guidelines(condition: str): Use for queries about standard treatments or protocols.
    3. search_medical_records(patient_id: str, query: str): Use for patient-specific data retrieval.

    OUTPUT FORMAT:
    {"tool": "function_name", "parameters": {"param_name": "value"}}
    If no tool is needed, return {"tool": "none"}.
    
    Strictly output JSON. No conversational text.
    """

    prompt = f"Analyze this query: {question}"
    
    client = MedGemmaClient(system_prompt=system_prompt)
    result = client.respond(prompt)
    return result