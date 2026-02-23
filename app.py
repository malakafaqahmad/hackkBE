from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
from pathlib import Path
import json
import traceback
import base64
import io
from PIL import Image
from agents.sAgents.pdfreader import PDFReader
from orchestrations.imageshandler import images_handler_orchestration, pdf_handler_orchestration
from ehr_store.patientdata.data_manager import get_daily_logs, get_recent_daily_logs, save_report

# Add paths for imports
_module_dir = Path(__file__).parent
_manageEhr_dir = _module_dir / 'manageEhr'

if str(_module_dir) not in sys.path:
    sys.path.insert(0, str(_module_dir))
if str(_manageEhr_dir) not in sys.path:
    sys.path.insert(0, str(_manageEhr_dir))

app = Flask(__name__)
CORS(app)

# Initialize PDF Reader
pdf_reader = PDFReader() 


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Differential Diagnosis API'
    }), 200

@app.route("/pdf-reader", methods=["POST"])
def read_pdf():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    extracted_text = pdf_reader.read(file)

    return jsonify({
        "status": "success",
        "text": extracted_text
    })


@app.route('/api/chat', methods=['POST'])
def unified_chat():
    """
    Unified chat endpoint that handles the entire diagnostic workflow:
    - Phase 1: Initial interview (messages 1-10)
    - Phase 2: Diagnosis generation (automatic after message 10)
    - Phase 3: Second interview (messages 11-20)
    - Phase 4: Final report generation (automatic after message 20)
    
    Expected JSON body:
    {
        "patient_id": "p1",                    // Required for new session
        "message": "I have chest pain",        // Optional: User's message (null to start/continue)
        "conversation_id": "uuid-string"       // Optional: For continuing existing conversation
        "conversation_history": list          // Optional: Full conversation history for context
    }
    
    Returns:
    {
        "success": true,
        "conversation_id": "uuid-123",
        "patient_id": "p1",
        "phase": "initial_interview",
        "progress": {
            "current_phase_message_count": 5,
            "total_messages": 5,
            "phase_message_limit": 10,
            "is_phase_complete": false
        },
        "message": "Can you describe your chest pain?",
        "message_type": "question",
        "updated_report": "# Medical Report\\n...",
        "differential_diagnoses": null,
        "final_report": null,
        "expects_user_input": true,
        "phase_transition": false,
        "next_action": "continue_chat"
    }
    """
    try:
        print("\n" + "="*60)
        print("📨 Received request to /api/chat")
        print("="*60)
        
        from orchestrations.unified_chat_orchestrator import UnifiedChatOrchestrator
        
        data = request.get_json()
        print(f"📦 Request data: {data}")
        
        if not data:
            return jsonify({
                'error': 'No data provided',
                'success': False
            }), 400
        
        # Initialize orchestrator and process request
        orchestrator = UnifiedChatOrchestrator()
        print("Processing chat message through orchestrator...")
        print(f"Input to orchestrator: conversation_id={data.get('conversation_id')}, patient_id={data.get('patient_id')}, message={data.get('message')}")
        
        result = orchestrator.process_message(
            conversation_id=data.get('conversation_id'),
            patient_id=data.get('patient_id'),
            user_message=data.get('message')
        )
        
        print(f"Result from orchestrator: {result.get('final_report')}")
        if result.get("final_report"):
            save_report(data.get('patient_id'), result.get("final_report"))
        # print("Returning response to client...")

        return jsonify(result), 200
    
    except ValueError as ve:
        # Handle validation errors (missing patient_id, session not found, etc.)
        return jsonify({
            'error': str(ve),
            'success': False
        }), 400 if 'required' in str(ve).lower() else 404
    
    except Exception as e:
        print(f"❌ Unexpected error in unified_chat: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'error': f'Unexpected error: {str(e)}',
            'success': False,
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/patients', methods=['GET'])
def list_patients():
    """List available patients"""
    try:
        from manageEhr.ehr_manager import EHRManager
        
        ehr_manager = EHRManager()
        patients = ehr_manager.get_patients()
        
        return jsonify({
            'success': True,
            'patients': patients
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500


@app.route('/api/exercise-plan', methods=['POST'])
def generate_exercise_plan():
    """
    Generate personalized exercise plan for a patient
    
    Expected JSON body:
    {
        "patient_id": "p1",                    // Required: Patient's ID
        "current_report": "...",               // Required: Current clinical report
        "current_diet": "..."                  // Required: Current diet information
    }
    
    Returns:
    {
        "success": true,
        "patient_id": "p1",
        "exercise_plan": "Complete exercise prescription report..."
    }
    """
    try:
        print("\n" + "="*60)
        print("📨 Received request to /api/exercise-plan")
        print("="*60)
        
        from orchestrations.exercise_pipeline import exercisePipeline
        
        data = request.get_json()
        print(f"📦 Request data: {data}")
        
        if not data:
            return jsonify({
                'error': 'No data provided',
                'success': False
            }), 400
        
        # Validate required fields
        patient_id = data.get('patient_id')
        current_report = data.get('current_report')
        current_diet = data.get('current_diet')
        
        if not patient_id:
            return jsonify({
                'error': 'patient_id is required',
                'success': False
            }), 400
        
        if not current_report:
            return jsonify({
                'error': 'current_report is required',
                'success': False
            }), 400
        
        if not current_diet:
            return jsonify({
                'error': 'current_diet is required',
                'success': False
            }), 400
        
        print(f"🏃 Generating exercise plan for patient: {patient_id}")
        
        # Generate exercise plan
        exercise_plan = exercisePipeline(
            patient_id=patient_id,
            current_report=current_report,
            current_diet=current_diet
        )
        
        print("✅ Exercise plan generated successfully")
        
        return jsonify({
            'success': True,
            'patient_id': patient_id,
            'exercise_plan': exercise_plan
        }), 200
    
    except Exception as e:
        print(f"❌ Error generating exercise plan: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'error': f'Failed to generate exercise plan: {str(e)}',
            'success': False,
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/diet-plan', methods=['POST'])
def generate_diet_plan():
    """
    Generate personalized diet plan for a patient
    
    Expected JSON body:
    {
        "patient_id": "p1",                    // Required: Patient's ID
        "current_report": "..."                // Required: Current clinical report
    }
    
    Returns:
    {
        "success": true,
        "patient_id": "p1",
        "diet_plan": "Complete diet plan report..."
    }
    """
    try:
        print("\n" + "="*60)
        print("📨 Received request to /api/diet-plan")
        print("="*60)
        
        from orchestrations.diet_Planner import dietPlanner
        
        data = request.get_json()
        print(f"📦 Request data: {data}")
        
        if not data:
            return jsonify({
                'error': 'No data provided',
                'success': False
            }), 400
        
        # Validate required fields
        patient_id = data.get('patient_id')
        current_report = data.get('current_report')
        
        if not patient_id:
            return jsonify({
                'error': 'patient_id is required',
                'success': False
            }), 400
        
        if not current_report:
            return jsonify({
                'error': 'current_report is required',
                'success': False
            }), 400
        
        print(f"🥗 Generating diet plan for patient: {patient_id}")
        
        # Generate diet plan
        diet_plan = dietPlanner(
            patient_id=patient_id,
            current_report=current_report
        )
        
        print("✅ Diet plan generated successfully")
        
        return jsonify({
            'success': True,
            'patient_id': patient_id,
            'diet_plan': diet_plan
        }), 200
    
    except Exception as e:
        print(f"❌ Error generating diet plan: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'error': f'Failed to generate diet plan: {str(e)}',
            'success': False,
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/first-aid', methods=['POST'])
def generate_first_aid():
    """
    Generate first aid emergency response for a patient
    
    Expected JSON body:
    {
        "patient_id": "p1",                    // Required: Patient's ID
        "current_symptoms": "..."              // Required: Current emergency symptoms
    }
    
    Returns:
    {
        "success": true,
        "patient_id": "p1",
        "emergency_report": "Complete emergency response report..."
    }
    """
    try:
        print("\n" + "="*60)
        print("📨 Received request to /api/first-aid")
        print("="*60)
        
        from orchestrations.first_aid_pipeline import firstAidPipeline
        
        data = request.get_json()
        print(f"📦 Request data: {data}")
        
        if not data:
            return jsonify({
                'error': 'No data provided',
                'success': False
            }), 400
        
        # Validate required fields
        patient_id = data.get('patient_id')
        current_symptoms = data.get('current_symptoms')
        
        if not patient_id:
            return jsonify({
                'error': 'patient_id is required',
                'success': False
            }), 400
        
        if not current_symptoms:
            return jsonify({
                'error': 'current_symptoms is required',
                'success': False
            }), 400
        
        print(f"🚨 Generating first aid response for patient: {patient_id}")
        
        # Generate first aid response
        emergency_report = firstAidPipeline(
            patient_id=patient_id,
            current_symptoms=current_symptoms
        )
        
        print("✅ First aid report generated successfully")
        
        return jsonify({
            'success': True,
            'patient_id': patient_id,
            'emergency_report': emergency_report
        }), 200
    
    except Exception as e:
        print(f"❌ Error generating first aid report: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'error': f'Failed to generate first aid report: {str(e)}',
            'success': False,
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/medicine-check', methods=['POST'])
def check_medicine_safety():
    """
    Verify medication safety and check for contraindications
    
    Expected JSON body:
    {
        "patient_id": "p1",                    // Required: Patient's ID
        "current_report": "...",               // Required: Current clinical report
        "prescription_data": {                 // Required: Prescription information
            "prescriber": "Dr. Smith",
            "date": "2024-01-15",
            "medications": [
                {
                    "name": "Metformin",
                    "dose": "500mg",
                    "frequency": "BID",
                    "route": "PO",
                    "indication": "Type 2 Diabetes"
                }
            ]
        }
    }
    
    Returns:
    {
        "success": true,
        "patient_id": "p1",
        "safety_report": {
            "patient_summary": "...",
            "parsed_prescription": "...",
            "contraindication": "...",
            "interactions": "...",
            "dose_check": "...",
            "appropriateness": "...",
            "risk_aggregation": "...",
            "final_report": "..."
        }
    }
    """
    try:
        print("\n" + "="*60)
        print("📨 Received request to /api/medicine-check")
        print("="*60)
        
        from orchestrations.medicine_double_check_pipeline import medicineDoubleCheckPipeline
        from agents.sAgents.cache import get_ehr_summary
        from agents.sAgents.differentialdiagnosis.ehrReport import ehr_summary_to_report
        
        data = request.get_json()
        print(f"📦 Request data: {data}")
        
        if not data:
            return jsonify({
                'error': 'No data provided',
                'success': False
            }), 400
        
        # Validate required fields
        patient_id = data.get('patient_id')
        current_report = data.get('current_report')
        prescription_data = data.get('prescription_data')
        
        if not patient_id:
            return jsonify({
                'error': 'patient_id is required',
                'success': False
            }), 400
        
        if not current_report:
            return jsonify({
                'error': 'current_report is required',
                'success': False
            }), 400
        
        if not prescription_data:
            return jsonify({
                'error': 'prescription_data is required',
                'success': False
            }), 400
        
        print(f"💊 Checking medication safety for patient: {patient_id}")
        
        # Get EHR summary
        ehr_summary = get_ehr_summary(patient_id, ehr_summary_to_report)
        
        # Perform medicine double check
        safety_report = medicineDoubleCheckPipeline(
            patient_id=patient_id,
            ehr_summary=ehr_summary,
            current_report=current_report,
            prescription_data=prescription_data
        )
        
        print("✅ Medicine safety check completed successfully")
        
        return jsonify({
            'success': True,
            'patient_id': patient_id,
            'safety_report': safety_report
        }), 200
    
    except Exception as e:
        print(f"❌ Error checking medicine safety: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'error': f'Failed to check medicine safety: {str(e)}',
            'success': False,
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/patients/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get patient EHR summary"""
    try:
        from manageEhr.ehr_manager import EHRManager
        
        ehr_manager = EHRManager()
        patient_data = ehr_manager.get_patient_full_record(patient_id)
        
        return jsonify({
            'success': True,
            'patient_id': patient_id,
            'data': patient_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500


@app.route('/api/digital-twin/analyze', methods=['POST'])
def digital_twin_analyze():
    """
    Digital Twin Analysis Endpoint
    
    Comprehensive health monitoring and predictive analytics system that:
    - Analyzes patient health data at multiple time scales (daily/weekly/monthly)
    - Predicts future health trajectories
    - Identifies medication adherence issues
    - Evaluates lifestyle factors
    - Generates prioritized clinical alerts
    - Performs deviation analysis (forecast vs actual)
    
    Expected JSON body:
    {
        "patient_id": "p1",                    // Required: Patient identifier
        "daily_logs": {                        // Required: Today's logs
            "date": "2026-02-21",
            "medications_taken": [
                {
                    "medication_name": "Lisinopril 10mg",
                    "prescribed_time": "08:00",
                    "actual_time": "08:15",
                    "taken": true
                }
            ],
            "vitals": {
                "blood_pressure_systolic": 128,
                "blood_pressure_diastolic": 82,
                "heart_rate": 72,
                "temperature_f": 98.6,
                "blood_glucose_mg_dl": 105,
                "weight_lbs": 180,
                "oxygen_saturation_percent": 98
            },
            "symptoms": [
                {
                    "symptom": "headache",
                    "severity": "mild",
                    "time_reported": "14:30"
                }
            ],
            "exercise": {
                "exercise_minutes": 30,
                "type": "walking",
                "intensity": "moderate"
            },
            "nutrition": {
                "meals": [
                    {
                        "meal_time": "morning",
                        "items": [
                            {"food_name": "oatmeal_cooked", "portion_size_g": 200}
                        ]
                    }
                ]
            },
            "labs": [],
            "notes": "Feeling good today"
        },
    }
    
    Returns:
    {
        "success": true,
        "patient_id": "p1",
        "execution_timestamp": "2026-02-21",
        "executive_summary": {
            "overall_health_status": "good",
            "health_score": 75.5,
            "trajectory": "improving",
            "deviation_status": "on_track",
            "critical_alerts": 0,
            "requires_immediate_attention": false,
            "key_recommendations": [...]
        },
        "patient_context": {...},
        "processed_logs": {...},
        "memory_profiles": {...},
        "analysis_results": {
            "medication_adherence": {...},
            "lifestyle_evaluation": {...},
            "symptoms_correlation": {...}
        },
        "health_forecast": {...},
        "clinical_alerts": {...},
        "digital_twin_state": {...},
        "deviation_analysis": {...}
    }
    """
    try:
        print("\n" + "="*80)
        print("🤖 Digital Twin Analysis Request Received")
        print("="*80)
        
        from orchestrations.digital_twin import digitaltwinpipeline
        
        data = request.get_json()
        print(f"📦 Request data keys: {list(data.keys()) if data else 'None'}")
        print(f"📦 Request data keys: {list(data.get('daily_logs', {}).keys()) if data else 'None'}")

        
        if not data:
            return jsonify({
                'error': 'No data provided',
                'success': False
            }), 400
        
        # Validate required fields
        patient_id = data.get('patient_id')
        daily_logs = data['daily_logs']

        if not patient_id:
            return jsonify({
                'error': 'patient_id is required',
                'success': False
            }), 400
        
        print(daily_logs)
        
        
        # Run the pipeline
        result = digitaltwinpipeline(patient_id, daily_logs)
        
        print("✅ Digital Twin Pipeline completed successfully")
        print(f"📈 Health Score: {result['executive_summary']['health_score']}")
        print(f"📊 Overall Status: {result['executive_summary']['overall_health_status']}")
        print(f"⚠️  Critical Alerts: {result['executive_summary']['critical_alerts']}")
        
        return jsonify({
            'success': True,
            'patient_id': patient_id,
            'execution_timestamp': result['pipeline_metadata']['execution_timestamp'],
            'executive_summary': result['executive_summary'],
            'patient_context': result['patient_context'],
            'processed_logs': result['processed_logs'],
            'memory_profiles': result['memory_profiles'],
            'analysis_results': result['analysis_results'],
            'health_forecast': result['health_forecast'],
            'clinical_alerts': result['clinical_alerts'],
            'digital_twin_state': result['digital_twin_state'],
            'deviation_analysis': result['deviation_analysis']
        }), 200
    
    except ValueError as ve:
        print(f"❌ Validation error: {str(ve)}")
        return jsonify({
            'error': f'Validation error: {str(ve)}',
            'success': False
        }), 400
    
    except Exception as e:
        print(f"❌ Error in digital twin analysis: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'error': f'Failed to complete digital twin analysis: {str(e)}',
            'success': False,
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/digital-twin/quick-check', methods=['POST'])
def digital_twin_quick_check():
    """
    Quick Digital Twin Health Check Endpoint
    
    Simplified endpoint for daily health check without full analysis.
    Returns only executive summary and critical alerts.
    
    Expected JSON body:
    {
        "patient_id": "p1",
        "daily_logs": {...}        // Only today's logs required
    }
    
    Returns abbreviated response with:
    - Overall health status
    - Critical alerts
    - Quick recommendations
    """
    try:
        print("\n" + "="*80)
        print("⚡ Digital Twin Quick Check Request")
        print("="*80)
        
        data = request.get_json()
        print(data)
        
        if not data or not data.get('patient_id') or not data.get('daily_logs'):
            return jsonify({
                'error': 'patient_id and daily_logs are required',
                'success': False
            }), 400
        
        patient_id = data['patient_id']
        daily_logs = data['daily_logs']
        
        print(f"🏃 Quick check for patient: {patient_id}")
        
        # Import required agents for quick check
        from agents.sAgents.digitaltwin.patientContextAgent import pca
        from agents.sAgents.digitaltwin.logsAgent import dailylogsAgent
        from agents.sAgents.digitaltwin.alertGeneratorAgent import alertGeneratorAgent
        
        # Load patient context
        patient_context = pca(patient_id)
        patient_context = json.loads(patient_context) if isinstance(patient_context, str) else patient_context
        
        # Process daily logs
        daily_summary = dailylogsAgent(patient_id, patient_context, daily_logs)
        daily_summary = json.loads(daily_summary) if isinstance(daily_summary, str) else daily_summary
        
        # Generate alerts for today only
        alerts = alertGeneratorAgent(
            patient_id,
            patient_context,
            daily_summary,
            {},  # No weekly logs
            {},  # No monthly logs
            {}   # No forecast
        )
        alerts = json.loads(alerts) if isinstance(alerts, str) else alerts
        
        print(f"✅ Quick check completed")
        print(f"📊 Overall day status: {daily_summary.get('overall_day_status', 'N/A')}")
        print(f"⚠️  Critical alerts: {alerts.get('alert_summary', {}).get('critical_count', 0)}")
        
        return jsonify({
            'success': True,
            'patient_id': patient_id,
            'date': daily_logs.get('date'),
            'overall_day_status': daily_summary.get('overall_day_status'),
            'medication_adherence': daily_summary.get('medication_adherence'),
            'vitals_summary': daily_summary.get('vitals_summary'),
            'critical_alerts': alerts.get('alert_summary', {}).get('critical_count', 0),
            'high_priority_alerts': alerts.get('alert_summary', {}).get('high_priority_count', 0),
            'top_alerts': [a for a in alerts.get('alerts', []) if a['priority'] in ['critical', 'high']][:5],
            'requires_immediate_attention': alerts.get('alert_summary', {}).get('requires_immediate_attention', False)
        }), 200
    
    except Exception as e:
        print(f"❌ Error in quick check: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'error': f'Failed to complete quick check: {str(e)}',
            'success': False
        }), 500


@app.route('/api/document-analyzer', methods=['POST'])
def document_analyzer():
    """
    Unified Document Analyzer API - Handles Images and PDFs
    
    Automatically detects file type and routes to appropriate handler:
    - Images (JPG, PNG, etc.) → Image analysis pipeline
    - PDFs → PDF extraction and analysis pipeline
    
    Request Format (multipart/form-data):
    - patient_id: string (required) - Patient identifier
    - file: file (required) - Single image or PDF file
    
    Supported File Types:
    - Images: .jpg, .jpeg, .png, .bmp, .gif, .tiff
    - Documents: .pdf
    
    Response Format:
    {
        "success": true,
        "patient_id": "p1",
        "file_info": {
            "filename": "xray.jpg",
            "type": "image",
            "size_kb": 245.3
        },
        "handler_used": "image_handler",
        "analysis_results": {...},
        "updated_report": "...",
        "processing_time_seconds": 45.2
    }
    
    Example Usage:
    ```bash
    # With image
    curl -X POST http://localhost:5000/api/document-analyzer \
      -F "patient_id=p1" \
      -F "file=@xray.jpg"
    
    # With PDF
    curl -X POST http://localhost:5000/api/document-analyzer \
      -F "patient_id=p1" \
      -F "file=@lab_report.pdf"
    ```
    """
    import time
    start_time = time.time()
    
    try:
        # Validate patient_id
        patient_id = request.form.get('patient_id')
        if not patient_id:
            return jsonify({
                'success': False,
                'error': 'Missing required field: patient_id'
            }), 400
        
        # Validate file
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded. Please provide an image or PDF file.'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Empty filename'
            }), 400
        
        # Get file extension
        file_ext = Path(file.filename).suffix.lower()
        
        # Allowed file extensions
        IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.tif', '.dcm'}
        PDF_EXTENSIONS = {'.pdf'}
        ALLOWED_EXTENSIONS = IMAGE_EXTENSIONS | PDF_EXTENSIONS
        
        # Validate file type
        if file_ext not in ALLOWED_EXTENSIONS:
            return jsonify({
                'success': False,
                'error': f'Invalid file type: {file.filename}. Allowed: images (jpg, png, etc.) or PDF'
            }), 400
        
        # Max file size: 10MB
        MAX_FILE_SIZE = 10 * 1024 * 1024
        
        # Read file content
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        # Validate file size
        if file_size > MAX_FILE_SIZE:
            return jsonify({
                'success': False,
                'error': f'File too large: {file.filename} ({file_size / 1024 / 1024:.2f}MB). Max size: 10MB'
            }), 413
        
        print(f"\n{'='*80}")
        print(f"📄 DOCUMENT ANALYZER - Processing Request")
        print(f"{'='*80}")
        print(f"Patient ID: {patient_id}")
        print(f"File: {file.filename}")
        print(f"Size: {file_size / 1024:.2f} KB")
        print(f"Extension: {file_ext}")
        
        # Route to appropriate handler based on file type
        handler_used = None
        result = None
        
        if file_ext in IMAGE_EXTENSIONS:
            # Process as IMAGE
            handler_used = "image_handler"
            print(f"🖼️  Detected IMAGE file - routing to image handler...")
            
            try:
                # Read and encode image
                file_content = file.read()
                file.seek(0)
                
                # Validate image
                img = Image.open(io.BytesIO(file_content))
                img_format = img.format or 'Unknown'
                img_size = img.size
                
                # Convert to base64
                img_base64 = base64.b64encode(file_content).decode('utf-8')
                
                # Prepare image data
                images_data = [{
                    'filename': file.filename,
                    'type': 'image',
                    'data': img_base64,
                    'format': img_format,
                    'dimensions': f'{img_size[0]}x{img_size[1]}'
                }]
                
                file_info = {
                    'filename': file.filename,
                    'type': 'image',
                    'size_kb': round(file_size / 1024, 2),
                    'format': img_format,
                    'dimensions': f'{img_size[0]}x{img_size[1]}'
                }
                
                # Call image handler orchestration
                result = images_handler_orchestration(
                    patientid=patient_id,
                    images=images_data
                )
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': f'Invalid image file: {file.filename}',
                    'details': str(e)
                }), 400
        
        elif file_ext in PDF_EXTENSIONS:
            # Process as PDF
            handler_used = "pdf_handler"
            print(f"📑 Detected PDF file - routing to PDF handler...")
            
            try:
                # Reset file pointer
                file.seek(0)
                
                file_info = {
                    'filename': file.filename,
                    'type': 'pdf',
                    'size_kb': round(file_size / 1024, 2)
                }
                
                # Call PDF handler orchestration
                result = pdf_handler_orchestration(
                    patientid=patient_id,
                    pdf_file=file
                )
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': f'Invalid PDF file: {file.filename}',
                    'details': str(e)
                }), 400
        
        # Parse results
        if handler_used == "image_handler":
            analysis_results = result.get('image_analysis_results', {})
            analysis_key = 'image_analysis_results'
        else:
            analysis_results = result.get('pdf_analysis_results', {})
            analysis_key = 'pdf_analysis_results'
        
        updated_report = result.get('updated_report', 'Report update failed')
        
        # Try to parse JSON responses if they're strings
        if isinstance(analysis_results, str):
            try:
                analysis_results = json.loads(analysis_results)
            except:
                pass
        
        if isinstance(updated_report, str) and updated_report.startswith('{'):
            try:
                updated_report = json.loads(updated_report)
            except:
                pass
        
        processing_time = round(time.time() - start_time, 2)
        
        print(f"\n✅ Processing completed successfully!")
        print(f"⏱️  Processing time: {processing_time}s")
        print(f"🔧 Handler used: {handler_used}")
        print(f"{'='*80}\n")
        
        # Return comprehensive response
        return jsonify({
            'success': True,
            'patient_id': patient_id,
            'file_info': file_info,
            'handler_used': handler_used,
            analysis_key: analysis_results,
            'updated_report': updated_report,
            'processing_time_seconds': processing_time,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }), 200
        
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"\n❌ ERROR in document analyzer:")
        print(error_trace)
        
        return jsonify({
            'success': False,
            'error': 'Internal server error during document processing',
            'details': str(e),
            'trace': error_trace if app.debug else None
        }), 500


@app.route('/api/logs/<patient_id>', methods=['GET'])
def get_logs(patient_id):
    try:
        logs = get_recent_daily_logs(patient_id, 10)
        return jsonify({
            'success': True,
            'patient_id': patient_id,
            'logs': logs
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to retrieve logs for patient {patient_id}',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
