import json
import os
from datetime import datetime, timedelta

class MoodTracker:
    def __init__(self):
        self.data_file = "mood_data.json"
        self.mood_history = self._load_mood_data()
    
    def _load_mood_data(self):
        """Load mood data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_mood_data(self):
        """Save mood data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.mood_history, f, indent=2)
        except Exception as e:
            print(f"Error saving mood data: {e}")
    
    def log_mood(self, mood_data):
        """Log a new mood entry"""
        self.mood_history.append(mood_data)
        self._save_mood_data()
    
    def get_mood_history(self, days=30):
        """Get mood history for the last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        filtered_history = []
        for entry in self.mood_history:
            entry_date = datetime.fromisoformat(entry['timestamp'])
            if entry_date > cutoff_date:
                filtered_history.append(entry)
        
        return filtered_history
    
    def get_mood_stats(self):
        """Get mood statistics"""
        if not self.mood_history:
            return {}
        
        recent_history = self.get_mood_history(7)  
        
        stats = {
            'total_entries': len(self.mood_history),
            'recent_entries': len(recent_history),
            'avg_energy': sum(entry['energy'] for entry in recent_history) / len(recent_history) if recent_history else 0,
            'avg_anxiety': sum(entry['anxiety'] for entry in recent_history) / len(recent_history) if recent_history else 0,
        }
        
        return stats
