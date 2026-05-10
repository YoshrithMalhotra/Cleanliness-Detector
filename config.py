"""
Configuration settings for AI Surveillance System
"""

import os
from datetime import timedelta

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = True
    

    CAMERA_SOURCES = {
        'camera_1': 0,  
    }
    
    FRAME_RATE = 1  
    FRAME_WIDTH = 640
    FRAME_HEIGHT = 480
    
    CONFIDENCE_THRESHOLD = 0.4
    NMS_THRESHOLD = 0.5
    
    CLEANLINESS_CLASSES = [
        'garbage_bag',
        'trash',
        'litter',
        'graffiti',
        'dirty_surface',
        'spill'
    ]
    
    SAFETY_CLASSES = [
        'person',
        'car',
        'truck',
        'weapon',
        'fire',
        'smoke'
    ]
    

    MAX_PEOPLE_COUNT = 75
    MIN_CLEANLINESS_SCORE = 0.5
    

    ALERT_EMAIL = os.environ.get('ALERT_EMAIL') or 'admin@example.com'
    SMTP_SERVER = os.environ.get('SMTP_SERVER') or 'smtp.gmail.com'
    SMTP_PORT = int(os.environ.get('SMTP_PORT') or 587)
    SMTP_USERNAME = os.environ.get('SMTP_USERNAME') or ''
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD') or ''
    

    DATABASE_PATH = 'data/surveillance.db'
    

    SAVE_FRAMES = True
    FRAMES_DIR = 'data/frames'
    ALERTS_DIR = 'data/alerts'
    REPORTS_DIR = 'data/reports'
    
    
    YOLO_MODEL = 'yolov8n.pt'  
    CUSTOM_CLEANLINESS_MODEL = 'models/cleanliness_detector.pt'
    

    DETECTION_INTERVAL = timedelta(seconds=2)
    ALERT_COOLDOWN = timedelta(minutes=5)  

