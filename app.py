"""
COSMIC OMNI-BRAIN AI v∞.UNBEATABLE
Main Flask Application
Advanced Chart Analysis Web Interface
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
import traceback

# Import AI Core modules
from ai_core.perception import CandlePerception
from ai_core.context_engine import MarketContextEngine
from ai_core.strategy_engine import DynamicStrategyEngine
from ai_core.utils import TradingUtils

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'cosmic_omni_brain_unbeatable_2024'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize AI components
perception = CandlePerception()
context_engine = MarketContextEngine()
strategy_engine = DynamicStrategyEngine()
utils = TradingUtils()

class CosmicOmniBrainAI:
    def __init__(self):
        self.analysis_count = 0
        self.successful_signals = 0
        
    def analyze_chart(self, image_data, filename):
        """Main chart analysis pipeline"""
        try:
            self.analysis_count += 1
            current_time = utils.get_bd_time()
            
            print(f"🧠 Starting analysis #{self.analysis_count} at {current_time.strftime('%H:%M:%S')}")
            
            # Step 1: Perception - Extract chart data
            print("📊 Step 1: Advanced Perception Analysis...")
            chart_data = perception.analyze_chart_image(image_data)
            if not chart_data:
                return self._create_error_response("Failed to analyze chart image")
            
            # Step 2: Context Analysis - Understand market psychology
            print("🧠 Step 2: Market Context & Psychology Analysis...")
            market_context = context_engine.analyze_market_psychology(chart_data, current_time)
            
            # Step 3: Detect traps and fakeouts
            print("🎯 Step 3: Trap & Fakeout Detection...")
            traps = context_engine.detect_traps_and_fakeouts(chart_data, chart_data['price_levels'])
            market_context['traps'] = traps
            
            # Step 4: Calculate trend fatigue
            print("⚡ Step 4: Trend Fatigue Analysis...")
            fatigue = context_engine.calculate_trend_fatigue(
                chart_data['structure'], 
                market_context['dominant_emotion']
            )
            market_context['trend_fatigue'] = fatigue
            
            # Step 5: Generate dynamic strategy
            print("🚀 Step 5: Dynamic Strategy Generation...")
            strategy_result = strategy_engine.generate_dynamic_strategy(
                chart_data, market_context, current_time
            )
            
            # Step 6: Validate and finalize
            print("✅ Step 6: Validation & Signal Generation...")
            final_result = self._finalize_analysis(
                strategy_result, chart_data, market_context, current_time, filename
            )
            
            # Step 7: Send to Telegram
            if final_result['signal'] != 'NO TRADE':
                print("📱 Step 7: Sending to Telegram...")
                telegram_message = utils.create_signal_message(final_result, current_time)
                utils.send_telegram_signal(telegram_message, image_data)
                self.successful_signals += 1
            else:
                print("⚠️ Step 7: No trade conditions - sending NO TRADE message...")
                no_trade_message = utils.create_no_trade_message(final_result.get('reason', 'Market conditions unclear'))
                utils.send_telegram_signal(no_trade_message)
            
            # Log the analysis
            utils.log_analysis(chart_data, final_result)
            
            print(f"🎯 Analysis #{self.analysis_count} complete: {final_result['signal']} ({final_result['confidence']:.2f})")
            
            return final_result
            
        except Exception as e:
            print(f"❌ Error in analysis: {str(e)}")
            traceback.print_exc()
            return self._create_error_response(f"Analysis failed: {str(e)}")
    
    def _finalize_analysis(self, strategy_result, chart_data, market_context, current_time, filename):
        """Finalize analysis with all validations"""
        
        # Check trading hours
        if not utils.is_trading_hours(current_time):
            return {
                'signal': 'NO TRADE',
                'reason': 'Outside trading hours (6 AM - 10 PM UTC+6)',
                'confidence': 0.0,
                'name': 'No Strategy',
                'reasoning': 'Market closed',
                'analysis_id': utils.generate_analysis_id(),
                'timestamp': current_time.isoformat()
            }
        
        # Check confidence threshold
        if not utils.validate_confidence_threshold(strategy_result['confidence'], 0.72):
            return {
                'signal': 'NO TRADE',
                'reason': f'Confidence {strategy_result["confidence"]:.2f} below threshold (0.72)',
                'confidence': strategy_result['confidence'],
                'name': strategy_result['name'],
                'reasoning': strategy_result['reasoning'],
                'analysis_id': utils.generate_analysis_id(),
                'timestamp': current_time.isoformat()
            }
        
        # Add analysis metadata
        strategy_result.update({
            'analysis_id': utils.generate_analysis_id(),
            'timestamp': current_time.isoformat(),
            'filename': filename,
            'image_hash': utils.hash_image(open(f"uploads/{filename}", 'rb').read()) if filename else None,
            'market_narrative': context_engine.generate_market_narrative(
                market_context['dominant_emotion'],
                market_context['institutional_activity'],
                market_context['retail_sentiment'],
                market_context.get('traps', []),
                market_context.get('trend_fatigue', {})
            )
        })
        
        return strategy_result
    
    def _create_error_response(self, error_message):
        """Create standardized error response"""
        return {
            'signal': 'ERROR',
            'reason': error_message,
            'confidence': 0.0,
            'name': 'Error',
            'reasoning': 'Analysis failed',
            'analysis_id': utils.generate_analysis_id(),
            'timestamp': utils.get_bd_time().isoformat()
        }

# Initialize the AI system
cosmic_ai = CosmicOmniBrainAI()

@app.route('/')
def index():
    """Main web interface"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_chart():
    """Analyze uploaded chart"""
    try:
        if 'chart' not in request.files:
            return jsonify({'error': 'No chart file uploaded'}), 400
        
        file = request.files['chart']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not utils.validate_image_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload an image.'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Read image data
        with open(filepath, 'rb') as f:
            image_data = f.read()
        
        # Analyze the chart
        result = cosmic_ai.analyze_chart(image_data, filename)
        
        # Clean up old files
        utils.cleanup_old_files()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/status')
