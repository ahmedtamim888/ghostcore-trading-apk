import os
import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from PIL import Image
import imutils
from datetime import datetime
import json
import base64
from io import BytesIO

try:
    import pytz
except ImportError:
    pytz = None

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATIC_FOLDER'] = 'static'

# Create directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['STATIC_FOLDER'], exist_ok=True)

class GhostCoreAI:
    def __init__(self):
        self.name = "GHOST CORE AI v.UM.100"
        self.version = "Multiversal Precision Prediction Bot"
        
    def analyze_chart(self, image_path):
        """Main analysis function for chart screenshot"""
        try:
            # Load and preprocess image
            image = cv2.imread(image_path)
            if image is None:
                return {"error": "Could not load image"}
            
            # Get chart analysis
            candles = self.detect_candles(image)
            prediction = self.generate_prediction(candles, image)
            debug_image = self.create_debug_overlay(image, candles, prediction)
            
            # Save debug image
            debug_path = os.path.join(app.config['STATIC_FOLDER'], 'debug_analysis.png')
            cv2.imwrite(debug_path, debug_image)
            
            return prediction
            
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def detect_candles(self, image):
        """Detect candlesticks using OpenCV without OCR"""
        try:
            height, width = image.shape[:2]
            
            # Preprocess image to improve detection
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(image, (3, 3), 0)
            
            # Convert to HSV for better color detection
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            
            # Enhance saturation and value channels
            hsv[:,:,1] = cv2.multiply(hsv[:,:,1], 1.2)  # Increase saturation
            hsv[:,:,2] = cv2.multiply(hsv[:,:,2], 1.1)  # Increase brightness
            
        except Exception as e:
            print(f"Error in color conversion: {e}")
            return []
        
        # Define more precise color ranges for green and red candles
        # Green candles - more restrictive range
        green_lower = np.array([45, 80, 80])
        green_upper = np.array([75, 255, 255])
        
        # Red candles - more restrictive range to avoid false positives
        red_lower1 = np.array([0, 80, 80])
        red_upper1 = np.array([8, 255, 255])
        red_lower2 = np.array([172, 80, 80])
        red_upper2 = np.array([180, 255, 255])
        
        # Create masks
        green_mask = cv2.inRange(hsv, green_lower, green_upper)
        red_mask1 = cv2.inRange(hsv, red_lower1, red_upper1)
        red_mask2 = cv2.inRange(hsv, red_lower2, red_upper2)
        red_mask = cv2.bitwise_or(red_mask1, red_mask2)
        
        # Enhanced morphological operations to clean up
        # Use different kernel sizes for better cleaning
        kernel_small = np.ones((2,2), np.uint8)
        kernel_medium = np.ones((3,3), np.uint8)
        
        # Remove small noise first
        green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel_small)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel_small)
        
        # Fill gaps in candle bodies
        green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, kernel_medium)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel_medium)
        
        # Remove very thin horizontal lines that might be grid lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 1))
        green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, horizontal_kernel)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, horizontal_kernel)
        
        # Find contours
        try:
            green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        except Exception as e:
            print(f"Error finding contours: {e}")
            return []
        
        candles = []
        
        # Process green candles with enhanced validation
        for contour in green_contours:
            area = cv2.contourArea(contour)
            if area > 100:  # Increased threshold to filter more noise
                x, y, w, h = cv2.boundingRect(contour)
                if self.is_valid_candle(w, h, height, area):
                    # Additional validation: check if it's a solid rectangular shape
                    aspect_ratio = h / w if w > 0 else 0
                    if aspect_ratio >= 1.5:  # Candles should be taller than wide
                        candles.append({
                            'type': 'bullish',
                            'x': x, 'y': y, 'width': w, 'height': h,
                            'center_x': x + w//2,
                            'body_ratio': w/h if h > 0 else 0,
                            'area': area,
                            'aspect_ratio': aspect_ratio
                        })
        
        # Process red candles with enhanced validation
        for contour in red_contours:
            area = cv2.contourArea(contour)
            if area > 100:  # Increased threshold to filter more noise
                x, y, w, h = cv2.boundingRect(contour)
                if self.is_valid_candle(w, h, height, area):
                    # Additional validation: check if it's a solid rectangular shape
                    aspect_ratio = h / w if w > 0 else 0
                    if aspect_ratio >= 1.5:  # Candles should be taller than wide
                        candles.append({
                            'type': 'bearish',
                            'x': x, 'y': y, 'width': w, 'height': h,
                            'center_x': x + w//2,
                            'body_ratio': w/h if h > 0 else 0,
                            'area': area,
                            'aspect_ratio': aspect_ratio
                        })
        
        # Sort candles by x position (time order)
        candles.sort(key=lambda c: c['center_x'])
        
        return candles[-8:] if len(candles) > 8 else candles  # Last 8 candles max
    
    def is_valid_candle(self, width, height, image_height, area):
        """Filter valid candle shapes with enhanced criteria"""
        # Basic geometry filters
        if height < 8 or width < 3:  # Minimum size requirements
            return False
        if height > image_height * 0.6:  # Too tall (reduced from 0.8)
            return False
        if width > height:  # Width should never exceed height for candles
            return False
        if area < width * height * 0.6:  # Area should be substantial relative to bounding box
            return False
        
        # Additional shape validation
        aspect_ratio = height / width if width > 0 else 0
        if aspect_ratio < 1.5 or aspect_ratio > 20:  # Reasonable aspect ratio range
            return False
            
        return True
    
    def generate_prediction(self, candles, image):
        """Generate trading signal based on candle analysis"""
        # Need at least 3 valid candles for basic analysis
        if len(candles) < 3:
            return {
                "signal": "NO SIGNAL",
                "confidence": 0,
                "reason": f"Insufficient candle data - need 3+ candles, found {len(candles)}",
                "analysis": {"candles_detected": len(candles)}
            }
        
        # Use available candles (minimum 3, maximum 8)
        recent_candles = candles[-6:] if len(candles) >= 6 else candles
        
        # Initialize analysis
        analysis = {
            "trend": "Unknown",
            "pattern": "None", 
            "momentum": "Neutral",
            "support_resistance": "None",
            "signal_strength": 0
        }
        
        signal_strength = 0
        
        # 1. Pattern Detection (flexible scoring)
        pattern_result = self.detect_patterns(recent_candles)
        analysis['pattern'] = pattern_result['pattern']
        signal_strength += pattern_result['score']
        
        # 2. Momentum Analysis
        momentum_result = self.analyze_momentum(recent_candles)
        analysis['momentum'] = momentum_result['momentum']
        signal_strength += momentum_result['score']
        
        # 3. Trend Analysis
        trend_result = self.analyze_trend(recent_candles)
        analysis['trend'] = trend_result['trend']
        signal_strength += trend_result['score']
        
        # 4. Support/Resistance
        sr_result = self.analyze_support_resistance(recent_candles)
        analysis['support_resistance'] = sr_result['level']
        signal_strength += sr_result['score']
        
        # 5. Quality bonus
        quality_bonus = self.calculate_quality_bonus(recent_candles)
        signal_strength += quality_bonus
        
        # Calculate confidence (0-100%)
        max_possible_score = 80  # Realistic maximum
        confidence = min((signal_strength / max_possible_score) * 100, 100)
        
        # Determine signal based on analysis
        signal = self.determine_signal(recent_candles, analysis, confidence)
        
        # Get current Bangladesh time
        if pytz:
            bd_tz = pytz.timezone('Asia/Dhaka')
            current_time = datetime.now(bd_tz)
        else:
            current_time = datetime.now()
        
        return {
            "signal": signal,
            "confidence": round(confidence, 1),
            "timeframe": "1 Minute",
            "local_time": current_time.strftime("%H:%M (UTC+6)"),
            "trend": analysis['trend'],
            "pattern": analysis['pattern'],
            "momentum": analysis['momentum'],
            "support_resistance": analysis['support_resistance'],
            "candle_count": len(recent_candles),
            "signal_strength": round(signal_strength, 1),
            "analysis": analysis
        }
    
    def detect_reversal_patterns(self, candles):
        """Detect reversal patterns with enhanced accuracy"""
        if len(candles) < 2:
            return {"score": 0, "pattern": "None"}
        
        last_candle = candles[-1]
        prev_candle = candles[-2]
        
        # Enhanced Engulfing Pattern Detection
        if (last_candle['type'] != prev_candle['type'] and 
            last_candle['height'] > prev_candle['height'] * 1.4 and  # Stricter size requirement
            last_candle['area'] > prev_candle['area'] * 1.3):  # Volume confirmation
            
            # Additional validation: check position overlap
            prev_top = prev_candle['y']
            prev_bottom = prev_candle['y'] + prev_candle['height']
            last_top = last_candle['y']
            last_bottom = last_candle['y'] + last_candle['height']
            
            # True engulfing: last candle should engulf previous candle
            if last_top <= prev_top and last_bottom >= prev_bottom:
                pattern_name = f"{last_candle['type'].title()} Engulfing"
                return {"score": 30, "pattern": pattern_name}
        
        # Enhanced Pin Bar Detection
        if (last_candle['body_ratio'] < 0.25 and  # Stricter body ratio
            last_candle['height'] > 20):  # Minimum height requirement
            
            # Check if it's at a significant level (compare with previous candles)
            if len(candles) >= 3:
                prev_avg_height = sum(c['height'] for c in candles[-3:-1]) / 2
                if last_candle['height'] > prev_avg_height * 1.2:  # Stands out
                    pattern_name = f"{last_candle['type'].title()} Pin Bar"
                    return {"score": 25, "pattern": pattern_name}
        
        # Enhanced Doji Detection
        if (last_candle['body_ratio'] < 0.15 and 
            last_candle['height'] > 15):  # Must have meaningful size
            return {"score": 18, "pattern": "Doji"}
        
        return {"score": 0, "pattern": "None"}
    
    def analyze_color_momentum(self, candles):
        """Analyze momentum based on candle colors"""
        if len(candles) < 3:
            return {"score": 0, "momentum": "Neutral"}
        
        bullish_count = sum(1 for c in candles if c['type'] == 'bullish')
        bearish_count = len(candles) - bullish_count
        
        # Strong momentum
        if bullish_count >= len(candles) * 0.7:
            return {"score": 18, "momentum": "Strong Bullish"}
        elif bearish_count >= len(candles) * 0.7:
            return {"score": 18, "momentum": "Strong Bearish"}
        
        # Recent momentum change
        recent_3 = candles[-3:]
        recent_bullish = sum(1 for c in recent_3 if c['type'] == 'bullish')
        
        if recent_bullish >= 2:
            return {"score": 12, "momentum": "Bullish Shift"}
        elif recent_bullish <= 1:
            return {"score": 12, "momentum": "Bearish Shift"}
        
        return {"score": 5, "momentum": "Neutral"}
    
    def analyze_trend_pattern(self, candles):
        """Analyze trend patterns (Higher Highs/Lows, Lower Highs/Lows)"""
        if len(candles) < 3:
            return {"score": 0, "trend": "Unknown"}
        
        # Simple trend analysis based on y positions
        highs = [c['y'] for c in candles]  # y increases downward in image
        lows = [c['y'] + c['height'] for c in candles]
        
        # Check for trend
        if len(highs) >= 3:
            recent_highs = highs[-3:]
            recent_lows = lows[-3:]
            
            # Downtrend (lower highs, lower lows)
            if (recent_highs[0] < recent_highs[1] < recent_highs[2] and
                recent_lows[0] < recent_lows[1] < recent_lows[2]):
                return {"score": 15, "trend": "Strong Downtrend"}
            
            # Uptrend (higher highs, higher lows)
            if (recent_highs[0] > recent_highs[1] > recent_highs[2] and
                recent_lows[0] > recent_lows[1] > recent_lows[2]):
                return {"score": 15, "trend": "Strong Uptrend"}
        
        return {"score": 8, "trend": "Sideways"}
    
    def analyze_support_resistance(self, candles):
        """Basic support/resistance analysis"""
        if len(candles) < 4:
            return {"score": 0, "level": "None"}
        
        # Look for similar price levels (y positions)
        y_positions = [c['y'] + c['height']//2 for c in candles]
        
        # Check for clustering around similar levels
        for i in range(len(y_positions)-1):
            matches = sum(1 for y in y_positions if abs(y - y_positions[i]) < 10)
            if matches >= 3:
                return {"score": 15, "level": "Key Level Touch"}
        
        return {"score": 5, "level": "Minor Level"}
    
    def noise_filter(self, candles):
        """Filter out false signals"""
        if len(candles) < 2:
            return 0
        
        # Check for very small candles (likely noise)
        small_candles = sum(1 for c in candles if c['height'] < 15)
        if small_candles > len(candles) * 0.5:
            return -5  # Penalty for too much noise
        
        return 8  # Clean candles bonus
    
    def validate_candle_quality(self, candles):
        """Validate that detected candles are reasonable"""
        if len(candles) < 2:
            return False
        
        # Check candle size consistency
        heights = [c['height'] for c in candles]
        avg_height = sum(heights) / len(heights)
        
        # Reject if candles are too small (likely noise)
        if avg_height < 12:  # More lenient
            return False
        
        # Validate candle spacing if we have enough candles
        if len(candles) >= 3:
            x_positions = [c['center_x'] for c in candles]
            spacings = [x_positions[i+1] - x_positions[i] for i in range(len(x_positions)-1)]
            avg_spacing = sum(spacings) / len(spacings)
            
            # Check if spacings are reasonable (more lenient)
            if avg_spacing < 5 or avg_spacing > 300:
                return False
        
        return True
    
    def detect_patterns(self, candles):
        """Detect trading patterns with realistic scoring"""
        if len(candles) < 2:
            return {"score": 0, "pattern": "None"}
        
        last_candle = candles[-1]
        prev_candle = candles[-2]
        
        # Engulfing Pattern (relaxed criteria)
        if (last_candle['type'] != prev_candle['type'] and 
            last_candle['height'] > prev_candle['height'] * 1.2):
            
            prev_top = prev_candle['y']
            prev_bottom = prev_candle['y'] + prev_candle['height']
            last_top = last_candle['y']
            last_bottom = last_candle['y'] + last_candle['height']
            
            # Check for engulfing (some overlap allowed)
            if (last_top <= prev_top + 5 and last_bottom >= prev_bottom - 5):
                pattern_name = f"{last_candle['type'].title()} Engulfing"
                return {"score": 25, "pattern": pattern_name}
        
        # Pin Bar Pattern
        if last_candle['body_ratio'] < 0.3 and last_candle['height'] > 15:
            pattern_name = f"{last_candle['type'].title()} Pin Bar"
            return {"score": 20, "pattern": pattern_name}
        
        # Doji Pattern
        if last_candle['body_ratio'] < 0.2:
            return {"score": 15, "pattern": "Doji"}
        
        # Consecutive candles (momentum)
        if len(candles) >= 3:
            last_3 = candles[-3:]
            same_type_count = sum(1 for c in last_3 if c['type'] == last_candle['type'])
            
            if same_type_count >= 2:
                pattern_name = f"{last_candle['type'].title()} Momentum"
                return {"score": 18, "pattern": pattern_name}
        
        # Large candle (breakout potential)
        if len(candles) >= 3:
            avg_height = sum(c['height'] for c in candles[-3:-1]) / 2
            if last_candle['height'] > avg_height * 1.4:
                pattern_name = f"Large {last_candle['type'].title()} Candle"
                return {"score": 15, "pattern": pattern_name}
        
        # Small pattern (consolidation)
        return {"score": 8, "pattern": "Standard Candle"}
    
    def analyze_momentum(self, candles):
        """Analyze momentum with flexible scoring"""
        if len(candles) < 3:
            return {"score": 5, "momentum": "Limited Data"}
        
        # Count candle types in available data
        bullish_count = sum(1 for c in candles if c['type'] == 'bullish')
        bearish_count = len(candles) - bullish_count
        
        # Strong momentum (70%+ same direction)
        if bullish_count >= len(candles) * 0.7:
            return {"score": 20, "momentum": "Strong Bullish"}
        elif bearish_count >= len(candles) * 0.7:
            return {"score": 20, "momentum": "Strong Bearish"}
        
        # Moderate momentum (60%+ same direction)
        if bullish_count >= len(candles) * 0.6:
            return {"score": 15, "momentum": "Bullish"}
        elif bearish_count >= len(candles) * 0.6:
            return {"score": 15, "momentum": "Bearish"}
        
        # Recent momentum (last 3 candles)
        if len(candles) >= 3:
            recent_3 = candles[-3:]
            recent_bullish = sum(1 for c in recent_3 if c['type'] == 'bullish')
            
            if recent_bullish >= 2:
                return {"score": 12, "momentum": "Recent Bullish"}
            elif recent_bullish <= 1:
                return {"score": 12, "momentum": "Recent Bearish"}
        
        return {"score": 8, "momentum": "Neutral"}
    
    def analyze_trend(self, candles):
        """Analyze trend with flexible criteria"""
        if len(candles) < 3:
            return {"score": 5, "trend": "Limited Data"}
        
        # Use candle positions for trend analysis
        positions = [c['y'] + c['height']//2 for c in candles]
        
        if len(positions) >= 3:
            # Compare first and last thirds
            first_third = positions[:len(positions)//3] if len(positions) >= 3 else [positions[0]]
            last_third = positions[-len(positions)//3:] if len(positions) >= 3 else [positions[-1]]
            
            avg_first = sum(first_third) / len(first_third)
            avg_last = sum(last_third) / len(last_third)
            
            diff = avg_last - avg_first
            
            # Trend detection (more lenient)
            if diff > 8:
                return {"score": 15, "trend": "Downtrend"}
            elif diff < -8:
                return {"score": 15, "trend": "Uptrend"}
            else:
                return {"score": 10, "trend": "Sideways"}
        
        return {"score": 8, "trend": "Neutral"}
    
    def calculate_quality_bonus(self, candles):
        """Calculate bonus points for candle quality"""
        if len(candles) < 2:
            return 0
        
        # Size consistency bonus
        heights = [c['height'] for c in candles]
        avg_height = sum(heights) / len(heights)
        
        if avg_height > 20:  # Good sized candles
            return 5
        elif avg_height > 15:  # Decent sized candles
            return 3
        
        return 0
    
    def determine_signal(self, candles, analysis, confidence):
        """Determine final signal based on analysis"""
        # Minimum confidence threshold
        if confidence < 45:
            return "NO SIGNAL"
        
        last_candle = candles[-1]
        
        # Priority 1: Strong patterns
        if "Engulfing" in analysis['pattern']:
            if "Bullish" in analysis['pattern']:
                return "CALL"
            elif "Bearish" in analysis['pattern']:
                return "PUT"
        
        # Priority 2: Pin bars (reversal signals)
        if "Pin Bar" in analysis['pattern']:
            if "Bullish" in analysis['pattern']:
                return "CALL"
            elif "Bearish" in analysis['pattern']:
                return "PUT"
        
        # Priority 3: Momentum signals
        if confidence >= 60:
            if "Bullish" in analysis['momentum']:
                return "CALL" 
            elif "Bearish" in analysis['momentum']:
                return "PUT"
        
        # Priority 4: Last candle direction (if confidence is decent)
        if confidence >= 55:
            if last_candle['type'] == 'bullish':
                return "CALL"
            elif last_candle['type'] == 'bearish':
                return "PUT"
        
        return "NO SIGNAL"
    
    
    
    def create_debug_overlay(self, image, candles, prediction):
        """Create debug overlay image with analysis"""
        debug_img = image.copy()
        
        # Draw detected candles
        for i, candle in enumerate(candles):
            color = (0, 255, 0) if candle['type'] == 'bullish' else (0, 0, 255)
            cv2.rectangle(debug_img, 
                         (candle['x'], candle['y']), 
                         (candle['x'] + candle['width'], candle['y'] + candle['height']), 
                         color, 2)
            
            # Add candle number
            cv2.putText(debug_img, str(i+1), 
                       (candle['x'], candle['y']-5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        # Add prediction text
        signal_color = (0, 255, 255) if prediction['signal'] == 'CALL' else (255, 0, 255)
        if prediction['signal'] == 'NO SIGNAL':
            signal_color = (128, 128, 128)
            
        cv2.putText(debug_img, f"Signal: {prediction['signal']}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, signal_color, 2)
        cv2.putText(debug_img, f"Confidence: {prediction['confidence']}%", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return debug_img

# Initialize AI
ghost_ai = GhostCoreAI()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_chart():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'})
        
        # Check file type
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            return jsonify({'error': 'Unsupported file format. Please use PNG, JPG, or other image formats.'})
        
        if file:
            # Secure filename and save
            filename = secure_filename(file.filename)
            if not filename:
                filename = 'chart_image.png'
            
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                # Analyze the chart
                result = ghost_ai.analyze_chart(filepath)
                
                # Clean up uploaded file
                if os.path.exists(filepath):
                    os.remove(filepath)
                
                return jsonify(result)
                
            except Exception as e:
                # Clean up on error
                if os.path.exists(filepath):
                    os.remove(filepath)
                return jsonify({'error': f'Analysis failed: {str(e)}'})
    
    except Exception as e:
        return jsonify({'error': f'Request processing failed: {str(e)}'})

@app.route('/debug-image')
def get_debug_image():
    debug_path = os.path.join(app.config['STATIC_FOLDER'], 'debug_analysis.png')
    if os.path.exists(debug_path):
        return send_file(debug_path, mimetype='image/png')
    return jsonify({'error': 'No debug image available'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
