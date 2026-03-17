"""
Database management for surveillance data
"""

import sqlite3
import json
from datetime import datetime, timedelta
from contextlib import contextmanager

class Database:
    def __init__(self, db_path):
        """Initialize database connection"""
        self.db_path = db_path
    
    @contextmanager
    def get_connection(self):
        """Get database connection context manager"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def initialize(self):
        """Create database tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Alerts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    camera_id TEXT NOT NULL,
                    type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    message TEXT NOT NULL,
                    resolved BOOLEAN DEFAULT 0
                )
            ''')
            
            # Detections table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS detections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    camera_id TEXT NOT NULL,
                    people_count INTEGER,
                    vehicles_count INTEGER,
                    cleanliness_score REAL,
                    details TEXT
                )
            ''')
            
            # Analytics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    camera_id TEXT NOT NULL,
                    metric_type TEXT NOT NULL,
                    metric_value REAL,
                    details TEXT
                )
            ''')
            
            print("✅ Database initialized")
    
    def save_alert(self, alert):
        """Save alert to database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO alerts (camera_id, type, severity, message)
                VALUES (?, ?, ?, ?)
            ''', (alert['camera_id'], alert['type'], alert['severity'], alert['message']))
    
    def save_detection(self, camera_id, results):
        """Save detection results to database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO detections (camera_id, people_count, vehicles_count, 
                                       cleanliness_score, details)
                VALUES (?, ?, ?, ?, ?)
            ''', (camera_id, 
                  results.get('people_count', 0),
                  results.get('vehicles_count', 0),
                  results.get('cleanliness_score', 1.0),
                  json.dumps(results)))
    
    def get_recent_alerts(self, limit=50):
        """Get recent alerts"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM alerts 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_analytics(self, hours=24):
        """Get analytics for the past N hours"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            since = datetime.now() - timedelta(hours=hours)
            
            # Get detection stats
            cursor.execute('''
                SELECT 
                    camera_id,
                    AVG(people_count) as avg_people,
                    MAX(people_count) as max_people,
                    AVG(cleanliness_score) as avg_cleanliness,
                    COUNT(*) as total_detections
                FROM detections
                WHERE timestamp > ?
                GROUP BY camera_id
            ''', (since,))
            
            detection_stats = [dict(row) for row in cursor.fetchall()]
            
            # Get alert stats
            cursor.execute('''
                SELECT 
                    camera_id,
                    type,
                    COUNT(*) as count
                FROM alerts
                WHERE timestamp > ?
                GROUP BY camera_id, type
            ''', (since,))
            
            alert_stats = [dict(row) for row in cursor.fetchall()]
            
            return {
                'detection_stats': detection_stats,
                'alert_stats': alert_stats,
                'time_range': hours
            }
    
    def mark_alert_resolved(self, alert_id):
        """Mark an alert as resolved"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE alerts 
                SET resolved = 1 
                WHERE id = ?
            ''', (alert_id,))
