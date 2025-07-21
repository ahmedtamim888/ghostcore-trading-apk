import os
import logging
import pytz
from datetime import datetime
from typing import Dict, Optional
import cv2
import numpy as np
import requests
import json

class TradingUtils:
    """Utility functions for the COSMIC OMNI-BRAIN AI trading bot"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.bd_timezone = pytz.timezone('Asia/Dhaka')  # UTC+6
        self.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('cosmic_omni_brain.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger('COSMIC_OMNI_BRAIN')
    
    def get_bd_time(self) -> str:
        """Get current Bangladesh time (UTC+6)"""
        try:
            bd_time = datetime.now(self.bd_timezone)
            return bd_time.strftime("%H:%M (UTC+6)")
        except Exception as e:
            self.logger.error(f"Error getting BD time: {e}")
            return datetime.now().strftime("%H:%M (Local)")
    
    def get_bd_datetime(self) -> datetime:
        """Get current Bangladesh datetime object"""
        try:
            return datetime.now(self.bd_timezone)
        except Exception as e:
            self.logger.error(f"Error getting BD datetime: {e}")
            return datetime.now()
    
    def format_signal_message(self, signal_data: Dict, image_path: Optional[str] = None) -> str:
        """Format signal for Telegram message"""
        bd_time = self.get_bd_time()
        
        # Determine signal emoji
        signal_emoji = {
            'CALL': '🔥',
            'PUT': '❄️',
            'NO SIGNAL': '⚠️'
        }.get(signal_data['signal'], '❓')
        
        # Determine confidence emoji
        confidence = signal_data.get('confidence', 0)
        if confidence >= 90:
            confidence_emoji = '🎯'
        elif confidence >= 75:
            confidence_emoji = '📈'
        elif confidence >= 60:
            confidence_emoji = '📊'
        else:
            confidence_emoji = '⚡'
        
        message = f"""🔮 COSMIC OMNI-BRAIN SIGNAL
        
🕒 1M | {bd_time}
{signal_emoji} Signal: {signal_data['signal']}
📖 Strategy: {signal_data.get('strategy', 'Unknown')}
{confidence_emoji} Confidence: {confidence}%
🧠 AI Logic: {signal_data.get('reasoning', 'No reasoning available')}
🎭 Market Mode: {signal_data.get('market_adaptation', 'Standard')}
⚖️ Risk Level: {signal_data.get('risk_level', 'Unknown').title()}

