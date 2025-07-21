import os
import cv2
import time
import numpy as np
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from PIL import Image

# Import our COSMIC OMNI-BRAIN AI modules
from ai_core.perception import CandlePerception
from ai_core.context_engine import MarketContextEngine
from ai_core.strategy_engine import DynamicStrategyEngine
from ai_core.utils import TradingUtils
from cosmic_features import CosmicTradingFeatures

class CosmicOmniBrainAI:
    """The ultimate binary options signal bot - COSMIC OMNI-BRAIN AI v∞.UNBEATABLE"""
    
    def __init__(self):
        self.name = "COSMIC OMNI-BRAIN AI v∞.UNBEATABLE"
        self.version = "∞.UNBEATABLE"
        
        # Initialize AI components
        self.perception = CandlePerception()
        self.context_engine = MarketContextEngine()
        self.strategy_engine = DynamicStrategyEngine()
        self.utils = TradingUtils()
        self.trading_features = CosmicTradingFeatures()
        
        # Performance tracking
        self.analysis_count = 0
        self.success_rate = 0.0
        
        self.utils.logger.info(f"🔮 {self.name} initialized successfully!")
    
    def analyze_chart(self, image_path: str) -> dict:
        """Main analysis function - the cosmic intelligence at work"""
        start_time = time.time()
        
        try:
            # Validate image first
            if not self.utils.validate_image(image_path):
                return self._error_response("Invalid image format or size")
            
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                return self._error_response("Could not load image")
            
            # Step 1: Ultra-precise candle detection
            self.utils.logger.info("🧠 Activating perception engine...")
            candles = self.perception.detect_candles(image)
            
            if len(candles) < 3:
                return self._error_response("Insufficient candle data - need at least 3 valid candles")
            
            # Step 2: Deep market context analysis
            self.utils.logger.info("🌀 Analyzing market psychology and context...")
            market_context = self.context_engine.analyze_market_context(candles, image.shape)
            
            # Step 3: Dynamic strategy generation
            self.utils.logger.info("⚡ Generating unique trading strategy...")
            signal_result = self.strategy_engine.generate_signal(candles, market_context, image.shape)
            
            # Step 4: Create annotated visualization
            annotated_image = self.utils.create_annotated_image(image, candles, signal_result)
            
            # Save annotated image
            debug_path = os.path.join('static', 'cosmic_analysis.png')
            cv2.imwrite(debug_path, annotated_image)
            
            # Step 5: Calculate processing metrics
            processing_time = time.time() - start_time
            
            # Step 6: Prepare comprehensive response
            response = {
                'signal': signal_result['signal'],
                'confidence': round(signal_result['confidence'], 1),
                'timeframe': '1 Minute',
                'local_time': self.utils.get_bd_time(),
                'strategy': signal_result['strategy'],
                'reasoning': signal_result['reasoning'],
                'market_adaptation': signal_result['market_adaptation'],
                'risk_level': signal_result['risk_level'],
                'candles_detected': len(candles),
                'market_health': round(market_context['market_health'] * 100, 1),
                'processing_time_ms': round(processing_time * 1000, 2),
                'ai_version': self.version,
                'analysis_details': {
                    'market_structure': market_context['market_structure']['trend'],
                    'volatility': market_context['volatility_profile']['volatility_trend'],
                    'trap_risk': max(
                        market_context['trap_detection']['bull_trap_risk'],
                        market_context['trap_detection']['bear_trap_risk']
                    ),
                    'liquidity_risk': market_context['liquidity_zones']['liquidity_sweep_risk']
                }
            }
            
            # Step 7: Send to Telegram if configured
            try:
                self.utils.send_telegram_signal(response, debug_path)
            except Exception as e:
                self.utils.logger.warning(f"Telegram notification failed: {e}")
            
            # Step 8: Log performance
            self.utils.log_signal(response, len(candles), processing_time)
            self.analysis_count += 1
            
            # Clean up uploaded file
            if os.path.exists(image_path):
                os.remove(image_path)
            
            return response
            
        except Exception as e:
            self.utils.logger.error(f"🚨 COSMIC ANALYSIS FAILED: {str(e)}")
            return self._error_response(f"Analysis failed: {str(e)}")
    
    def _error_response(self, error_message: str) -> dict:
        """Generate error response"""
        return {
            'error': self.utils.format_error_message(error_message),
            'signal': 'ERROR',
            'confidence': 0,
            'timeframe': '1 Minute',
            'local_time': self.utils.get_bd_time(),
            'ai_version': self.version
        }
    
    def get_system_status(self) -> dict:
        """Get system status information"""
        return {
            'ai_name': self.name,
            'version': self.version,
            'analyses_performed': self.analysis_count,
            'system_info': self.utils.get_system_info(),
            'current_time': self.utils.get_bd_time(),
            'status': 'OPERATIONAL' if self.analysis_count >= 0 else 'INITIALIZING'
        }

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATIC_FOLDER'] = 'static'

