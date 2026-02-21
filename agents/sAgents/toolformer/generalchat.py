from medgemma.medgemmaClient import MedGemmaClient


def general_chat(question, conversation_id = None, validated_data=None):
    """
    Synthesizes the final response using validated medical evidence.
    """
    system_prompt = """
    You are an AI Medical Assistant based on MedGemma. 
    You provide clear, evidence-based health information. 
    - If validated data is provided, use it as your primary source of truth.
    - Always include a disclaimer that you are an AI and not a doctor.
    - Use a professional yet empathetic tone.
    """
    
    if validated_data:
        context_prompt = f"Context: {validated_data}\n\nUser Question: {question}"
    else:
        context_prompt = question

    client = MedGemmaClient(system_prompt=system_prompt)
    result = client.chat(user_text = context_prompt, conversation_id=conversation_id)
    return result