from medgemma.medgemmaClient import MedGemmaClient
import base64
import io


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

    # Prepare image metadata for context (without base64 data)
    image_metadata = []
    for img in images:
        metadata = {
            'filename': img.get('filename', 'unknown'),
            'type': img.get('type', 'image'),
            'format': img.get('format', 'unknown')
        }
        if 'dimensions' in img:
            metadata['dimensions'] = img['dimensions']
        image_metadata.append(metadata)

    user_prompt = f"""Patient ID: {patientid}
Number of Images: {len(images)}
Image Metadata: {image_metadata}
Current Report: {report}

Analyze the provided medical image(s) in the context of the patient's current report and return a structured analysis as specified in the system prompt.
"""

    client = MedGemmaClient(system_prompt)
    
    # Process images - handle multiple images by analyzing first one (or combine if needed)
    # For now, analyze the first image
    if images and len(images) > 0:
        first_image = images[0]
        
        # Decode base64 image data
        if 'data' in first_image:
            try:
                image_bytes = base64.b64decode(first_image['data'])
                response = client.respond(user_prompt, image_object=image_bytes)
            except Exception as e:
                print(f"Error decoding image: {e}")
                response = client.respond(user_prompt)
        else:
            response = client.respond(user_prompt)
    else:
        response = client.respond(user_prompt)

    return response