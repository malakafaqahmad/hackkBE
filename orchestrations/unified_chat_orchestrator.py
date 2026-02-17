"""
Unified Chat Orchestrator
Handles the complete differential diagnosis workflow in a stateful manner
"""
import sys
from pathlib import Path
import json
import traceback
from typing import Dict, Any, Optional

# Add paths for imports
_module_dir = Path(__file__).parent.parent
_manageEhr_dir = _module_dir / 'manageEhr'

if str(_module_dir) not in sys.path:
    sys.path.insert(0, str(_module_dir))
if str(_manageEhr_dir) not in sys.path:
    sys.path.insert(0, str(_manageEhr_dir))

from session_manager import get_session_manager
from agents.sAgents.differentialdiagnosis.interviewer import interview_message
from agents.sAgents.differentialdiagnosis.secondinterviewer import second_interview_message
from agents.sAgents.differentialdiagnosis.ddGenerator import generate_differential_diagnosis
from agents.sAgents.differentialdiagnosis.finalReporter import finalReporter


class UnifiedChatOrchestrator:
    """Orchestrates the unified chat workflow for differential diagnosis"""
    
    def __init__(self):
        self.session_manager = get_session_manager()
    
    def process_message(
        self,
        conversation_id: Optional[str] = None,
        patient_id: Optional[str] = None,
        user_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a user message through the unified chat workflow
        
        Args:
            conversation_id: Existing conversation ID (for continuing)
            patient_id: Patient ID (for new conversations)
            user_message: User's message (optional for first call)
            
        Returns:
            Dict containing response data with phase, progress, message, etc.
            
        Raises:
            ValueError: If required parameters are missing
            Exception: If processing fails
        """
        try:
            # Load or create session
            session, is_new_session = self._load_or_create_session(conversation_id, patient_id)
            conversation_id = session['conversation_id']
            patient_id = session['patient_id']
            phase = session['phase']
            
            self._log_request(phase, user_message, conversation_id, session['message_counts'])
            
            # Response variables
            agent_response = None
            message_type = "question"
            phase_transition = False
            
            # If this is a new session, return the initial message
            if is_new_session:
                agent_response = session.get('initial_message', 'Session started')
                # Remove the flag
                if 'initial_message' in session:
                    self.session_manager.update_session(conversation_id, {'initial_message': None})
            # Route to appropriate phase handler
            elif phase == 'initial_interview':
                agent_response, message_type, phase_transition = self._handle_initial_interview(
                    session, user_message, conversation_id
                )
            
            elif phase == 'second_interview':
                agent_response, message_type, phase_transition = self._handle_second_interview(
                    session, user_message, conversation_id
                )
            
            elif phase == 'completed':
                agent_response = "The diagnostic process is complete. You can review the final report."
                message_type = "completed"
            
            else:
                raise Exception(f'Invalid phase: {phase}')
            
            # Build and return response
            return self._build_response(conversation_id, agent_response, message_type, phase_transition)
            
        except Exception as e:
            print(f"❌ Unexpected error in unified chat orchestrator: {str(e)}")
            traceback.print_exc()
            raise
    
    def _load_or_create_session(
        self,
        conversation_id: Optional[str],
        patient_id: Optional[str]
    ) -> tuple[Dict[str, Any], bool]:
        """
        Load existing session or create new one
        
        Returns:
            tuple: (session, is_new_session)
        """
        if conversation_id:
            session = self.session_manager.get_session(conversation_id)
            if not session:
                raise ValueError(f'Session not found: {conversation_id}')
            return session, False
        else:
            # New session - we need to start the interview first to get the conversation_id from MedGemma
            if not patient_id:
                raise ValueError('patient_id is required for new conversation')
            
            # Call interview_message to start and get the conversation_id from MedGemmaClient
            print(f"\n🆕 Starting new conversation for patient: {patient_id}")
            print("Calling interview agent to initialize session and get conversation_id from MedGemma...")
            print("the data is as follows: ")
            print(f"patient_id: {patient_id}")
            print(f"conversation_id: {conversation_id}")
            # print(f"user_message: {user_message}")
            
            result = interview_message(
                patient_id=patient_id,
                user_message=None,  # Start interview
                conversation_history=[],
                conversation_id=None,
                current_report=None
            )
            
            # Get the conversation_id from MedGemmaClient
            conversation_id = result.get('conversation_id')
            if not conversation_id:
                raise ValueError('Failed to get conversation_id from interviewer')
            
            print(f"✅ Received conversation_id from MedGemma: {conversation_id}")
            
            # Create session with the MedGemma conversation_id
            self.session_manager.create_session(conversation_id, patient_id)
            session = self.session_manager.get_session(conversation_id)
            
            # Store the initial response
            self.session_manager.update_session(conversation_id, {
                'initial_message': result['message']
            })
            
            # Update phase conversation ID (it's the same as main ID for phase 1)
            self.session_manager.update_session(conversation_id, {
                'phase_conversation_ids': {
                    'initial_interview': conversation_id
                }
            })
            
            # Add initial assistant message to history
            self.session_manager.append_to_history(conversation_id, 'assistant', result['message'])
            
            # Reload session to get updated data
            session = self.session_manager.get_session(conversation_id)
            
            return session, True
    
    def _handle_initial_interview(
        self,
        session: Dict[str, Any],
        user_message: Optional[str],
        conversation_id: str
    ) -> tuple:
        """
        Handle Phase 1: Initial Interview
        
        Returns:
            tuple: (agent_response, message_type, phase_transition)
        """
        phase_conv_id = session['phase_conversation_ids']['initial_interview']
        
        # Call interviewer agent
        result = interview_message(
            patient_id=session['patient_id'],
            user_message=user_message,
            conversation_history=session['conversation_history'],
            conversation_id=phase_conv_id,
            current_report=session['current_report']
        )
        
        agent_response = result['message']
        
        # Update session with result
        if result.get('conversation_id'):
            self.session_manager.update_session(conversation_id, {
                'phase_conversation_ids': {
                    'initial_interview': result['conversation_id']
                }
            })
        
        if result.get('updated_report'):
            self.session_manager.update_session(conversation_id, {
                'current_report': result['updated_report']
            })
        
        # Add to conversation history
        if user_message:
            self.session_manager.append_to_history(conversation_id, 'user', user_message)
            self.session_manager.increment_message_count(conversation_id, 'initial_interview')
        
        self.session_manager.append_to_history(conversation_id, 'assistant', agent_response)
        
        # Check if phase 1 is complete (10 user messages)
        session = self.session_manager.get_session(conversation_id)
        if session['message_counts']['initial_interview'] >= 10:
            return self._transition_to_second_interview(session, conversation_id)
        
        return agent_response, "question", False
    
    def _transition_to_second_interview(
        self,
        session: Dict[str, Any],
        conversation_id: str
    ) -> tuple:
        """
        Automatic transition from Phase 1 to Phase 3
        Includes diagnosis generation and second interview initialization
        
        Returns:
            tuple: (agent_response, message_type, phase_transition)
        """
        print("\n🔄 Phase 1 complete - transitioning to diagnosis generation...")
        
        # Update phase to diagnosis_generation
        self.session_manager.update_session(conversation_id, {
            'phase': 'diagnosis_generation'
        })
        
        # AUTOMATICALLY GENERATE DIAGNOSIS
        print("🧠 Generating differential diagnosis...")
        
        try:
            diagnosis_result = generate_differential_diagnosis(
                patient_id=session['patient_id'],
                conversation_history=session['conversation_history'],
                current_report=session['current_report']
            )
            
            print(f"✅ Diagnosis generated successfully")
            
            # Store differential diagnoses
            self.session_manager.update_session(conversation_id, {
                'differential_diagnoses': diagnosis_result,
                'phase': 'second_interview'
            })
            
            print("\n🔄 Transitioning to Phase 3 - Second Interview...")
            
            # AUTOMATICALLY START SECOND INTERVIEW (with empty message)
            session = self.session_manager.get_session(conversation_id)
            
            # Convert differential diagnoses to string format
            if isinstance(diagnosis_result, dict):
                dd_string = json.dumps(diagnosis_result, indent=2)
            else:
                dd_string = str(diagnosis_result)
            
            second_result = second_interview_message(
                patient_id=session['patient_id'],
                user_message=None,  # Empty message to start second interview
                conversation_history=session['conversation_history'],
                current_report=session['current_report'],
                differential_diagnoses=dd_string,
                conversation_id=None  # New conversation for second interview
            )
            
            print(f"✅ Second interview started successfully")
            
            # Store second interview conversation ID
            if second_result.get('conversation_id'):
                self.session_manager.update_session(conversation_id, {
                    'phase_conversation_ids': {
                        'second_interview': second_result['conversation_id']
                    }
                })
            
            # Update report if changed
            if second_result.get('updated_report'):
                self.session_manager.update_session(conversation_id, {
                    'current_report': second_result['updated_report']
                })
            
            # Update differential if changed
            if second_result.get('updated_differential'):
                self.session_manager.update_session(conversation_id, {
                    'differential_diagnoses': second_result['updated_differential']
                })
            
            # Add to conversation history
            agent_response = second_result['message']
            self.session_manager.append_to_history(conversation_id, 'assistant', agent_response)
            
            return agent_response, "question", True
            
        except Exception as e:
            print(f"❌ Error during phase transition: {str(e)}")
            traceback.print_exc()
            raise Exception(f'Failed to transition to second interview: {str(e)}')
    
    def _handle_second_interview(
        self,
        session: Dict[str, Any],
        user_message: Optional[str],
        conversation_id: str
    ) -> tuple:
        """
        Handle Phase 3: Second Interview
        
        Returns:
            tuple: (agent_response, message_type, phase_transition)
        """
        phase_conv_id = session['phase_conversation_ids']['second_interview']
        
        # Convert differential diagnoses to string
        dd = session.get('differential_diagnoses')
        if isinstance(dd, dict):
            dd_string = json.dumps(dd, indent=2)
        else:
            dd_string = str(dd) if dd else ""
        
        # Call second interviewer agent
        result = second_interview_message(
            patient_id=session['patient_id'],
            user_message=user_message,
            conversation_history=session['conversation_history'],
            current_report=session['current_report'],
            differential_diagnoses=dd_string,
            conversation_id=phase_conv_id
        )
        
        agent_response = result['message']
        
        # Update session with result
        if result.get('conversation_id'):
            self.session_manager.update_session(conversation_id, {
                'phase_conversation_ids': {
                    'second_interview': result['conversation_id']
                }
            })
        
        if result.get('updated_report'):
            self.session_manager.update_session(conversation_id, {
                'current_report': result['updated_report']
            })
        
        if result.get('updated_differential'):
            self.session_manager.update_session(conversation_id, {
                'differential_diagnoses': result['updated_differential']
            })
        
        # Add to conversation history
        if user_message:
            self.session_manager.append_to_history(conversation_id, 'user', user_message)
            self.session_manager.increment_message_count(conversation_id, 'second_interview')
        
        self.session_manager.append_to_history(conversation_id, 'assistant', agent_response)
        
        # Check if phase 3 is complete (10 user messages in second interview)
        session = self.session_manager.get_session(conversation_id)
        if session['message_counts']['second_interview'] >= 10:
            return self._generate_final_report(session, conversation_id)
        
        return agent_response, "question", False
    
    def _generate_final_report(
        self,
        session: Dict[str, Any],
        conversation_id: str
    ) -> tuple:
        """
        Generate final report after Phase 3 completion
        
        Returns:
            tuple: (agent_response, message_type, phase_transition)
        """
        print("\n🔄 Phase 3 complete - generating final report...")
        
        # Update phase
        self.session_manager.update_session(conversation_id, {
            'phase': 'final_report_generation'
        })
        
        # AUTOMATICALLY GENERATE FINAL REPORT
        print("📄 Generating final report...")
        
        try:
            # Format conversation history as string
            conv_history_str = "\n".join([
                f"{role.upper()}: {msg}" for role, msg in session['conversation_history']
            ])
            
            # Convert differential diagnoses to string
            dd = session.get('differential_diagnoses')
            if isinstance(dd, dict):
                dd_string = json.dumps(dd, indent=2)
            else:
                dd_string = str(dd) if dd else ""
            
            final_result = finalReporter(
                patient_id=session['patient_id'],
                conversation_history=conv_history_str,
                current_report=session['current_report'],
                differential_diagnoses=dd_string
            )
            
            if final_result.get('success'):
                print(f"✅ Final report generated successfully")
                
                # Store final report
                self.session_manager.update_session(conversation_id, {
                    'final_report': final_result['report'],
                    'phase': 'completed'
                })
                
                agent_response = "Thank you for completing the interview. I have generated a comprehensive final medical report based on our conversation."
                message_type = "final_report"
                
                return agent_response, message_type, True
            else:
                raise Exception(final_result.get('error', 'Unknown error'))
                
        except Exception as e:
            print(f"❌ Error generating final report: {str(e)}")
            traceback.print_exc()
            raise Exception(f'Failed to generate final report: {str(e)}')
    
    def _build_response(
        self,
        conversation_id: str,
        agent_response: str,
        message_type: str,
        phase_transition: bool
    ) -> Dict[str, Any]:
        """Build the final response dictionary"""
        session = self.session_manager.get_session(conversation_id)
        
        # Get the active conversation_id based on current phase
        # For second interview, use the phase-specific conversation_id
        active_conversation_id = conversation_id
        if session['phase'] in ['second_interview', 'final_report_generation', 'completed']:
            phase_ids = session.get('phase_conversation_ids', {})
            if 'second_interview' in phase_ids:
                active_conversation_id = phase_ids['second_interview']
                print(f"📍 Using second interview conversation_id: {active_conversation_id}")
        
        # Calculate progress
        current_phase_count = session['message_counts'].get(
            'initial_interview' if session['phase'] == 'initial_interview' else 'second_interview',
            0
        )
        
        if session['phase'] in ['diagnosis_generation', 'second_interview', 'final_report_generation', 'completed']:
            phase_limit = 10
            if session['phase'] in ['second_interview', 'final_report_generation', 'completed']:
                current_phase_count = session['message_counts']['second_interview']
        else:
            phase_limit = 10
        
        is_phase_complete = (
            (session['phase'] == 'initial_interview' and current_phase_count >= 10) or
            (session['phase'] == 'second_interview' and current_phase_count >= 10) or
            session['phase'] == 'completed'
        )
        
        # Determine next action
        if session['phase'] == 'completed':
            next_action = 'conversation_complete'
            expects_user_input = False
        elif session['phase'] in ['diagnosis_generation', 'final_report_generation']:
            next_action = 'continue_chat'
            expects_user_input = True
        else:
            next_action = 'continue_chat'
            expects_user_input = True
        
        # Build response - use active_conversation_id instead of main session conversation_id
        response_data = {
            'success': True,
            'conversation_id': active_conversation_id,
            'patient_id': session['patient_id'],
            'phase': session['phase'],
            'progress': {
                'current_phase_message_count': current_phase_count,
                'total_messages': session['message_counts']['total'],
                'phase_message_limit': phase_limit,
                'is_phase_complete': is_phase_complete
            },
            'message': agent_response,
            'message_type': message_type,
            'updated_report': session.get('current_report'),
            'differential_diagnoses': session.get('differential_diagnoses'),
            'final_report': session.get('final_report'),
            'expects_user_input': expects_user_input,
            'phase_transition': phase_transition,
            'next_action': next_action
        }
        
        print(f"\n✅ Response prepared - Phase: {session['phase']}, Expects input: {expects_user_input}\n")
        
        return response_data
    
    def _log_request(
        self,
        phase: str,
        user_message: Optional[str],
        conversation_id: str,
        message_counts: Dict[str, int]
    ):
        """Log request details for debugging"""
        print(f"\n{'='*60}")
        print(f"UNIFIED CHAT - Phase: {phase}, Message: {user_message}")
        print(f"Conversation ID: {conversation_id}")
        print(f"Message Counts: {message_counts}")
        print("conversation history is as follows: ")
        print(self.session_manager.get_session(conversation_id)['conversation_history'])
        print(f"{'='*60}\n")
