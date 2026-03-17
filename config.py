"""
Configuration settings for AI Surveillance System
"""

import os
from datetime import timedelta

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = True
    
    # Camera settings
    CAMERA_SOURCES = {
        'camera_1': 0,  # Default webcam, change to IP camera URL if needed
        # 'camera_2': 'rtsp://username:password@ip:port/stream',
    }
    
    # Frame processing
    FRAME_RATE = 30  # Process every Nth frame
    FRAME_WIDTH = 640
    FRAME_HEIGHT = 480
    
    # Detection thresholds
    CONFIDENCE_THRESHOLD = 0.5
    NMS_THRESHOLD = 0.4
    
    # Cleanliness detection
    CLEANLINESS_CLASSES = [
        'garbage_bag',
        'trash',
        'litter',
        'graffiti',
        'dirty_surface',
        'spill'
    ]
    
    # Safety detection
    SAFETY_CLASSES = [
        'person',
        'car',
        'truck',
        'weapon',
        'fire',
        'smoke'
    ]
    
    # Alert thresholds
    MAX_PEOPLE_COUNT = 50  # Overcrowding threshold
    MIN_CLEANLINESS_SCORE = 0.7  # 0-1, lower means dirtier
    
    # Alert settings
    ALERT_EMAIL = os.environ.get('ALERT_EMAIL') or 'admin@example.com'
    SMTP_SERVER = os.environ.get('SMTP_SERVER') or 'smtp.gmail.com'
    SMTP_PORT = int(os.environ.get('SMTP_PORT') or 587)
    SMTP_USERNAME = os.environ.get('SMTP_USERNAME') or ''
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD') or ''
    
    # Database
    DATABASE_PATH = 'data/surveillance.db'
    
    # Storage
    SAVE_FRAMES = True
    FRAMES_DIR = 'data/frames'
    ALERTS_DIR = 'data/alerts'
    REPORTS_DIR = 'data/reports'
    
    # Model paths
    YOLO_MODEL = 'yolov8n.pt'  # nano model for speed
    CUSTOM_CLEANLINESS_MODEL = 'models/cleanliness_detector.pt'
    
    # Detection intervals
    DETECTION_INTERVAL = timedelta(seconds=2)
    ALERT_COOLDOWN = timedelta(minutes=5)  # Don't send duplicate alerts within this time
