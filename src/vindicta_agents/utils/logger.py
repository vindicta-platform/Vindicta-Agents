import sqlite3
import json
import uuid
from datetime import datetime
from typing import Any, Dict, Optional
import os

class FlightRecorder:
    """
    SQLite-based logger for Swarm events and Axiomatic decisions.
    Acts as a 'Black Box' for the Swarm.
    """
    def __init__(self, db_path: str = "swarm_flight_recorder.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the SQLite database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS flight_log (
                id TEXT PRIMARY KEY,
                timestamp DATETIME,
                trace_id TEXT,
                component TEXT,
                event_type TEXT,
                details JSON
            )
        ''')
        
        conn.commit()
        conn.close()

    def log_event(self, trace_id: str, component: str, event_type: str, details: Dict[str, Any]):
        """
        Log an event to the Flight Recorder.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        event_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        cursor.execute(
            'INSERT INTO flight_log (id, timestamp, trace_id, component, event_type, details) VALUES (?, ?, ?, ?, ?, ?)',
            (event_id, timestamp, trace_id, component, event_type, json.dumps(details))
        )
        
        conn.commit()
        conn.close()
        # Also print to stdout for immediate visibility in this stage
        print(f"[{component.upper()}] {event_type}: {trace_id}")

    def fetch_logs(self, trace_id: Optional[str] = None):
        """
        Retrieve logs, optionally filtered by trace_id.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if trace_id:
            cursor.execute('SELECT * FROM flight_log WHERE trace_id = ? ORDER BY timestamp DESC', (trace_id,))
        else:
            cursor.execute('SELECT * FROM flight_log ORDER BY timestamp DESC LIMIT 100')
            
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return rows
