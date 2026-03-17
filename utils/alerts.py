"""
Alert management system
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from config import Config

class AlertManager:
    def __init__(self, database):
        """Initialize alert manager"""
        self.db = database
        self.last_alert_time = {}
        self.alert_cooldown = Config.ALERT_COOLDOWN
        
    def send_alert(self, alert):
        """Send alert notification"""
        alert_key = f"{alert['type']}_{alert['camera_id']}"
        
        # Check cooldown
        if alert_key in self.last_alert_time:
            time_since_last = datetime.now() - self.last_alert_time[alert_key]
            if time_since_last < self.alert_cooldown:
                return False
        
        # Log to console
        severity_emoji = {
            'critical': '🚨',
            'high': '⚠️',
            'medium': '⚡',
            'low': 'ℹ️'
        }
        emoji = severity_emoji.get(alert['severity'], '📢')
        print(f"{emoji} ALERT [{alert['severity'].upper()}]: {alert['message']} (Camera: {alert['camera_id']})")
        
        # Send email if configured
        if Config.SMTP_USERNAME and Config.SMTP_PASSWORD:
            try:
                self._send_email_alert(alert)
            except Exception as e:
                print(f"Failed to send email alert: {e}")
        
        # Update last alert time
        self.last_alert_time[alert_key] = datetime.now()
        
        return True
    
    def _send_email_alert(self, alert):
        """Send email notification"""
        msg = MIMEMultipart()
        msg['From'] = Config.SMTP_USERNAME
        msg['To'] = Config.ALERT_EMAIL
        msg['Subject'] = f"[{alert['severity'].upper()}] Surveillance Alert - {alert['type']}"
        
        body = f"""
        AI Surveillance System Alert
        
        Type: {alert['type']}
        Severity: {alert['severity']}
        Camera: {alert['camera_id']}
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        Message: {alert['message']}
        
        Please review the surveillance dashboard for more details.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
            server.starttls()
            server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
            server.send_message(msg)
    
    def get_active_alerts(self):
        """Get currently active alerts"""
        return list(self.last_alert_time.keys())
    
    def clear_alerts(self):
        """Clear all alert states"""
        self.last_alert_time.clear()
