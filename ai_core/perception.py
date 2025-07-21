import cv2
import numpy as np
from typing import List, Dict, Tuple
import logging

class CandlePerception:
    """Advanced candle detection using computer vision - trained like a 100-billion-year entity"""
    
    def __init__(self):
        self.name = "COSMIC PERCEPTION ENGINE"
        self.logger = logging.getLogger(__name__)
        
    def detect_candles(self, image: np.ndarray) -> List[Dict]:
        """Ultra-precise candle detection with multiple validation layers"""
        try:
            height, width = image.shape[:2]
            
            # Multi-stage preprocessing for maximum accuracy
            enhanced_image = self._enhance_image(image)
            
            # Detect candles using multiple methods and combine results
            hsv_candles = self._detect_hsv_candles(enhanced_image)
            edge_candles = self._detect_edge_candles(enhanced_image)
            morphology_candles = self._detect_morphology_candles(enhanced_image)
            
            # Combine and validate all detections
            all_candles = hsv_candles + edge_candles + morphology_candles
            validated_candles = self._validate_and_merge_candles(all_candles, image.shape)
            
            return validated_candles
            
        except Exception as e:
            self.logger.error(f"Candle detection failed: {e}")
            return []
    
    def _enhance_image(self, image: np.ndarray) -> np.ndarray:
        """Multi-layer image enhancement for perfect candle visibility"""
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(image, (3, 3), 0)
        
        # Convert to HSV for better color separation
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        
        # Enhance saturation and value channels
        hsv[:,:,1] = np.clip(hsv[:,:,1] * 1.3, 0, 255)  # Boost saturation
        hsv[:,:,2] = np.clip(hsv[:,:,2] * 1.1, 0, 255)  # Boost brightness
        
        # Apply adaptive histogram equalization to V channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        hsv[:,:,2] = clahe.apply(hsv[:,:,2])
        
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    def _detect_hsv_candles(self, image: np.ndarray) -> List[Dict]:
        """HSV-based candle detection with precise color ranges"""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Precise color ranges for different broker color schemes
        green_ranges = [
            (np.array([45, 80, 80]), np.array([75, 255, 255])),    # Standard green
            (np.array([35, 60, 60]), np.array([85, 255, 255])),    # Light green
            (np.array([40, 100, 100]), np.array([70, 255, 255]))   # Dark green
        ]
        
        red_ranges = [
            (np.array([0, 80, 80]), np.array([10, 255, 255])),     # Red 1
            (np.array([170, 80, 80]), np.array([180, 255, 255])),  # Red 2
            (np.array([0, 60, 60]), np.array([15, 255, 255])),     # Light red
            (np.array([165, 60, 60]), np.array([180, 255, 255]))   # Dark red
        ]
        
        candles = []
        
        # Process green candles
        for lower, upper in green_ranges:
            mask = cv2.inRange(hsv, lower, upper)
            mask = self._clean_mask(mask)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                candle = self._process_contour(contour, 'bullish')
                if candle:
                    candles.append(candle)
        
        # Process red candles
        for lower, upper in red_ranges:
            mask = cv2.inRange(hsv, lower, upper)
            mask = self._clean_mask(mask)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                candle = self._process_contour(contour, 'bearish')
                if candle:
                    candles.append(candle)
        
        return candles
    
    def _detect_edge_candles(self, image: np.ndarray) -> List[Dict]:
        """Edge-based candle detection for complex backgrounds"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Canny edge detection
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        
        # Find contours from edges
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        candles = []
        for contour in contours:
            # Analyze the area inside the contour to determine candle type
            x, y, w, h = cv2.boundingRect(contour)
            if self._is_valid_candle_shape(w, h, image.shape[0]):
                roi = image[y:y+h, x:x+w]
                candle_type = self._determine_candle_type_from_roi(roi)
                
                if candle_type:
                    candle = self._create_candle_object(x, y, w, h, candle_type)
                    candles.append(candle)
        
        return candles
    
    def _detect_morphology_candles(self, image: np.ndarray) -> List[Dict]:
        """Morphological operations for candle detection"""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Create binary mask for potential candle areas
        _, sat_thresh = cv2.threshold(hsv[:,:,1], 30, 255, cv2.THRESH_BINARY)
        _, val_thresh = cv2.threshold(hsv[:,:,2], 40, 255, cv2.THRESH_BINARY)
        
        combined_mask = cv2.bitwise_and(sat_thresh, val_thresh)
        
        # Apply morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 10))
        opened = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
        
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        candles = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if self._is_valid_candle_shape(w, h, image.shape[0]):
                roi = image[y:y+h, x:x+w]
                candle_type = self._determine_candle_type_from_roi(roi)
                
                if candle_type:
                    candle = self._create_candle_object(x, y, w, h, candle_type)
                    candles.append(candle)
        
        return candles
    
    def _clean_mask(self, mask: np.ndarray) -> np.ndarray:
        """Clean mask using advanced morphological operations"""
        # Remove small noise
        kernel_small = np.ones((2,2), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_small)
        
        # Fill gaps in candle bodies
        kernel_medium = np.ones((3,3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_medium)
        
        # Remove horizontal lines (grid lines)
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 1))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, horizontal_kernel)
        
        return mask
    
    def _process_contour(self, contour, candle_type: str) -> Dict:
        """Process contour and create candle object if valid"""
        area = cv2.contourArea(contour)
        if area < 50:  # Minimum area threshold
            return None
        
        x, y, w, h = cv2.boundingRect(contour)
        
        if not self._is_valid_candle_shape(w, h, None, area):
            return None
        
        return self._create_candle_object(x, y, w, h, candle_type)
    
    def _is_valid_candle_shape(self, width: int, height: int, image_height: int = None, area: int = None) -> bool:
        """Enhanced candle shape validation"""
        # Basic geometry filters
        if height < 8 or width < 2:
            return False
        
        if image_height and height > image_height * 0.6:
            return False
        
        if width > height:  # Candles should be taller than wide
            return False
        
        # Aspect ratio validation
        aspect_ratio = height / width if width > 0 else 0
        if aspect_ratio < 1.5 or aspect_ratio > 25:
            return False
        
        # Area validation if provided
        if area and area < width * height * 0.5:
            return False
        
        return True
    
    def _determine_candle_type_from_roi(self, roi: np.ndarray) -> str:
        """Determine candle type from region of interest"""
        if roi.size == 0:
            return None
        
        # Convert to HSV and analyze dominant colors
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # Check for green colors
        green_mask = cv2.inRange(hsv_roi, np.array([35, 50, 50]), np.array([85, 255, 255]))
        green_pixels = cv2.countNonZero(green_mask)
        
        # Check for red colors
        red_mask1 = cv2.inRange(hsv_roi, np.array([0, 50, 50]), np.array([15, 255, 255]))
        red_mask2 = cv2.inRange(hsv_roi, np.array([165, 50, 50]), np.array([180, 255, 255]))
        red_pixels = cv2.countNonZero(red_mask1) + cv2.countNonZero(red_mask2)
        
        total_pixels = roi.shape[0] * roi.shape[1]
        
        if green_pixels > total_pixels * 0.1:
            return 'bullish'
        elif red_pixels > total_pixels * 0.1:
            return 'bearish'
        
        return None
    
    def _create_candle_object(self, x: int, y: int, w: int, h: int, candle_type: str) -> Dict:
        """Create standardized candle object"""
        return {
            'type': candle_type,
            'x': x, 'y': y, 'width': w, 'height': h,
            'center_x': x + w // 2,
            'center_y': y + h // 2,
            'body_ratio': w / h if h > 0 else 0,
            'area': w * h,
            'aspect_ratio': h / w if w > 0 else 0,
            'confidence': self._calculate_candle_confidence(w, h, candle_type)
        }
    
    def _calculate_candle_confidence(self, width: int, height: int, candle_type: str) -> float:
        """Calculate confidence score for detected candle"""
        confidence = 0.5  # Base confidence
        
        # Size-based confidence
        if height > 15:
            confidence += 0.2
        if height > 25:
            confidence += 0.1
        
        # Aspect ratio confidence
        aspect_ratio = height / width if width > 0 else 0
        if 2 <= aspect_ratio <= 10:
            confidence += 0.2
        
        return min(confidence, 1.0)
    
    def _validate_and_merge_candles(self, candles: List[Dict], image_shape: Tuple) -> List[Dict]:
        """Validate and merge overlapping candle detections"""
        if not candles:
            return []
        
        # Remove duplicates and overlapping detections
        unique_candles = []
        for candle in candles:
            is_duplicate = False
            for existing in unique_candles:
                if self._candles_overlap(candle, existing):
                    # Keep the one with higher confidence
                    if candle['confidence'] > existing['confidence']:
                        unique_candles.remove(existing)
                        unique_candles.append(candle)
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_candles.append(candle)
        
        # Sort by x position (chronological order)
        unique_candles.sort(key=lambda c: c['center_x'])
        
        # Return last 10 candles maximum for analysis
        return unique_candles[-10:] if len(unique_candles) > 10 else unique_candles
    
    def _candles_overlap(self, candle1: Dict, candle2: Dict, threshold: float = 0.5) -> bool:
        """Check if two candles overlap significantly"""
        x1_start, x1_end = candle1['x'], candle1['x'] + candle1['width']
        x2_start, x2_end = candle2['x'], candle2['x'] + candle2['width']
        
        y1_start, y1_end = candle1['y'], candle1['y'] + candle1['height']
        y2_start, y2_end = candle2['y'], candle2['y'] + candle2['height']
        
        # Calculate overlap
        x_overlap = max(0, min(x1_end, x2_end) - max(x1_start, x2_start))
        y_overlap = max(0, min(y1_end, y2_end) - max(y1_start, y2_start))
        
        overlap_area = x_overlap * y_overlap
        min_area = min(candle1['area'], candle2['area'])
        
        return overlap_area > min_area * threshold