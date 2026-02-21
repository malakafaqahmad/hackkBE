from medgemma.medgemmaClient import MedGemmaClient

def funct_validator(prompt, function_name):
    """
    Validates the clinical relevance and safety of the tool's result.
    """
    system_prompt = """
    You are a Clinical Validation Agent. Your goal is to verify if the output from a medical tool 
    accurately answers the user's original intent without medical contradictions.
    
    RESPONSE FORMAT:
    {
        "is_valid": true/false,
        "reason": "Brief explanation if invalid",
        "clean_data": "Refined data for the chat agent"
    }
    """

    validation_request = f"""
    User Question: {prompt}
    Tool Used: {function_name}
    
    Evaluate if this data is clinically relevant and safe to present.
    """

    client = MedGemmaClient(system_prompt=system_prompt)
    result = client.respond(validation_request)
    return result


