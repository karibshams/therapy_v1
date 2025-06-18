import json
import os
from datetime import datetime

class JournalManager:
    def __init__(self):
        self.data_file = "journal_entries.json"
        self.entries = self._load_entries()
    
    def _load_entries(self):
        """Load journal entries from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_entries(self):
        """Save journal entries to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.entries, f, indent=2)
        except Exception as e:
            print(f"Error saving journal entries: {e}")
    
    def save_entry(self, entry_data):
        """Save a new journal entry"""
        entry_data['id'] = len(self.entries) + 1
        self.entries.append(entry_data)
        self._save_entries()
    
    def get_recent_entries(self, limit=10):
        """Get recent journal entries"""
        return sorted(self.entries, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def search_entries(self, keyword):
        """Search journal entries by keyword"""
        matching_entries = []
        for entry in self.entries:
            if keyword.lower() in entry['content'].lower():
                matching_entries.append(entry)
        return matching_entries
    
    def get_entry_by_id(self, entry_id):
        """Get a specific journal entry by ID"""
        for entry in self.entries:
            if entry['id'] == entry_id:
                return entry
        return None