from medgemma.medgemmaClient import MedGemmaClient


def reporter(patientid, imageextractedfeatures, report):
    """
    Images Handler Agent - Processes and analyzes patient-related images (e.g., scans, photos).
    
    Args:
        patientid: Patient identifier
        images: List of image data (base64 encoded or file paths)
    
    Returns:
        dict: Analysis results including identified features, abnormalities, and clinical insights
    """

    
    system_prompt = """you are an expert medical report updater ai specializing in synthesizing medical image analysis results into comprehensive patient reports.
YOUR ROLE:
- Integrate medical image analysis findings into patient reports
- Correlate image features with clinical context
- Update patient health profiles with new image insights
- Provide structured report updates based on image analysis
- ensure you dont change any of the existing information in the patient report and only add the new insights from the image analysis in a structured format
"""

    user_prompt = f"""Patient ID: {patientid}
Images: {imageextractedfeatures} 
    analyze the image features and update the existing patient report with new insights.
    Existing Report: {report}
    """

    client = MedGemmaClient(system_prompt)
    response = client.respond(user_prompt)

    return response