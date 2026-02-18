from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
from pathlib import Path
import json
import traceback
from agents.sAgents.pdfreader import PDFReader

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
        
        # print(f"Result from orchestrator: {result}")
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




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
