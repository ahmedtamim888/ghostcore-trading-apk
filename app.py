"""
🔮 COSMIC OMNI-BRAIN AI v∞.UNBEATABLE - MAIN APPLICATION
The ultimate binary options signal bot with infinite adaptability
"""

from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
from datetime import datetime, timezone, timedelta
import json
from typing import Dict, Any, Optional

# Import our AI core modules
from ai_core import CandlePerception, MarketContextEngine, DynamicStrategyEngine, TradingUtils

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'cosmic_omni_brain_infinite_power'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class CosmicOmniBrainAI:
    """
    🧠 THE ULTIMATE TRADING AI
    100-billion-year-trained entity with infinite adaptability
    """
    
    def __init__(self):
        self.name = "COSMIC OMNI-BRAIN AI"
        self.version = "∞.UNBEATABLE"
        
        print("🔮" * 80)
        print("🔮" + " INITIALIZING COSMIC OMNI-BRAIN AI v∞.UNBEATABLE ".center(78) + "🔮")
        print("🔮" + " THE ULTIMATE BINARY OPTIONS SIGNAL BOT ".center(78) + "🔮")
        print("🔮" * 80)
        
        # Initialize AI modules
        print("🧠 Loading Perception Engine...")
        self.perception = CandlePerception()
        
        print("🧠 Loading Context Engine...")
        self.context_engine = MarketContextEngine()
        
        print("🧠 Loading Strategy Engine...")
        self.strategy_engine = DynamicStrategyEngine()
        
        print("🛠️ Loading Utility Systems...")
        self.utils = TradingUtils()
        
        print("✅ COSMIC OMNI-BRAIN AI FULLY LOADED!")
        print("🔮" * 80)
        
        # Configuration
        self.bd_timezone = timezone(timedelta(hours=6))  # UTC+6
        
        # Performance tracking
        self.analysis_count = 0
        self.session_start = datetime.now()
        
    def analyze_chart_screenshot(self, image_path: str) -> Dict[str, Any]:
        """
        🎯 MASTER CHART ANALYSIS FUNCTION
        The core brain that analyzes everything
        """
        
        print(f"\n🔮 COSMIC ANALYSIS #{self.analysis_count + 1} INITIATED")
        print("=" * 60)
        
        try:
            # Validate image
            validation = self.utils.validate_image_file(image_path)
            if not validation['valid']:
                return self._create_error_response(validation['error'])
            
            # Load image
            print("📸 Loading chart image...")
            image = cv2.imread(image_path)
            if image is None:
                return self._create_error_response("Failed to load image")
            
            print(f"📊 Image loaded: {image.shape[1]}x{image.shape[0]} pixels")
            
            # 1. PERCEPTION ANALYSIS
            print("\n🧠 PHASE 1: PERCEPTION ANALYSIS")
            chart_analysis = self.perception.analyze_chart_structure(image)
            
            candles_detected = len(chart_analysis.get('candles', []))
            print(f"✅ Detected {candles_detected} candlesticks")
            print(f"✅ Analysis quality: {chart_analysis.get('analysis_quality', 0):.2f}")
            
            # 2. MARKET CONTEXT ANALYSIS
            print("\n🧠 PHASE 2: MARKET CONTEXT ANALYSIS")
            market_context = self.context_engine.analyze_market_psychology(chart_analysis)
            
            sentiment = market_context.get('sentiment', {})
            print(f"✅ Market sentiment: {sentiment.get('label', 'unknown')}")
            print(f"✅ Context confidence: {market_context.get('confidence', 0):.2f}")
            
            # 3. DYNAMIC STRATEGY GENERATION
            print("\n🧠 PHASE 3: DYNAMIC STRATEGY GENERATION")
            strategy_result = self.strategy_engine.generate_dynamic_strategy(chart_analysis, market_context)
            
            strategy_name = strategy_result.get('strategy_name', 'Unknown')
            print(f"✅ Strategy generated: {strategy_name}")
            print(f"✅ Strategy confidence: {strategy_result.get('confidence', 0):.2f}")
            
            # 4. CONFIDENCE CALCULATION
            print("\n🧠 PHASE 4: CONFIDENCE CALCULATION")
            confidence_analysis = self.utils.calculate_confidence_score(
                chart_analysis, market_context, strategy_result
            )
            
            overall_confidence = confidence_analysis.get('overall_confidence', 0)
            confidence_grade = confidence_analysis.get('confidence_grade', 'Unknown')
            print(f"✅ Overall confidence: {overall_confidence:.2f} ({confidence_grade})")
            
            # 5. SIGNAL GENERATION
            print("\n🧠 PHASE 5: SIGNAL GENERATION")
            entry_logic = strategy_result.get('entry_logic', {})
            signal = entry_logic.get('signal', 'NO TRADE')
            signal_reason = entry_logic.get('reason', 'Unknown reason')
            
            print(f"✅ Generated signal: {signal}")
            print(f"✅ Signal reason: {signal_reason}")
            
            # 6. COMPREHENSIVE RESULT COMPILATION
            print("\n🧠 PHASE 6: RESULT COMPILATION")
            
            # Get current time
            time_info = self.utils.get_bd_time()
            
            # Compile complete analysis result
            analysis_result = {
                'analysis_id': self.utils.generate_analysis_id(),
                'timestamp': time_info['iso'],
                'current_time': time_info['current_time'],
                'signal': signal,
                'confidence': confidence_analysis,
                'strategy': strategy_result,
                'market_context': market_context,
                'chart_analysis': chart_analysis,
                'entry_logic': entry_logic,
                'signal_reasoning': signal_reason,
                'ai_version': self.version,
                'analysis_number': self.analysis_count + 1,
                'success': True
            }
            
            # 7. TELEGRAM DELIVERY
            print("\n🧠 PHASE 7: TELEGRAM DELIVERY")
            
            if signal in ['CALL', 'PUT']:
                telegram_success = self.utils.send_telegram_signal(analysis_result, image_path)
                analysis_result['telegram_sent'] = telegram_success
                
                if telegram_success:
                    print("✅ Signal sent to Telegram successfully!")
                else:
                    print("❌ Failed to send signal to Telegram")
            else:
                print("⚠️ No trade signal - not sending to Telegram")
                analysis_result['telegram_sent'] = False
            
            # 8. LOGGING AND STATISTICS
            print("\n🧠 PHASE 8: LOGGING & STATISTICS")
            self.utils.log_analysis(analysis_result)
            self.analysis_count += 1
            
            # Cleanup old files
            self.utils.cleanup_old_files()
            
            print("=" * 60)
            print(f"🔮 COSMIC ANALYSIS #{self.analysis_count} COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            
            return analysis_result
            
        except Exception as e:
            error_msg = f"Analysis error: {str(e)}"
            print(f"❌ {error_msg}")
            return self._create_error_response(error_msg)
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create standardized error response"""
        
        return {
            'analysis_id': 'ERROR',
            'timestamp': datetime.now().isoformat(),
            'signal': 'ERROR',
            'confidence': {'overall_confidence': 0.0, 'confidence_grade': 'Error'},
            'error': error_message,
            'success': False,
            'telegram_sent': False
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        
        system_info = self.utils.get_system_info()
        performance_stats = self.utils.get_performance_stats()
        
        return {
            'ai_name': self.name,
            'ai_version': self.version,
            'status': 'ONLINE',
            'uptime': str(datetime.now() - self.session_start),
            'total_analyses': self.analysis_count,
            'system_info': system_info,
            'performance': performance_stats,
            'modules': {
                'perception': self.perception.name,
                'context_engine': self.context_engine.name,
                'strategy_engine': self.strategy_engine.name,
                'utils': self.utils.name
            }
        }

# Initialize the AI
cosmic_ai = CosmicOmniBrainAI()

# Flask Routes

@app.route('/')
def index():
    """Main interface"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_chart():
    """
    🎯 MAIN ANALYSIS ENDPOINT
    Receives chart upload and returns complete analysis
    """
    
    try:
        # Check if file is present
        if 'chart_image' not in request.files:
            return jsonify({'error': 'No file uploaded', 'success': False}), 400
        
        file = request.files['chart_image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected', 'success': False}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        file.save(filepath)
        
        print(f"\n📁 File saved: {unique_filename}")
        
        # Perform analysis
        result = cosmic_ai.analyze_chart_screenshot(filepath)
        
        # Add file info to result
        result['uploaded_file'] = unique_filename
        result['file_path'] = filepath
        
        return jsonify(result)
        
    except Exception as e:
        error_response = {
            'error': f'Server error: {str(e)}',
            'success': False,
            'timestamp': datetime.now().isoformat()
        }
        return jsonify(error_response), 500

@app.route('/status')
def system_status():
    """Get system status and performance metrics"""
    
    try:
        status = cosmic_ai.get_system_status()
        return jsonify(status)
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'ERROR'}), 500

