from medgemma.medgemmaClient import MedGemmaClient


def imagesHandler(patientid, images, report):
    """
    Images Handler Agent - Processes and analyzes patient-related images (e.g., scans, photos).
    
    Args:
        patientid: Patient identifier
        images: List of image data (base64 encoded or file paths)
        report: Current patient report for context
    
    Returns:
        dict: Analysis results including identified features, abnormalities, and clinical insights
    """

    
    system_prompt = """You are an Expert Medical Image Analysis AI specializing in processing patient-related images.
YOUR ROLE:
- Analyze medical images (e.g., scans, xrays, mri) for clinical insights
- Identify key features and abnormalities
- Correlate image findings with patient context
- Provide structured analysis results
OUTPUT FORMAT (Valid JSON only):
{
    "image_analysis": [
        {
            "image_id": "string",
            "identified_features": ["feature1", "feature2"],
            "abnormalities": ["abnormality1", "abnormality2"],
            "clinical_insights": ["insight1", "insight2"],
            "confidence_scores": {
                "feature1": float (0-100),
                "abnormality1": float (0-100)
            }
        }
    ]

}
"""

    user_prompt = f"""Patient ID: {patientid}
Images: {images} 
Current Report: {report}
    analyze the provided images in the context of the patient and return a structured analysis as specified in the system prompt.
    """

    client = MedGemmaClient(system_prompt)
    response = client.respond(user_prompt)

    return response