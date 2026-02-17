from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
from pathlib import Path
import json
import traceback

# Add paths for imports
_module_dir = Path(__file__).parent
_manageEhr_dir = _module_dir / 'manageEhr'

if str(_module_dir) not in sys.path:
    sys.path.insert(0, str(_module_dir))
if str(_manageEhr_dir) not in sys.path:
    sys.path.insert(0, str(_manageEhr_dir))

app = Flask(__name__)
CORS(app) 


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Differential Diagnosis API'
    }), 200


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
        
        print(f"Result from orchestrator: {result}")
        print("Returning response to client...")

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


@app.route('/api/interview', methods=['POST'])
def interview():
    """
    Handle interview messages - both starting and continuing the conversation
    
    Expected JSON body:
    {
        "patient_id": "p1",
        "message": "I have chest pain" (optional - omit to start interview),
        "conversation_history": [{"role": "assistant", "content": "..."}, {"role": "user", "content": "..."}] (optional),
        "conversation_id": "abc123" (optional - for continuing conversation)
    }
    """
    try:
        from agents.sAgents.differentialdiagnosis.interviewer import interview_message
        
        data = request.get_json()
        
        if not data or 'patient_id' not in data:
            return jsonify({
                'error': 'Missing required field: patient_id'
            }), 400
        
        patient_id = data['patient_id']
        user_message = data.get('message', None)
        conversation_history = data.get('conversation_history', [])
        conversation_id = data.get('conversation_id', None)
        report = data.get('current_report', None)
        
        # Convert conversation history from frontend format to tuple format
        formatted_history = [(msg['role'], msg['content']) for msg in conversation_history] if conversation_history else []
        
        # Process the message (or start interview if no message)
        result = interview_message(patient_id, user_message, formatted_history, conversation_id, report)
        
        return jsonify({
            'success': True,
            'patient_id': result['patient_id'],
            'message': result['message'],
            'updated_report': result['updated_report'],
            'conversation_id': result['conversation_id']
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
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


@app.route('/api/diagnosis', methods=['POST'])
def generate_diagnosis():
    """
    Generate differential diagnosis based on patient report and conversation
    
    Expected JSON body:
    {
        "patient_id": "p1",
        "conversation_history": [{"role": "assistant", "content": "..."}, {"role": "user", "content": "..."}],
        "current_report": "# Medical Report..." (required)
    }
    """
    try:
        from agents.sAgents.differentialdiagnosis.ddGenerator import generate_differential_diagnosis
        
        data = request.get_json()
        
        if not data or 'patient_id' not in data or 'current_report' not in data:
            return jsonify({
                'error': 'Missing required fields: patient_id and current_report'
            }), 400
        
        patient_id = data['patient_id']
        current_report = data['current_report']
        conversation_history = data.get('conversation_history', [])
        
        # Convert conversation history from frontend format to tuple format
        formatted_history = [(msg['role'], msg['content']) for msg in conversation_history] if conversation_history else []
        
        # Generate differential diagnosis
        result = generate_differential_diagnosis(patient_id, formatted_history, current_report)
        print("Generated differential diagnosis:", result)
        
        return jsonify({
            'success': True,
            'patient_id': result['patient_id'],
            'differential_diagnoses': result,
            'raw_response': result.get('raw_response', '')
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500


@app.route('/api/second-interview', methods=['POST'])
def second_interview():
    """
    Handle second interview messages - focused follow-up based on differential diagnosis
    
    Expected JSON body:
    {
        "patient_id": "p1",
        "message": "Yes, it gets worse when I lie down" (optional - omit to start),
        "conversation_history": [{"role": "assistant", "content": "..."}, {"role": "user", "content": "..."}] (optional),
        "current_report": "# Medical Report..." (required),
        "differential_diagnoses": "[{...}]" (required),
        "conversation_id": "abc123" (optional)
    }
    """
    try:
        from agents.sAgents.differentialdiagnosis.secondinterviewer import second_interview_message
        
        data = request.get_json()
        
        if not data or 'patient_id' not in data or 'current_report' not in data or 'differential_diagnoses' not in data:
            return jsonify({
                'error': 'Missing required fields: patient_id, current_report, and differential_diagnoses'
            }), 400
        
        patient_id = data['patient_id']
        user_message = data.get('message', None)
        conversation_history = data.get('conversation_history', [])
        current_report = data['current_report']
        differential_diagnoses = data['differential_diagnoses']
        conversation_id = data.get('conversation_id', None)
        print("Received second interview request with data:", conversation_id)
        
        # Convert conversation history from frontend format to tuple format
        formatted_history = [(msg['role'], msg['content']) for msg in conversation_history] if conversation_history else []
        
        # Process the message (or start second interview if no message)
        result = second_interview_message(
            patient_id,
            user_message,
            formatted_history,
            current_report,
            differential_diagnoses,
            conversation_id
        )
        print("the updated differential diagnosis after second interview:", result['updated_differential'])
        
        return jsonify({
            'success': True,
            'patient_id': result['patient_id'],
            'message': result['message'],
            'updated_report': result['updated_report'],
            'updated_differential': result['updated_differential'],
            'conversation_id': result['conversation_id']
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500


@app.route('/api/final-report', methods=['POST'])
def generate_final_report():
    """
    Generate comprehensive final medical report
    
    Expected JSON body:
    {
        "patient_id": "p1",
        "conversation_history": "Complete conversation transcript...",
        "current_report": "# Medical Report..." (required),
        "differential_diagnoses": "[{...}]" or "Diagnosis text..." (required)
    }
    """
    try:
        from agents.sAgents.differentialdiagnosis.finalReporter import finalReporter
        
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                'error': 'No data provided',
                'success': False
            }), 400
            
        if 'patient_id' not in data:
            return jsonify({
                'error': 'Missing required field: patient_id',
                'success': False
            }), 400
            
        if 'current_report' not in data:
            return jsonify({
                'error': 'Missing required field: current_report',
                'success': False
            }), 400
            
        if 'differential_diagnoses' not in data:
            return jsonify({
                'error': 'Missing required field: differential_diagnoses',
                'success': False
            }), 400
        
        patient_id = data['patient_id']
        conversation_history = data.get('conversation_history', '')
        current_report = data['current_report']
        differential_diagnoses = data['differential_diagnoses']

        print("Received final report generation request with conversation:", conversation_history)
        print("Current report:", current_report)
        print("Differential diagnoses:", differential_diagnoses)
        
        # Convert differential_diagnoses to string if it's a dict/list
        if isinstance(differential_diagnoses, (dict, list)):
            import json
            differential_diagnoses = json.dumps(differential_diagnoses, indent=2)
        
        print('final report generating')
        
        # Generate final report
        result = finalReporter(
            patient_id=patient_id,
            conversation_history=conversation_history,
            current_report=current_report,
            differential_diagnoses=differential_diagnoses
        )
        print("Generated final report:", result)
        
        # Return the result (already structured by finalReporter)
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 500
        
    except Exception as e:
        return jsonify({
            'error': f'Unexpected error: {str(e)}',
            'success': False
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
