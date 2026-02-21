from medgemma.medgemmaClient import MedGemmaClient


def reportHandler(patientid, pdftext, report):


    
    system_prompt = """You are an Expert Medical Image Analysis AI specializing in processing patient-related test results.
YOUR ROLE:
- Analyze medical test results (e.g., lab reports, imaging findings) for clinical insights
- Identify key features and abnormalities
- Correlate findings with patient context
- Provide structured analysis results
OUTPUT FORMAT (Valid JSON only):
{
    "image_analysis": [
        {
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
report: {pdftext} 
Current Report: {report}
    analyze the provided report text in the context of the patient and return a structured analysis as specified in the system prompt.
    """

    client = MedGemmaClient(system_prompt)
    response = client.respond(user_prompt)

    return response