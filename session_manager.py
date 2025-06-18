import json
import os
from datetime import datetime, timedelta

class SessionManager:
    def __init__(self):
        self.data_file = "sessions.json"
        self.sessions = self._load_sessions()
        self.current_session_id = self._create_new_session()
    
    def _load_sessions(self):
        """Load sessions from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_sessions(self):
        """Save sessions to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.sessions, f, indent=2)
        except Exception as e:
            print(f"Error saving sessions: {e}")
    
    def _create_new_session(self):
        """Create a new session"""
        session_id = f"session_{len(self.sessions) + 1}"
        self.sessions[session_id] = {
            'id': session_id,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'messages': [],
            'duration': 0,
            'status': 'active'
        }
        self._save_sessions()
        return session_id
    
    def get_current_session(self):
        """Get the current active session"""
        return self.sessions.get(self.current_session_id, {})
    
    def add_message(self, role, content, emotion=None):
        """Add a message to the current session"""
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'emotion': emotion
        }
        
        if self.current_session_id in self.sessions:
            self.sessions[self.current_session_id]['messages'].append(message)
            self._save_sessions()
    
    def get_sessions(self):
        """Get all sessions"""
        return self.sessions
    
    def get_latest_session(self):
        """Get the most recent session"""
        if not self.sessions:
            return None
        
        latest_session = max(self.sessions.values(), key=lambda x: x['date'])
        return latest_session
    
    def clear_current_session(self):
        """Clear the current session"""
        if self.current_session_id in self.sessions:
            self.sessions[self.current_session_id]['messages'] = []
            self._save_sessions()
    
    def auto_delete_old_sessions(self, days=30):
        """Auto-delete sessions older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        sessions_to_delete = []
        for session_id, session in self.sessions.items():
            session_date = datetime.strptime(session['date'], "%Y-%m-%d %H:%M:%S")
            if session_date < cutoff_date:
                sessions_to_delete.append(session_id)
        
        for session_id in sessions_to_delete:
            del self.sessions[session_id]
        
        if sessions_to_delete:
            self._save_sessions()
        
        return len(sessions_to_delete)