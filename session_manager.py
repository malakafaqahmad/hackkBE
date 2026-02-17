"""
Session Manager for Unified Chat Endpoint
Handles state management for the differential diagnosis workflow
"""
from typing import Dict, Any, Optional
from datetime import datetime
import json


class SessionManager:
    """Manages conversation sessions with in-memory storage"""
    
    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}
    
    def create_session(self, conversation_id: str, patient_id: str) -> str:
        """
        Create a new session for a patient with the conversation_id from MedGemmaClient
        
        Args:
            conversation_id: The conversation ID returned by MedGemmaClient
            patient_id: The patient's ID
            
        Returns:
            conversation_id: The conversation identifier
        """
        self._sessions[conversation_id] = {
            'conversation_id': conversation_id,
            'patient_id': patient_id,
            'phase': 'initial_interview',
            'message_counts': {
                'initial_interview': 0,
                'second_interview': 0,
                'total': 0
            },
            'conversation_history': [],
            'current_report': None,
            'differential_diagnoses': None,
            'final_report': None,
            'phase_conversation_ids': {
                'initial_interview': None,  # Will be same as main conversation_id
                'second_interview': None    # Will be different for second interview
            },
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        return conversation_id
    
    def get_session(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """
        Get session by conversation_id
        
        Args:
            conversation_id: The conversation ID (can be main or phase-specific)
            
        Returns:
            Session data or None if not found
        """
        # First, try direct lookup (main conversation_id)
        if conversation_id in self._sessions:
            return self._sessions[conversation_id]
        
        # If not found, search for phase-specific conversation_id
        for session_id, session_data in self._sessions.items():
            phase_ids = session_data.get('phase_conversation_ids', {})
            if conversation_id in phase_ids.values():
                # Found it as a phase-specific ID, return the main session
                print(f"🔍 Resolved phase conversation_id {conversation_id} to main session {session_id}")
                return session_data
        
        return None
    
    def update_session(self, conversation_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update session data
        
        Args:
            conversation_id: The conversation ID
            updates: Dictionary of fields to update
            
        Returns:
            True if successful, False if session not found
        """
        if conversation_id not in self._sessions:
            return False
        
        # Update timestamp
        updates['updated_at'] = datetime.now().isoformat()
        
        # Deep merge for nested fields
        for key, value in updates.items():
            if key in ['message_counts', 'phase_conversation_ids'] and isinstance(value, dict):
                self._sessions[conversation_id][key].update(value)
            else:
                self._sessions[conversation_id][key] = value
        
        return True
    
    def delete_session(self, conversation_id: str) -> bool:
        """
        Delete a session
        
        Args:
            conversation_id: The conversation ID
            
        Returns:
            True if deleted, False if not found
        """
        if conversation_id in self._sessions:
            del self._sessions[conversation_id]
            return True
        return False
    
    def increment_message_count(self, conversation_id: str, phase: str) -> bool:
        """
        Increment message count for a specific phase
        
        Args:
            conversation_id: The conversation ID
            phase: The phase name (initial_interview or second_interview)
            
        Returns:
            True if successful, False if session not found
        """
        if conversation_id not in self._sessions:
            return False
        
        self._sessions[conversation_id]['message_counts'][phase] += 1
        self._sessions[conversation_id]['message_counts']['total'] += 1
        self._sessions[conversation_id]['updated_at'] = datetime.now().isoformat()
        
        return True
    
    def append_to_history(self, conversation_id: str, role: str, message: str) -> bool:
        """
        Append a message to conversation history
        
        Args:
            conversation_id: The conversation ID
            role: The role (user or assistant)
            message: The message content
            
        Returns:
            True if successful, False if session not found
        """
        if conversation_id not in self._sessions:
            return False
        
        self._sessions[conversation_id]['conversation_history'].append((role, message))
        self._sessions[conversation_id]['updated_at'] = datetime.now().isoformat()
        
        return True


# Global session manager instance
_session_manager = SessionManager()


def get_session_manager() -> SessionManager:
    """Get the global session manager instance"""
    return _session_manager