@app.route('/health')
def health_check():
    """Simple health check endpoint"""
    
    return jsonify({
        'status': 'healthy',
        'ai_version': cosmic_ai.version,
        'timestamp': datetime.now().isoformat(),
        'analyses_performed': cosmic_ai.analysis_count
    })

@app.route('/api/telegram/test', methods=['POST'])
def test_telegram():
    """Test Telegram connectivity"""
    
    try:
        test_message = {
            'strategy': {
                'strategy_name': 'Telegram Test',
                'description': 'Testing Telegram connection',
                'strategy_reasoning': 'System connectivity test',
                'entry_logic': {'signal': 'TEST', 'reason': 'Connection test'}
            },
            'confidence': {'overall_confidence': 1.0},
            'market_context': {'market_narrative': 'Testing system connectivity'}
        }
        
        success = cosmic_ai.utils.send_telegram_signal(test_message)
        
        return jsonify({
            'telegram_test': 'success' if success else 'failed',
            'message_sent': success,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'telegram_test': 'error', 'error': str(e)}), 500

if __name__ == '__main__':
    print("\n🚀 STARTING COSMIC OMNI-BRAIN AI SERVER...")
    print("🌐 Access the web interface at: http://localhost:5000")
    print("📊 Upload your chart screenshots for instant analysis!")
    print("⚡ Real-time signals sent directly to Telegram!")
    print("\n🔮 THE FUTURE OF TRADING AI IS HERE! 🔮\n")
    
    # Start Flask server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,  # Set to False for production
        threaded=True
    )