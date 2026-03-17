# Installation Guide - AI Surveillance System

## Quick Start (Recommended)

### Option 1: Using the run script (macOS/Linux)
```bash
chmod +x run.sh
./run.sh
```

### Option 2: Manual Installation

#### Step 1: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

#### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 3: Create Data Directories
```bash
mkdir -p data/frames data/alerts data/reports
```

#### Step 4: Run the Application
```bash
python app.py
```

#### Step 5: Access the System
Open your browser and navigate to:
```
http://localhost:5051
```

## Configuration

### 1. Environment Variables (Optional)
Copy `.env.example` to `.env` and configure:
```bash
cp .env.example .env
```

Edit `.env` to add:
- Email alert settings
- Custom camera URLs
- Detection thresholds

### 2. Camera Setup

#### Using Webcam (Default)
The system uses your default webcam (ID: 0) by default.

#### Using IP Cameras
Edit `config.py` and add your IP camera URLs:
```python
CAMERA_SOURCES = {
    'camera_1': 'rtsp://username:password@192.168.1.100:554/stream',
    'camera_2': 'http://192.168.1.101:8080/video',
}
```

### 3. Email Alerts Setup (Optional)

For Gmail:
1. Enable 2-factor authentication
2. Generate an App Password
3. Add to `.env`:
```
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ALERT_EMAIL=recipient@example.com
```

## System Requirements

### Minimum
- Python 3.8+
- 4GB RAM
- Webcam or IP camera
- Internet connection (for downloading models)

### Recommended
- Python 3.9+
- 8GB+ RAM
- GPU (for faster processing)
- Multiple camera support

## Troubleshooting

### Issue: Camera not detected
**Solution**: Check camera permissions and ensure it's not being used by another application.

### Issue: Module not found errors
**Solution**: 
```bash
pip install --upgrade -r requirements.txt
```

### Issue: Slow performance
**Solution**: 
- Reduce `FRAME_RATE` in `config.py`
- Use smaller YOLO model (yolov8n.pt)
- Reduce camera resolution

### Issue: YOLO model download fails
**Solution**: 
The model will auto-download on first run. Ensure internet connection.
Alternatively, download manually from: https://github.com/ultralytics/assets/releases

## Features Setup

### 1. Real-time Monitoring
- Start the system
- Click "Start Monitoring"
- View live feeds and alerts

### 2. Analytics Dashboard
- Access at `/dashboard`
- View historical data
- Generate reports

### 3. Alert System
- Configure in `config.py`
- Set thresholds for different alert types
- Enable email notifications

## Performance Optimization

### For Better Performance:
1. Use GPU acceleration (install CUDA + cuDNN)
2. Reduce frame processing rate
3. Use smaller models
4. Lower camera resolution

### For Better Accuracy:
1. Use larger YOLO models (yolov8m.pt, yolov8l.pt)
2. Adjust confidence thresholds
3. Train custom models for specific use cases

## Next Steps

1. ✅ Install and run the system
2. 🎥 Configure cameras
3. ⚙️ Adjust detection thresholds
4. 📧 Set up email alerts
5. 📊 Monitor and analyze

## Support

For issues or questions:
- Check troubleshooting section
- Review configuration settings
- Check camera connections
- Verify Python version compatibility

## Updates

To update the system:
```bash
git pull  # If using version control
pip install --upgrade -r requirements.txt
```
