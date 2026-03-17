# AI Surveillance System for Cleanliness and Public Safety

## Overview
An intelligent surveillance system that uses computer vision and deep learning to monitor public spaces for:
- **Cleanliness Monitoring**: Detect garbage, litter, graffiti, and dirty areas
- **Public Safety**: Detect overcrowding, unauthorized access, suspicious activities, and safety violations

## Features
- Real-time video analysis
- Object detection (people, vehicles, garbage, etc.)
- Anomaly detection
- Alert system for critical events
- Dashboard for monitoring
- Historical data analysis
- Report generation

## Technology Stack
- **Backend**: Python, Flask
- **Computer Vision**: OpenCV, YOLOv8 (Ultralytics)
- **Deep Learning**: TensorFlow/PyTorch
- **Database**: SQLite (can be upgraded to PostgreSQL)
- **Frontend**: HTML, CSS, JavaScript
- **Alerts**: Email notifications

## Installation

### Prerequisites
- Python 3.8+
- Webcam or IP camera access

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## Usage
1. Access the web interface at `http://localhost:5000`
2. Configure camera sources
3. Start monitoring
4. View real-time alerts and analytics


## Project Structure
```
PBL/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── config.py             # Configuration settings
├── models/               # AI models
│   ├── detector.py       # Object detection
│   ├── cleanliness_model.py  # Cleanliness detection
│   └── safety_model.py   # Safety detection
├── utils/                # Utility functions
│   ├── camera.py         # Camera handling
│   ├── alerts.py         # Alert system
│   └── database.py       # Database operations
├── static/               # Static files (CSS, JS)
├── templates/            # HTML templates
└── data/                 # Data storage
```

## License
MIT License