# Create directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['STATIC_FOLDER'], exist_ok=True)

# Initialize the COSMIC OMNI-BRAIN AI
cosmic_ai = CosmicOmniBrainAI()

@app.route('/')
def index():
    """Main interface"""
    system_status = cosmic_ai.get_system_status()
    return render_template('index.html', system_status=system_status)

@app.route('/analyze', methods=['POST'])
def analyze_chart():
    """Analyze uploaded chart image"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'})
        
        # Check file type
        allowed_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp'}
        file_ext = os.path.splitext(file.filename.lower())[1]
        
        if file_ext not in allowed_extensions:
            return jsonify({'error': 'Unsupported file format. Please use PNG, JPG, or other image formats.'})
        
        if file:
            # Secure filename and save
            filename = secure_filename(file.filename)
            if not filename:
                filename = 'chart_image.png'
            
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Analyze with COSMIC OMNI-BRAIN AI
            result = cosmic_ai.analyze_chart(filepath)
            
            return jsonify(result)
    
    except Exception as e:
        cosmic_ai.utils.logger.error(f"Request processing failed: {str(e)}")
        return jsonify({'error': f'Request processing failed: {str(e)}'})

@app.route('/debug-image')
def get_debug_image():
    """Get the annotated analysis image"""
    debug_path = os.path.join(app.config['STATIC_FOLDER'], 'cosmic_analysis.png')
    if os.path.exists(debug_path):
        return send_file(debug_path, mimetype='image/png')
    return jsonify({'error': 'No analysis image available'})

@app.route('/status')
def get_status():
    """Get system status"""
    return jsonify(cosmic_ai.get_system_status())

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'ai_name': cosmic_ai.name,
        'version': cosmic_ai.version,
        'timestamp': cosmic_ai.utils.get_bd_time()
    })

@app.route('/dashboard')
def dashboard():
    """Advanced trading dashboard"""
    return render_template('dashboard.html')

@app.route('/api/dashboard-data')
def dashboard_data():
    """API endpoint for dashboard data"""
    try:
        dashboard_data = cosmic_ai.trading_features.get_trading_dashboard_data()
        return jsonify(dashboard_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Periodic cleanup
@app.before_first_request
def setup_cleanup():
    """Setup periodic cleanup"""
    try:
        cosmic_ai.utils.cleanup_old_files(app.config['UPLOAD_FOLDER'], max_age_hours=1)
        cosmic_ai.utils.cleanup_old_files(app.config['STATIC_FOLDER'], max_age_hours=24)
    except Exception as e:
        cosmic_ai.utils.logger.warning(f"Cleanup setup failed: {e}")

if __name__ == '__main__':
    # Startup message
    print("🔮" * 50)
    print(f"🚀 LAUNCHING {cosmic_ai.name}")
    print("💫 The Ultimate Binary Options Signal Bot")
    print("🧠 Omni-brain intelligence activated")
    print("⚡ Dynamic strategy generation online")
    print("🎯 Ready for market domination")
    print("🔮" * 50)
    
    # Start the cosmic intelligence
    app.run(host='0.0.0.0', port=5000, debug=True)