def status():
    """Get system status"""
    try:
        system_info = utils.get_system_info()
        
        status_data = {
            'status': 'ACTIVE',
            'ai_version': 'v∞.UNBEATABLE',
            'total_analyses': cosmic_ai.analysis_count,
            'successful_signals': cosmic_ai.successful_signals,
            'success_rate': (cosmic_ai.successful_signals / cosmic_ai.analysis_count * 100) if cosmic_ai.analysis_count > 0 else 0,
            'system_info': system_info
        }
        
        return jsonify(status_data)
        
    except Exception as e:
        return jsonify({'error': f'Status check failed: {str(e)}'}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': utils.get_bd_time().isoformat(),
        'ai_status': 'COSMIC OMNI-BRAIN AI v∞.UNBEATABLE ACTIVE'
    })

@app.route('/api/telegram/test')
def test_telegram():
    """Test Telegram integration"""
    try:
        test_message = "🌌 COSMIC OMNI-BRAIN AI v∞.UNBEATABLE\n\n✅ System Status: ACTIVE\n🧠 All modules operational\n📡 Telegram integration: WORKING\n\n🎯 Ready for chart analysis!"
        
        result = utils.send_telegram_signal(test_message)
        
        if result and result.get('ok'):
            return jsonify({'status': 'success', 'message': 'Telegram test successful'})
        else:
            return jsonify({'status': 'error', 'message': 'Telegram test failed'}), 500
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Telegram test error: {str(e)}'}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error. Please try again.'}), 500

if __name__ == '__main__':
    print("🌌 COSMIC OMNI-BRAIN AI v∞.UNBEATABLE")
    print("🧠 Advanced Chart Analysis System")
    print("🚀 Starting Flask application...")
    print("📡 Telegram integration: ACTIVE")
    print("🎯 Ready for chart analysis!")
    print("=" * 50)
    
    # Run the application
    app.run(host='0.0.0.0', port=5000, debug=False)