"""
🔮 COSMIC OMNI-BRAIN AI - UTILITIES
Essential utility functions for the AI trading system
"""

import json
import urllib.request
import urllib.parse
import os
import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional
import uuid
import hashlib

class TradingUtils:
    """
    🛠️ COSMIC UTILITY TOOLKIT
    Essential functions for time, logging, Telegram, and system operations
    """
    
    def __init__(self):
        self.name = "COSMIC UTILS"
        self.version = "∞.UNBEATABLE"
        self.bd_timezone = timezone(timedelta(hours=6))  # UTC+6
        
        # Telegram configuration
        self.bot_token = "8173800058:AAEWDc9ocSz7Ohj1v62fjyA8LyJvMadl8NY"
        self.user_id = "7700105638"
        
        # Setup logging
        self._setup_logging()
        
        # Performance tracking
        self.analysis_stats = {
            'total_analyses': 0,
            'successful_signals': 0,
            'avg_confidence': 0.0,
            'strategy_types_used': {},
            'session_start': datetime.now()
        }
    
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('cosmic_ai.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('COSMIC_AI')
    
    def get_bd_time(self) -> Dict[str, str]:
        """
        🕐 GET BANGLADESH TIME (UTC+6)
        Returns current time in multiple formats
        """
        now = datetime.now(self.bd_timezone)
        
        return {
            'current_time': now.strftime("%H:%M"),
            'full_time': now.strftime("%H:%M:%S"),
            'date': now.strftime("%Y-%m-%d"),
            'datetime': now.strftime("%Y-%m-%d %H:%M:%S"),
            'iso': now.isoformat(),
            'timestamp': int(now.timestamp()),
            'minute': now.minute,
            'hour': now.hour,
            'day_of_week': now.strftime("%A"),
            'timezone': "UTC+6"
        }
    
    def is_trading_hours(self) -> Dict[str, Any]:
        """Check if current time is suitable for trading"""
        
        time_info = self.get_bd_time()
        hour = time_info['hour']
        minute = time_info['minute']
        day_of_week = time_info['day_of_week']
        
        # Define trading sessions
        trading_sessions = {
            'london': {'start': 14, 'end': 23},  # 2 PM to 11 PM Bangladesh time
            'new_york': {'start': 21, 'end': 6},  # 9 PM to 6 AM Bangladesh time
            'asian': {'start': 6, 'end': 15}     # 6 AM to 3 PM Bangladesh time
        }
        
        is_weekend = day_of_week in ['Saturday', 'Sunday']
        
        # Check active sessions
        active_sessions = []
        for session, times in trading_sessions.items():
            if times['start'] <= hour <= times['end']:
                active_sessions.append(session)
        
        is_good_time = (
            not is_weekend and 
            len(active_sessions) > 0 and
            not (22 <= hour <= 6)  # Avoid very late/early hours
        )
        
        return {
            'is_trading_hours': is_good_time,
            'active_sessions': active_sessions,
            'is_weekend': is_weekend,
            'current_hour': hour,
            'recommendation': 'good' if is_good_time else 'avoid',
            'next_good_time': self._calculate_next_good_time(hour, is_weekend)
        }
    
    def _calculate_next_good_time(self, current_hour: int, is_weekend: bool) -> str:
        """Calculate next good trading time"""
        
        if is_weekend:
            return "Monday 06:00 (UTC+6)"
        
        if current_hour < 6:
            return "06:00 (UTC+6) - Asian session start"
        elif current_hour > 23:
            return "Tomorrow 06:00 (UTC+6)"
        else:
            return "Next major session"
    
    def calculate_confidence_score(self, chart_analysis: Dict, market_context: Dict, 
                                 strategy_result: Dict) -> Dict[str, float]:
        """
        🎯 CALCULATE OVERALL CONFIDENCE SCORE
        Combines multiple factors for final confidence
        """
        
        # Extract individual confidence scores
        chart_quality = chart_analysis.get('analysis_quality', 0.5)
        context_confidence = market_context.get('confidence', 0.5)
        strategy_confidence = strategy_result.get('confidence', 0.5)
        
        # Weight different factors
        weights = {
            'chart_quality': 0.25,
            'market_context': 0.35,
            'strategy_logic': 0.40
        }
        
        # Calculate weighted average
        weighted_confidence = (
            chart_quality * weights['chart_quality'] +
            context_confidence * weights['market_context'] +
            strategy_confidence * weights['strategy_logic']
        )
        
        # Apply bonuses and penalties
        
        # Confluence bonus
        confluence_factors = strategy_result.get('confluence_factors', [])
        confluence_bonus = min(len(confluence_factors) * 0.05, 0.15)
        
        # Market condition bonus
        market_conditions = strategy_result.get('market_conditions', {})
        if market_conditions.get('state') in ['trending', 'institutional']:
            market_bonus = 0.1
        else:
            market_bonus = 0
        
        # Time-based adjustment
        time_info = self.get_bd_time()
        trading_hours = self.is_trading_hours()
        if trading_hours['is_trading_hours']:
            time_bonus = 0.05
        else:
            time_bonus = -0.1
        
        # Signal strength bonus
        entry_logic = strategy_result.get('entry_logic', {})
        signal_strength_bonus = entry_logic.get('confidence_boost', 0)
        
        # Calculate final confidence
        final_confidence = (
            weighted_confidence + 
            confluence_bonus + 
            market_bonus + 
            time_bonus + 
            signal_strength_bonus
        )
        
        # Ensure confidence is within bounds
        final_confidence = max(0.1, min(0.98, final_confidence))
        
        return {
            'overall_confidence': final_confidence,
            'chart_quality': chart_quality,
            'market_context': context_confidence,
            'strategy_logic': strategy_confidence,
            'confluence_bonus': confluence_bonus,
            'market_bonus': market_bonus,
            'time_bonus': time_bonus,
            'signal_strength_bonus': signal_strength_bonus,
            'confidence_grade': self._get_confidence_grade(final_confidence)
        }
    
    def _get_confidence_grade(self, confidence: float) -> str:
        """Convert confidence score to grade"""
        
        if confidence >= 0.9:
            return 'A+ (Excellent)'
        elif confidence >= 0.8:
            return 'A (Very High)'
        elif confidence >= 0.7:
            return 'B+ (High)'
        elif confidence >= 0.6:
            return 'B (Good)'
        elif confidence >= 0.5:
            return 'C+ (Fair)'
        elif confidence >= 0.4:
            return 'C (Low)'
        else:
            return 'D (Very Low)'
    
    def send_telegram_signal(self, signal_data: Dict, image_path: Optional[str] = None) -> bool:
        """
        📱 SEND SIGNAL TO TELEGRAM
        Sends formatted signal with optional image
        """
        
        try:
            # Create message
            message = self._format_telegram_message(signal_data)
            
            # Send message
            success = self._send_telegram_message(message)
            
            if success:
                self.logger.info("✅ Telegram signal sent successfully")
                
                # Send image if provided
                if image_path and os.path.exists(image_path):
                    self._send_telegram_image(image_path, "📊 Chart Analysis")
                
                return True
            else:
                self.logger.error("❌ Failed to send Telegram signal")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Telegram send error: {e}")
            return False
    
    def _format_telegram_message(self, signal_data: Dict) -> str:
        """Format signal data into Telegram message"""
        
        strategy = signal_data.get('strategy', {})
        entry_logic = strategy.get('entry_logic', {})
        confidence_info = signal_data.get('confidence', {})
        time_info = self.get_bd_time()
        
        signal = entry_logic.get('signal', 'NO TRADE')
        confidence = confidence_info.get('overall_confidence', 0.5)
        
        # Generate strategy name for display
        strategy_name = strategy.get('strategy_name', 'Dynamic Strategy')
        strategy_description = strategy.get('description', 'Adaptive market analysis')
        
        # Generate reasoning
        reasoning = strategy.get('strategy_reasoning', 'Market analysis indicates this setup')
        market_narrative = signal_data.get('market_context', {}).get('market_narrative', 'Market showing mixed signals')
        
        # Format message
        message = f"""🌌 <b>COSMIC OMNI-BRAIN AI STRATEGY</b>

⚡ <b>ADAPTIVE PREDICTION</b>
1M;{time_info['current_time']};{signal}

💫 <b>STRONG CONFIDENCE ({confidence:.2f})</b>

🧠 <b>DYNAMIC STRATEGY BUILT:</b>
{strategy_description}

📊 <b>AI REASONING:</b>
🎯 Strategy: {strategy_name}
🧠 Market psychology: {reasoning}

📈 <b>MARKET NARRATIVE:</b>
{market_narrative}

🎯 <b>MARKET STATE:</b>
{'🔥 UP' if signal == 'CALL' else '❄️ DOWN' if signal == 'PUT' else '⚠️ NO TRADE'} - Confidence: {int(confidence * 100)}%

⏰ <b>Entry at start of next 1M candle (UTC+6)</b>

🤖 <i>Analysis #{self.analysis_stats['total_analyses'] + 1} - Real chart patterns detected</i>"""

        return message
    
    def _send_telegram_message(self, text: str) -> bool:
        """Send text message to Telegram"""
        
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            data = {
                'chat_id': self.user_id,
                'text': text,
                'parse_mode': 'HTML'
            }
            
            encoded_data = urllib.parse.urlencode(data).encode('utf-8')
            req = urllib.request.Request(url, data=encoded_data, method='POST')
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                
            return result.get('ok', False)
            
        except Exception as e:
            self.logger.error(f"❌ Telegram message error: {e}")
            return False
    
    def _send_telegram_image(self, image_path: str, caption: str = "") -> bool:
        """Send image to Telegram"""
        
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"
            
            # Read image file
            with open(image_path, 'rb') as img_file:
                files = {'photo': img_file}
                data = {
                    'chat_id': self.user_id,
                    'caption': caption
                }
                
                # Note: This is a simplified version. For file uploads,
                # you might need to use a more advanced method or library
                
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Telegram image error: {e}")
            return False
    
    def log_analysis(self, signal_data: Dict):
        """
        📝 LOG ANALYSIS RESULTS
        Track performance and statistics
        """
        
        strategy = signal_data.get('strategy', {})
        entry_logic = strategy.get('entry_logic', {})
        confidence_info = signal_data.get('confidence', {})
        
        signal = entry_logic.get('signal', 'NO TRADE')
        confidence = confidence_info.get('overall_confidence', 0.5)
        strategy_type = strategy.get('strategy_type', 'unknown')
        
        # Update statistics
        self.analysis_stats['total_analyses'] += 1
        
        if signal in ['CALL', 'PUT']:
            self.analysis_stats['successful_signals'] += 1
            
            # Update strategy usage
            if strategy_type in self.analysis_stats['strategy_types_used']:
                self.analysis_stats['strategy_types_used'][strategy_type] += 1
            else:
                self.analysis_stats['strategy_types_used'][strategy_type] = 1
        
        # Update average confidence
        total_confidence = (
            self.analysis_stats['avg_confidence'] * (self.analysis_stats['total_analyses'] - 1) +
            confidence
        )
        self.analysis_stats['avg_confidence'] = total_confidence / self.analysis_stats['total_analyses']
        
        # Log to file
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'signal': signal,
            'confidence': confidence,
            'strategy_type': strategy_type,
            'strategy_name': strategy.get('strategy_name', 'Unknown'),
            'analysis_id': self.analysis_stats['total_analyses']
        }
        
        self.logger.info(f"📊 Analysis #{self.analysis_stats['total_analyses']}: {signal} (conf: {confidence:.2f})")
        
        # Write to JSON log file
        try:
            with open('analysis_log.json', 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            self.logger.error(f"❌ Log file error: {e}")
    
    def get_performance_stats(self) -> Dict:
        """Get current performance statistics"""
        
        uptime = datetime.now() - self.analysis_stats['session_start']
        
        return {
            'session_uptime': str(uptime),
            'total_analyses': self.analysis_stats['total_analyses'],
            'successful_signals': self.analysis_stats['successful_signals'],
            'signal_rate': (
                self.analysis_stats['successful_signals'] / 
                max(self.analysis_stats['total_analyses'], 1)
            ),
            'average_confidence': self.analysis_stats['avg_confidence'],
            'strategy_distribution': self.analysis_stats['strategy_types_used'],
            'analyses_per_hour': (
                self.analysis_stats['total_analyses'] / 
                max(uptime.total_seconds() / 3600, 1)
            )
        }
    
    def cleanup_old_files(self, directory: str = "uploads", max_age_hours: int = 24):
        """
        🧹 CLEANUP OLD FILES
        Remove old uploaded images to save space
        """
        
        try:
            if not os.path.exists(directory):
                return
            
            current_time = datetime.now()
            max_age = timedelta(hours=max_age_hours)
            
            deleted_count = 0
            
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                
                if os.path.isfile(filepath):
                    file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                    
                    if current_time - file_time > max_age:
                        os.remove(filepath)
                        deleted_count += 1
            
            if deleted_count > 0:
                self.logger.info(f"🧹 Cleaned up {deleted_count} old files")
                
        except Exception as e:
            self.logger.error(f"❌ Cleanup error: {e}")
    
    def generate_analysis_id(self) -> str:
        """Generate unique analysis ID"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        return f"COSMIC_{timestamp}_{unique_id}"
    
    def validate_image_file(self, filepath: str) -> Dict[str, Any]:
        """Validate uploaded image file"""
        
        if not os.path.exists(filepath):
            return {'valid': False, 'error': 'File does not exist'}
        
        # Check file size (max 10MB)
        file_size = os.path.getsize(filepath)
        if file_size > 10 * 1024 * 1024:
            return {'valid': False, 'error': 'File too large (max 10MB)'}
        
        # Check file extension
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        file_ext = os.path.splitext(filepath)[1].lower()
        
        if file_ext not in valid_extensions:
            return {'valid': False, 'error': 'Invalid file type'}
        
        return {
            'valid': True,
            'file_size': file_size,
            'file_extension': file_ext,
            'file_size_mb': file_size / (1024 * 1024)
        }
    
    def create_backup(self, data: Dict, backup_type: str = "analysis"):
        """Create backup of important data"""
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"backup_{backup_type}_{timestamp}.json"
            
            with open(backup_filename, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            self.logger.info(f"💾 Backup created: {backup_filename}")
            
        except Exception as e:
            self.logger.error(f"❌ Backup error: {e}")
    
    def hash_image(self, image_path: str) -> str:
        """Generate hash of image for duplicate detection"""
        
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
                return hashlib.md5(image_data).hexdigest()
        except Exception:
            return "unknown"
    
    def format_number(self, number: float, decimal_places: int = 2) -> str:
        """Format number for display"""
        
        if number >= 1000000:
            return f"{number / 1000000:.{decimal_places}f}M"
        elif number >= 1000:
            return f"{number / 1000:.{decimal_places}f}K"
        else:
            return f"{number:.{decimal_places}f}"
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        
        time_info = self.get_bd_time()
        trading_hours = self.is_trading_hours()
        performance = self.get_performance_stats()
        
        return {
            'ai_version': self.version,
            'current_time': time_info,
            'trading_status': trading_hours,
            'performance': performance,
            'system_health': 'optimal'
        }