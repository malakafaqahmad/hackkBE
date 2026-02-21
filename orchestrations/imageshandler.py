from agents.sAgents.imageshandler.imager import imagesHandler
from agents.sAgents.imageshandler.reportupdater import reporter
from agents.sAgents.imageshandler.pdfer import reportHandler
from agents.sAgents.pdfreader import PDFReader
from ehr_store.patientdata import load_report
import json


def images_handler_orchestration(patientid, images):

    # Load current patient report
    report = load_report(patientid)
    
    # Convert report to string for AI processing
    if report:
        report_str = json.dumps(report, indent=2) if isinstance(report, dict) else str(report)
    else:
        report_str = "No existing report found for this patient."
    # print(f"\n📄 Current Report for Patient {patientid}:\n{report_str}")

    # Step 1: Analyze images and extract features
    image_analysis_results = imagesHandler(patientid, images, report_str)
    
    # Step 2: Update patient report with new insights from image analysis
    updated_report = reporter(patientid, image_analysis_results, report_str)

    return {
        'image_analysis_results': image_analysis_results,
        'updated_report': updated_report
    }


def pdf_handler_orchestration(patientid, pdf_file):
    # Placeholder for PDF handling orchestration
    # Load current patient report
    report = load_report(patientid)
    # Convert report to string for AI processing
    if report:
        report_str = json.dumps(report, indent=2) if isinstance(report, dict) else str(report)
    else:
        report_str = "No existing report found for this patient."

    # convert pdf file to text
    pdf_reader = PDFReader()
    pdf_text = pdf_reader.read(pdf_file)

    print(f"\n📄 Current Report for Patient {patientid}:\n{report_str}")
    print(f"\n📄 Extracted PDF Text:\n{pdf_text}")
    # Step 1: Analyze PDF report and extract insights
    pdf_analysis_results = reportHandler(patientid, pdf_text, report_str)
    # Step 2: Update patient report with new insights from PDF analysis
    updated_report = reporter(patientid, pdf_analysis_results, report_str)

    return {
        'pdf_analysis_results': pdf_analysis_results,
        'updated_report': updated_report
    }




