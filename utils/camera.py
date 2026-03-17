"""
Camera management system
"""

import cv2
import threading
import time

class CameraManager:
    def __init__(self, camera_sources):
        """Initialize camera manager with multiple sources"""
        self.camera_sources = camera_sources
        self.cameras = {}
        self.frames = {}
        self.active = {}
        self.threads = {}
        
    def start_camera(self, camera_id):
        """Start a specific camera"""
        if camera_id in self.cameras and self.cameras[camera_id] is not None:
            return True
            
        source = self.camera_sources.get(camera_id)
        if source is None:
            print(f"Camera {camera_id} not found in sources")
            return False
        
        try:
            cap = cv2.VideoCapture(source)
            if not cap.isOpened():
                print(f"Failed to open camera {camera_id}")
                return False
            
            self.cameras[camera_id] = cap
            self.active[camera_id] = True
            
            # Start capture thread
            thread = threading.Thread(target=self._capture_loop, args=(camera_id,))
            thread.daemon = True
            thread.start()
            self.threads[camera_id] = thread
            
            print(f"✅ Camera {camera_id} started")
            return True
            
        except Exception as e:
            print(f"Error starting camera {camera_id}: {e}")
            return False
    
    def _capture_loop(self, camera_id):
        """Continuous frame capture loop"""
        while self.active.get(camera_id, False):
            try:
                cap = self.cameras.get(camera_id)
                if cap is None or not cap.isOpened():
                    break
                
                ret, frame = cap.read()
                if ret:
                    self.frames[camera_id] = frame
                else:
                    print(f"Failed to read from camera {camera_id}")
                    time.sleep(0.1)
                    
            except Exception as e:
                print(f"Error in capture loop for {camera_id}: {e}")
                time.sleep(1)
    
    def get_frame(self, camera_id):
        """Get the latest frame from a camera"""
        return self.frames.get(camera_id)
    
    def stop_camera(self, camera_id):
        """Stop a specific camera"""
        self.active[camera_id] = False
        
        if camera_id in self.cameras and self.cameras[camera_id] is not None:
            self.cameras[camera_id].release()
            self.cameras[camera_id] = None
        
        print(f"🛑 Camera {camera_id} stopped")
    
    def start_all(self):
        """Start all cameras"""
        for camera_id in self.camera_sources:
            self.start_camera(camera_id)
    
    def stop_all(self):
        """Stop all cameras"""
        for camera_id in list(self.cameras.keys()):
            self.stop_camera(camera_id)
    
    def get_status(self):
        """Get status of all cameras"""
        status = {}
        for camera_id in self.camera_sources:
            status[camera_id] = {
                'active': self.active.get(camera_id, False),
                'has_frame': camera_id in self.frames
            }
        return status
    
    def __del__(self):
        """Cleanup on deletion"""
        self.stop_all()