🤖 Analysis by COSMIC OMNI-BRAIN AI v∞.UNBEATABLE
"""
        
        return message.strip()
    
    def send_telegram_signal(self, signal_data: Dict, image_path: Optional[str] = None) -> bool:
        """Send signal to Telegram"""
        if not self.telegram_bot_token or not self.telegram_chat_id:
            self.logger.warning("Telegram credentials not configured")
            return False
        
        try:
            message = self.format_signal_message(signal_data, image_path)
            
            # Send text message
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            payload = {
                'chat_id': self.telegram_chat_id,
                'text': message,
                'parse_mode': 'HTML',
                'disable_web_page_preview': True
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                self.logger.info("Signal sent successfully to Telegram")
                
                # Send image if provided
                if image_path and os.path.exists(image_path):
                    self._send_telegram_image(image_path)
                
                return True
            else:
                self.logger.error(f"Failed to send Telegram message: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error sending Telegram signal: {e}")
            return False
    
    def _send_telegram_image(self, image_path: str) -> bool:
        """Send image to Telegram"""
        try:
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendPhoto"
            
            with open(image_path, 'rb') as photo:
                files = {'photo': photo}
                data = {
                    'chat_id': self.telegram_chat_id,
                    'caption': '📊 Chart Analysis'
                }
                
                response = requests.post(url, files=files, data=data, timeout=30)
                
                if response.status_code == 200:
                    self.logger.info("Image sent successfully to Telegram")
                    return True
                else:
                    self.logger.error(f"Failed to send Telegram image: {response.text}")
                    return False
                    
        except Exception as e:
            self.logger.error(f"Error sending Telegram image: {e}")
            return False
    
    def create_annotated_image(self, original_image: np.ndarray, candles: list, 
                             signal_data: Dict) -> np.ndarray:
        """Create annotated image with analysis overlays"""
        try:
            # Create a copy of the original image
            annotated = original_image.copy()
            height, width = annotated.shape[:2]
            
            # Draw detected candles
            for i, candle in enumerate(candles):
                color = (0, 255, 0) if candle['type'] == 'bullish' else (0, 0, 255)
                
                # Draw candle rectangle
                cv2.rectangle(annotated, 
                            (candle['x'], candle['y']), 
                            (candle['x'] + candle['width'], candle['y'] + candle['height']), 
                            color, 2)
                
                # Add candle number
                cv2.putText(annotated, str(i+1), 
                          (candle['x'], candle['y']-5), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
            
            # Add signal information overlay
            overlay_height = 120
            overlay = np.zeros((overlay_height, width, 3), dtype=np.uint8)
            overlay[:] = (0, 0, 0)  # Black background
            
            # Signal text
            signal = signal_data['signal']
            confidence = signal_data.get('confidence', 0)
            strategy = signal_data.get('strategy', 'Unknown')
            
            # Signal color
            signal_color = (0, 255, 255) if signal == 'CALL' else (255, 0, 255)
            if signal == 'NO SIGNAL':
                signal_color = (128, 128, 128)
            
            # Add text to overlay
            cv2.putText(overlay, f"COSMIC OMNI-BRAIN AI v∞", 
                       (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.putText(overlay, f"Signal: {signal}", 
                       (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, signal_color, 2)
            
            cv2.putText(overlay, f"Confidence: {confidence}%", 
                       (10, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            cv2.putText(overlay, f"Strategy: {strategy[:40]}", 
                       (10, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            
            cv2.putText(overlay, f"Time: {self.get_bd_time()}", 
                       (10, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1)
            
            # Combine original image with overlay
            result = np.vstack([annotated, overlay])
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error creating annotated image: {e}")
            return original_image
    
    def calculate_confidence_score(self, signal_strength: float, market_health: float, 
                                 data_quality: float) -> float:
        """Calculate overall confidence score"""
        try:
            # Weighted combination of factors
            weights = {
                'signal_strength': 0.5,
                'market_health': 0.3,
                'data_quality': 0.2
            }
            
            confidence = (
                signal_strength * weights['signal_strength'] +
                market_health * weights['market_health'] +
                data_quality * weights['data_quality']
            ) * 100
            
            return max(0.0, min(100.0, confidence))
            
        except Exception as e:
            self.logger.error(f"Error calculating confidence: {e}")
            return 50.0  # Default middle confidence
    
    def log_signal(self, signal_data: Dict, candles_count: int, processing_time: float):
        """Log signal details for analysis"""
        try:
            log_entry = {
                'timestamp': self.get_bd_datetime().isoformat(),
                'signal': signal_data['signal'],
                'confidence': signal_data.get('confidence', 0),
                'strategy': signal_data.get('strategy', 'Unknown'),
                'candles_analyzed': candles_count,
                'processing_time_ms': round(processing_time * 1000, 2),
                'market_adaptation': signal_data.get('market_adaptation', 'Standard')
            }
            
            self.logger.info(f"SIGNAL GENERATED: {json.dumps(log_entry, indent=2)}")
            
        except Exception as e:
            self.logger.error(f"Error logging signal: {e}")
    
    def cleanup_old_files(self, directory: str, max_age_hours: int = 24):
        """Clean up old files to save space"""
        try:
            import time
            import glob
            
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            
            pattern = os.path.join(directory, "*")
            files = glob.glob(pattern)
            
            deleted_count = 0
            for file_path in files:
                if os.path.isfile(file_path):
                    file_age = current_time - os.path.getmtime(file_path)
                    if file_age > max_age_seconds:
                        os.remove(file_path)
                        deleted_count += 1
            
            if deleted_count > 0:
                self.logger.info(f"Cleaned up {deleted_count} old files from {directory}")
                
        except Exception as e:
            self.logger.error(f"Error cleaning up files: {e}")
    
    def validate_image(self, image_path: str) -> bool:
        """Validate that uploaded image is suitable for analysis"""
        try:
            if not os.path.exists(image_path):
                return False
            
            # Check file size (max 16MB)
            file_size = os.path.getsize(image_path)
            if file_size > 16 * 1024 * 1024:
                self.logger.warning(f"Image too large: {file_size} bytes")
                return False
            
            # Try to load image
            image = cv2.imread(image_path)
            if image is None:
                self.logger.warning("Could not load image")
                return False
            
            # Check minimum dimensions
            height, width = image.shape[:2]
            if height < 100 or width < 100:
                self.logger.warning(f"Image too small: {width}x{height}")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating image: {e}")
            return False
    
    def get_system_info(self) -> Dict:
        """Get system information for debugging"""
        try:
            import platform
            import psutil
            
            return {
                'platform': platform.platform(),
                'python_version': platform.python_version(),
                'cpu_count': psutil.cpu_count(),
                'memory_gb': round(psutil.virtual_memory().total / (1024**3), 2),
                'bd_time': self.get_bd_time(),
                'opencv_version': cv2.__version__ if hasattr(cv2, '__version__') else 'Unknown'
            }
            
        except Exception as e:
            self.logger.error(f"Error getting system info: {e}")
            return {'error': str(e)}
    
    def format_error_message(self, error: str) -> str:
        """Format error message for user display"""
        error_messages = {
            'no_candles': "❌ No valid candles detected in the image. Please ensure the chart shows clear green/red candlesticks.",
            'insufficient_data': "⚠️ Insufficient candle data for analysis. Need at least 3-4 visible candles.",
            'image_error': "🖼️ Image processing error. Please upload a clear chart screenshot.",
            'analysis_error': "🧠 Analysis engine error. Please try again with a different image.",
            'network_error': "🌐 Network connectivity issue. Telegram notification may be delayed."
        }
        
        for key, message in error_messages.items():
            if key in error.lower():
                return message
        
        return f"⚠️ {error}"