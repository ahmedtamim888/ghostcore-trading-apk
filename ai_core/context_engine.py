"""
COSMIC OMNI-BRAIN AI v∞.UNBEATABLE
Market Context & Psychology Engine
Advanced Market Behavior Analysis
"""

from datetime import datetime, timezone, timedelta
import math
import random

class MarketContextEngine:
    def __init__(self):
        self.market_phases = {
            'accumulation': {'volatility': 'low', 'volume': 'decreasing', 'sentiment': 'neutral'},
            'markup': {'volatility': 'increasing', 'volume': 'high', 'sentiment': 'bullish'},
            'distribution': {'volatility': 'high', 'volume': 'high', 'sentiment': 'mixed'},
            'markdown': {'volatility': 'increasing', 'volume': 'medium', 'sentiment': 'bearish'}
        }
        
        self.trap_patterns = {
            'bull_trap': {'fake_breakout': True, 'direction': 'up', 'reversal': 'down'},
            'bear_trap': {'fake_breakout': True, 'direction': 'down', 'reversal': 'up'},
            'liquidity_grab': {'stop_hunt': True, 'institutional': True},
            'fakeout': {'false_signal': True, 'quick_reversal': True}
        }
        
        self.psychology_states = {
            'greed': {'buy_pressure': 'high', 'risk': 'high', 'reversal_risk': 'high'},
            'fear': {'sell_pressure': 'high', 'oversold': True, 'bounce_potential': 'high'},
            'euphoria': {'bubble_risk': 'extreme', 'distribution_likely': True},
            'panic': {'capitulation': True, 'bottom_signal': True},
            'complacency': {'low_volatility': True, 'breakout_pending': True}
        }

    def analyze_market_psychology(self, chart_data, current_time):
        """Analyze current market psychology and sentiment"""
        
        structure = chart_data['structure']
        pixel_data = chart_data['pixel_analysis']
        candles = chart_data['candle_data']
        
        # Determine dominant emotion
        psychology = self._assess_market_emotion(structure, pixel_data)
        
        # Detect institutional activity
        institutional_signals = self._detect_institutional_activity(candles, structure)
        
        # Analyze retail sentiment
        retail_sentiment = self._analyze_retail_sentiment(pixel_data, structure)
        
        # Market manipulation detection
        manipulation_risk = self._detect_manipulation_patterns(structure, psychology)
        
        return {
            'dominant_emotion': psychology,
            'institutional_activity': institutional_signals,
            'retail_sentiment': retail_sentiment,
            'manipulation_risk': manipulation_risk,
            'market_maturity': self._assess_market_maturity(structure)
        }

    def _assess_market_emotion(self, structure, pixel_data):
        """Assess the dominant market emotion"""
        
        trend = structure['trend']
        strength = structure['strength']
        volatility = structure['volatility']
        bullish_ratio = pixel_data['bullish_ratio']
        
        # Greed detection
        if trend == 'strong_uptrend' and strength > 0.8 and volatility == 'high':
            return {
                'emotion': 'greed',
                'intensity': strength,
                'reversal_risk': 0.8,
                'description': 'Market showing signs of greed - high reversal risk'
            }
        
        # Fear detection
        elif trend == 'strong_downtrend' and strength > 0.8 and volatility == 'high':
            return {
                'emotion': 'fear',
                'intensity': strength,
                'bounce_potential': 0.7,
                'description': 'Fear dominating - potential oversold bounce'
            }
        
        # Complacency
        elif trend == 'sideways' and volatility == 'low':
            return {
                'emotion': 'complacency',
                'intensity': 0.6,
                'breakout_potential': 0.8,
                'description': 'Market complacency - breakout likely'
            }
        
        # Euphoria
        elif bullish_ratio > 0.9 and volatility == 'high':
            return {
                'emotion': 'euphoria',
                'intensity': 0.9,
                'distribution_risk': 0.9,
                'description': 'Euphoric conditions - distribution phase likely'
            }
        
        # Panic
        elif pixel_data['bearish_ratio'] > 0.9 and volatility == 'high':
            return {
                'emotion': 'panic',
                'intensity': 0.9,
                'capitulation_signal': True,
                'description': 'Panic selling - potential capitulation bottom'
            }
        
        else:
            return {
                'emotion': 'neutral',
                'intensity': 0.5,
                'description': 'Balanced market psychology'
            }

    def _detect_institutional_activity(self, candles, structure):
        """Detect signs of institutional/smart money activity"""
        
        if not candles:
            return {'activity': 'unknown', 'confidence': 0.0}
        
        # Look for large body candles (institutional moves)
        large_candles = [c for c in candles if c['body_size'] > 0.8]
        
        # Check for absorption patterns
        absorption_signals = len(large_candles) / len(candles) if candles else 0
        
        # Volume analysis (simulated based on candle sizes)
        avg_size = sum(c['body_size'] for c in candles) / len(candles)
        
        if absorption_signals > 0.3 and avg_size > 0.6:
            activity_type = 'accumulation' if structure['trend'] == 'strong_uptrend' else 'distribution'
            confidence = min(absorption_signals + avg_size, 1.0)
        else:
            activity_type = 'retail_driven'
            confidence = 0.4
        
        return {
            'activity': activity_type,
            'confidence': confidence,
            'absorption_rate': absorption_signals,
            'avg_candle_size': avg_size
        }

    def _analyze_retail_sentiment(self, pixel_data, structure):
        """Analyze retail trader sentiment"""
        
        bullish_ratio = pixel_data['bullish_ratio']
        candle_density = pixel_data['candle_density']
        
        # High candle density often indicates retail activity
        if candle_density > 0.7:
            activity_level = 'high'
        elif candle_density > 0.4:
            activity_level = 'medium'
        else:
            activity_level = 'low'
        
        # Sentiment bias
        if bullish_ratio > 0.7:
            sentiment = 'extremely_bullish'
            contrarian_signal = 'bearish'
        elif bullish_ratio > 0.6:
            sentiment = 'bullish'
            contrarian_signal = 'neutral'
        elif bullish_ratio < 0.3:
            sentiment = 'extremely_bearish'
            contrarian_signal = 'bullish'
        elif bullish_ratio < 0.4:
            sentiment = 'bearish'
            contrarian_signal = 'neutral'
        else:
            sentiment = 'neutral'
            contrarian_signal = 'neutral'
        
        return {
            'sentiment': sentiment,
            'activity_level': activity_level,
            'contrarian_signal': contrarian_signal,
            'bullish_ratio': bullish_ratio
        }

    def _detect_manipulation_patterns(self, structure, psychology):
        """Detect potential market manipulation"""
        
        manipulation_score = 0.0
        signals = []
        
        # High volatility with weak trend (whipsaw)
        if structure['volatility'] == 'high' and structure['strength'] < 0.5:
            manipulation_score += 0.3
            signals.append('whipsaw_pattern')
        
        # Extreme emotions often precede manipulation
        if psychology['emotion'] in ['greed', 'fear', 'euphoria', 'panic']:
            manipulation_score += 0.2
            signals.append('emotional_extreme')
        
        # Sudden trend changes
        if structure['trend'] == 'weak_trend':
            manipulation_score += 0.1
            signals.append('trend_uncertainty')
        
        risk_level = 'high' if manipulation_score > 0.5 else 'medium' if manipulation_score > 0.3 else 'low'
        
        return {
            'risk_level': risk_level,
            'score': manipulation_score,
            'signals': signals
        }

    def _assess_market_maturity(self, structure):
        """Assess the maturity of current market move"""
        
        trend_strength = structure['strength']
        volatility = structure['volatility']
        
        if trend_strength > 0.8 and volatility == 'high':
            return 'mature'  # Move may be exhausting
        elif trend_strength > 0.6 and volatility == 'medium':
            return 'developing'  # Move has room to continue
        elif trend_strength < 0.4:
            return 'early'  # Move just beginning
        else:
            return 'transitional'  # Uncertain phase

    def detect_traps_and_fakeouts(self, chart_data, price_levels):
        """Detect potential traps and fakeout patterns"""
        
        structure = chart_data['structure']
        candles = chart_data['candle_data']
        
        traps = []
        
        # Bull trap detection
        if (structure['trend'] == 'strong_uptrend' and 
            structure['volatility'] == 'high' and 
            structure['strength'] > 0.9):
            
            traps.append({
                'type': 'bull_trap',
                'probability': 0.7,
                'expected_direction': 'bearish',
                'description': 'Potential bull trap - extreme bullish conditions'
            })
        
        # Bear trap detection  
        elif (structure['trend'] == 'strong_downtrend' and 
              structure['volatility'] == 'high' and 
              structure['strength'] > 0.9):
            
            traps.append({
                'type': 'bear_trap',
                'probability': 0.7,
                'expected_direction': 'bullish',
                'description': 'Potential bear trap - extreme bearish conditions'
            })
        
        # Liquidity grab patterns
        if len(candles) > 3:
            recent_volatility = sum(c['upper_wick'] + c['lower_wick'] for c in candles[-3:]) / 3
            if recent_volatility > 0.8:
                traps.append({
                    'type': 'liquidity_grab',
                    'probability': 0.6,
                    'description': 'High wick activity suggests liquidity hunting'
                })
        
        return traps

    def calculate_trend_fatigue(self, structure, psychology):
        """Calculate how tired/exhausted the current trend is"""
        
        base_fatigue = structure['strength']  # Higher strength = more fatigue
        
        # Emotional extremes increase fatigue
        if psychology['emotion'] in ['greed', 'euphoria']:
            emotion_fatigue = 0.3
        elif psychology['emotion'] in ['fear', 'panic']:
            emotion_fatigue = 0.3
        else:
            emotion_fatigue = 0.0
        
        # High volatility increases fatigue
        volatility_fatigue = 0.2 if structure['volatility'] == 'high' else 0.0
        
        total_fatigue = min(base_fatigue + emotion_fatigue + volatility_fatigue, 1.0)
        
        if total_fatigue > 0.8:
            fatigue_level = 'extreme'
            reversal_probability = 0.8
        elif total_fatigue > 0.6:
            fatigue_level = 'high'
            reversal_probability = 0.6
        elif total_fatigue > 0.4:
            fatigue_level = 'medium'
            reversal_probability = 0.4
        else:
            fatigue_level = 'low'
            reversal_probability = 0.2
        
        return {
            'level': fatigue_level,
            'score': total_fatigue,
            'reversal_probability': reversal_probability
        }

    def generate_market_narrative(self, psychology, institutional, retail, traps, fatigue):
        """Generate a comprehensive market narrative"""
        
        narrative_parts = []
        
        # Psychology narrative
        emotion = psychology['dominant_emotion']
        narrative_parts.append(f"Market psychology: {emotion['emotion']} (intensity: {emotion['intensity']:.1f})")
        
        # Institutional activity
        inst_activity = institutional['activity']
        narrative_parts.append(f"Institutional activity: {inst_activity} (confidence: {institutional['confidence']:.1f})")
        
        # Retail sentiment
        retail_sentiment = retail['sentiment']
        narrative_parts.append(f"Retail sentiment: {retail_sentiment}")
        
        # Trap warnings
        if traps:
            trap_types = [t['type'] for t in traps]
            narrative_parts.append(f"Trap signals: {', '.join(trap_types)}")
        
        # Trend fatigue
        narrative_parts.append(f"Trend fatigue: {fatigue['level']} (reversal risk: {fatigue['reversal_probability']:.1f})")
        
        return " | ".join(narrative_parts)