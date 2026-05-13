"""
Unified detection system combining cleanliness and safety detection
"""

import cv2
import numpy as np
from ultralytics import YOLO
import torch

from config import Config

class UnifiedDetector:
    def __init__(self):
        """Initialize detection models"""
        print("🔧 Loading AI models...")
        
        # Load YOLO model for general object detection
        try:
            self.yolo_model = YOLO(Config.YOLO_MODEL)
            print("✅ YOLO model loaded")
        except Exception as e:
            print(f"⚠️  Error loading YOLO model: {e}")
            print("📥 Downloading YOLO model...")
            self.yolo_model = YOLO('yolov8n.pt')  # Will auto-download
        
        self.confidence_threshold = Config.CONFIDENCE_THRESHOLD
        
        # Detection categories
        self.cleanliness_items = ['bottle', 'cup', 'fork', 'knife', 'spoon', 
                                  'bowl', 'banana', 'apple', 'sandwich', 'orange']
        self.safety_items = ['person', 'car', 'truck', 'bus', 'motorcycle', 'bicycle']
        
    def detect(self, frame):
        """
        Run detection on frame
        Returns dict with detection results
        """
        results = {
            'people_count': 0,
            'vehicles_count': 0,
            'cleanliness_score': 1.0,
            'safety_issues': [],
            'detections': [],
            'garbage_detected': False
        }
        
        try:
            # Run YOLO detection
            yolo_results = self.yolo_model(frame, conf=self.confidence_threshold, verbose=False)
            
            if len(yolo_results) > 0:
                result = yolo_results[0]
                
                # Parse detections
                if result.boxes is not None:
                    boxes = result.boxes.cpu().numpy()
                    
                    for box in boxes:
                        cls_id = int(box.cls[0])
                        confidence = float(box.conf[0])
                        class_name = self.yolo_model.names[cls_id]
                        
                        # Get bounding box
                        x1, y1, x2, y2 = box.xyxy[0]
                        
                        detection = {
                            'class': class_name,
                            'confidence': confidence,
                            'bbox': [int(x1), int(y1), int(x2), int(y2)]
                        }
                        results['detections'].append(detection)
                        
                        # Count people
                        if class_name == 'person':
                            results['people_count'] += 1
                        
                        # Count vehicles
                        if class_name in ['car', 'truck', 'bus', 'motorcycle']:
                            results['vehicles_count'] += 1
                        
                        # Detect cleanliness issues
                        if class_name in self.cleanliness_items:
                            results['garbage_detected'] = True
                            results['cleanliness_score'] *= 0.9
            
            # Analyze cleanliness based on detections
            if results['garbage_detected']:
                results['cleanliness_score'] = max(0.0, min(1.0, results['cleanliness_score']))
            
            # Detect safety issues
            if results['people_count'] > Config.MAX_PEOPLE_COUNT:
                results['safety_issues'].append('Overcrowding detected')
            
        except Exception as e:
            print(f"Detection error: {e}")
        
        return results
    
    def draw_detections(self, frame, results):
        """Draw detection results on frame"""
        annotated_frame = frame.copy()
        
        # Draw each detection
        for detection in results['detections']:
            bbox = detection['bbox']
            class_name = detection['class']
            confidence = detection['confidence']
            
            # Choose color based on category
            if class_name == 'person':
                color = (0, 255, 0)  # Green for people
            elif class_name in self.cleanliness_items:
                color = (0, 165, 255)  # Orange for garbage
            else:
                color = (255, 0, 0)  # Blue for others
            
            # Draw bounding box
            cv2.rectangle(annotated_frame, 
                         (bbox[0], bbox[1]), 
                         (bbox[2], bbox[3]), 
                         color, 2)
            
            # Draw label
            label = f"{class_name}: {confidence:.2f}"
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(annotated_frame, 
                         (bbox[0], bbox[1] - label_size[1] - 10),
                         (bbox[0] + label_size[0], bbox[1]),
                         color, -1)
            cv2.putText(annotated_frame, label, 
                       (bbox[0], bbox[1] - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Draw info panel...
        info_height = 120
        overlay = annotated_frame.copy()
        cv2.rectangle(overlay, (0, 0), (300, info_height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, annotated_frame, 0.4, 0, annotated_frame)
        
        # Display statistics
        cv2.putText(annotated_frame, f"People: {results['people_count']}", 
                   (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(annotated_frame, f"Vehicles: {results['vehicles_count']}", 
                   (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(annotated_frame, f"Cleanliness: {results['cleanliness_score']:.2f}", 
                   (10, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Display safety alert if issues detected
        if results['safety_issues']:
            cv2.putText(annotated_frame, "⚠️ ALERT!", 
                       (10, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        return annotated_frame