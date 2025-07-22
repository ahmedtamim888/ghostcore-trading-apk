"""
🔮 COSMIC OMNI-BRAIN AI - CONTEXT ENGINE
Advanced market psychology and context analysis
"""

from typing import Dict, List, Any, Optional
import json
from datetime import datetime, timezone, timedelta

class MarketContextEngine:
    """
    🧠 ULTIMATE MARKET PSYCHOLOGY ANALYZER
    Understands market traps, liquidity, manipulation, sentiment
    """
    
    def __init__(self):
        self.name = "COSMIC CONTEXT ENGINE"
        self.version = "∞.UNBEATABLE"
        
        # Market context patterns
        self.trap_patterns = {
            'bull_trap': {
                'sequence': ['bearish', 'bullish_fake', 'bearish_strong'],
                'confidence': 0.85
            },
            'bear_trap': {
                'sequence': ['bullish', 'bearish_fake', 'bullish_strong'],
                'confidence': 0.85
            },
            'liquidity_grab': {
                'wick_ratio': 0.6,
                'reversal_strength': 0.8
            },
            'stop_hunt': {
                'wick_extension': 1.5,
                'immediate_reversal': True
            }
        }
        
        # Market phases
        self.market_phases = {
            'accumulation': {'volatility': 'low', 'trend': 'sideways'},
            'markup': {'volatility': 'medium', 'trend': 'up'},
            'distribution': {'volatility': 'high', 'trend': 'sideways'},
            'markdown': {'volatility': 'medium', 'trend': 'down'}
        }
        
        # Sentiment indicators
        self.sentiment_factors = [
            'trend_strength',
            'volume_profile',
            'rejection_levels', 
            'breakout_quality',
            'momentum_shifts'
        ]
        
    def analyze_market_psychology(self, chart_data: Dict) -> Dict:
        """
        🧠 DEEP MARKET PSYCHOLOGY ANALYSIS
        Understand what the market is really doing
        """
        
        print("🔮 COSMIC CONTEXT: Analyzing market psychology...")
        
        candles = chart_data.get('candles', [])
        price_levels = chart_data.get('price_levels', {})
        patterns = chart_data.get('patterns', [])
        
        if not candles:
            return self._generate_insufficient_data_context()
        
        # 1. Detect market traps and manipulation
        trap_analysis = self._detect_market_traps(candles)
        
        # 2. Analyze liquidity behavior
        liquidity_analysis = self._analyze_liquidity_patterns(candles, price_levels)
        
        # 3. Determine market phase
        market_phase = self._identify_market_phase(candles)
        
        # 4. Assess trend fatigue
        trend_fatigue = self._assess_trend_fatigue(candles)
        
        # 5. Analyze momentum shifts
        momentum_analysis = self._analyze_momentum_shifts(candles)
        
        # 6. Detect institutional behavior
        institutional_signals = self._detect_institutional_activity(candles, patterns)
        
        # 7. Overall market sentiment
        sentiment_score = self._calculate_market_sentiment(
            trap_analysis, liquidity_analysis, market_phase, 
            trend_fatigue, momentum_analysis
        )
        
        return {
            'traps': trap_analysis,
            'liquidity': liquidity_analysis,
            'market_phase': market_phase,
            'trend_fatigue': trend_fatigue,
            'momentum': momentum_analysis,
            'institutional': institutional_signals,
            'sentiment': sentiment_score,
            'market_narrative': self._generate_market_narrative(
                trap_analysis, liquidity_analysis, market_phase
            ),
            'confidence': self._calculate_context_confidence(candles),
            'timestamp': datetime.now().isoformat()
        }
    
    def _detect_market_traps(self, candles: List[Dict]) -> Dict:
        """Detect bull traps, bear traps, and false breakouts"""
        
        if len(candles) < 5:
            return {'detected': [], 'risk_level': 'unknown'}
        
        detected_traps = []
        recent_candles = candles[-5:]
        
        # Check for bull trap pattern
        if self._is_bull_trap_pattern(recent_candles):
            detected_traps.append({
                'type': 'bull_trap',
                'confidence': 0.8,
                'description': 'False bullish breakout followed by reversal'
            })
        
        # Check for bear trap pattern
        if self._is_bear_trap_pattern(recent_candles):
            detected_traps.append({
                'type': 'bear_trap',
                'confidence': 0.8,
                'description': 'False bearish breakdown followed by reversal'
            })
        
        # Check for liquidity grab
        for candle in recent_candles:
            if self._is_liquidity_grab(candle):
                detected_traps.append({
                    'type': 'liquidity_grab',
                    'confidence': 0.75,
                    'description': 'Long wick indicating liquidity hunting'
                })
        
        # Assess overall trap risk
        risk_level = 'high' if len(detected_traps) >= 2 else 'medium' if detected_traps else 'low'
        
        return {
            'detected': detected_traps,
            'risk_level': risk_level,
            'trap_count': len(detected_traps)
        }
    
    def _is_bull_trap_pattern(self, candles: List[Dict]) -> bool:
        """Check for bull trap pattern"""
        
        if len(candles) < 3:
            return False
        
        # Pattern: Strong bullish move followed by immediate bearish reversal
        last_three = candles[-3:]
        
        return (
            last_three[0]['direction'] == 'bearish' and
            last_three[1]['direction'] == 'bullish' and
            last_three[1]['strength'] > 0.7 and
            last_three[2]['direction'] == 'bearish' and
            last_three[2]['strength'] > last_three[1]['strength']
        )
    
    def _is_bear_trap_pattern(self, candles: List[Dict]) -> bool:
        """Check for bear trap pattern"""
        
        if len(candles) < 3:
            return False
        
        # Pattern: Strong bearish move followed by immediate bullish reversal
        last_three = candles[-3:]
        
        return (
            last_three[0]['direction'] == 'bullish' and
            last_three[1]['direction'] == 'bearish' and
            last_three[1]['strength'] > 0.7 and
            last_three[2]['direction'] == 'bullish' and
            last_three[2]['strength'] > last_three[1]['strength']
        )
    
    def _is_liquidity_grab(self, candle: Dict) -> bool:
        """Check if candle shows liquidity grab pattern"""
        
        # Long wicks indicate liquidity hunting
        return (
            candle['ratios']['upper_wick'] > 0.4 or
            candle['ratios']['lower_wick'] > 0.4
        ) and candle['ratios']['body'] < 0.5
    
    def _analyze_liquidity_patterns(self, candles: List[Dict], price_levels: Dict) -> Dict:
        """Analyze liquidity behavior and zones"""
        
        if not candles:
            return {'zones': [], 'behavior': 'unknown'}
        
        liquidity_zones = []
        
        # Identify liquidity zones around support/resistance
        for level in price_levels.get('support', []):
            zone_activity = self._assess_zone_activity(candles, level['level'], 'support')
            if zone_activity['activity_score'] > 0.3:
                liquidity_zones.append({
                    'type': 'support_liquidity',
                    'level': level['level'],
                    'strength': level['strength'],
                    'activity': zone_activity
                })
        
        for level in price_levels.get('resistance', []):
            zone_activity = self._assess_zone_activity(candles, level['level'], 'resistance')
            if zone_activity['activity_score'] > 0.3:
                liquidity_zones.append({
                    'type': 'resistance_liquidity',
                    'level': level['level'],
                    'strength': level['strength'],
                    'activity': zone_activity
                })
        
        # Determine overall liquidity behavior
        behavior = self._classify_liquidity_behavior(candles, liquidity_zones)
        
        return {
            'zones': liquidity_zones,
            'behavior': behavior,
            'zone_count': len(liquidity_zones)
        }
    
    def _assess_zone_activity(self, candles: List[Dict], level: int, zone_type: str) -> Dict:
        """Assess activity around a price level"""
        
        tolerance = 20  # Price tolerance for zone
        touches = 0
        rejections = 0
        
        for candle in candles:
            # Check if candle interacted with level
            if zone_type == 'support':
                if abs(candle['body']['bottom'] - level) <= tolerance:
                    touches += 1
                    if candle['direction'] == 'bullish':
                        rejections += 1
            else:  # resistance
                if abs(candle['body']['top'] - level) <= tolerance:
                    touches += 1
                    if candle['direction'] == 'bearish':
                        rejections += 1
        
        activity_score = touches / len(candles) if candles else 0
        rejection_rate = rejections / max(touches, 1)
        
        return {
            'touches': touches,
            'rejections': rejections,
            'activity_score': activity_score,
            'rejection_rate': rejection_rate
        }
    
    def _classify_liquidity_behavior(self, candles: List[Dict], zones: List[Dict]) -> str:
        """Classify overall liquidity behavior"""
        
        if not zones:
            return 'no_clear_zones'
        
        # Analyze recent candle behavior near zones
        recent_candles = candles[-3:] if len(candles) >= 3 else candles
        
        zone_interactions = 0
        for candle in recent_candles:
            for zone in zones:
                if abs(candle['position']['y'] - zone['level']) <= 30:
                    zone_interactions += 1
        
        if zone_interactions >= 2:
            return 'active_zone_testing'
        elif zone_interactions == 1:
            return 'zone_approach'
        else:
            return 'free_movement'
    
    def _identify_market_phase(self, candles: List[Dict]) -> Dict:
        """Identify current market phase"""
        
        if len(candles) < 10:
            return {'phase': 'insufficient_data', 'confidence': 0}
        
        recent_candles = candles[-10:]
        
        # Calculate volatility
        volatility = self._calculate_volatility(recent_candles)
        
        # Calculate trend direction
        bullish_count = sum(1 for c in recent_candles if c['direction'] == 'bullish')
        trend_ratio = bullish_count / len(recent_candles)
        
        # Determine phase
        if volatility < 0.3 and 0.4 <= trend_ratio <= 0.6:
            phase = 'accumulation'
            confidence = 0.8
        elif volatility >= 0.3 and trend_ratio > 0.7:
            phase = 'markup'
            confidence = 0.9
        elif volatility >= 0.5 and 0.4 <= trend_ratio <= 0.6:
            phase = 'distribution'
            confidence = 0.85
        elif volatility >= 0.3 and trend_ratio < 0.3:
            phase = 'markdown'
            confidence = 0.9
        else:
            phase = 'transition'
            confidence = 0.6
        
        return {
            'phase': phase,
            'confidence': confidence,
            'volatility': volatility,
            'trend_ratio': trend_ratio
        }
    
    def _calculate_volatility(self, candles: List[Dict]) -> float:
        """Calculate volatility from candle data"""
        
        if not candles:
            return 0
        
        # Use total height variance as volatility measure
        heights = [candle['total_height'] for candle in candles]
        avg_height = sum(heights) / len(heights)
        
        variance = sum((h - avg_height) ** 2 for h in heights) / len(heights)
        volatility = (variance ** 0.5) / avg_height if avg_height > 0 else 0
        
        return min(volatility, 1.0)
    
    def _assess_trend_fatigue(self, candles: List[Dict]) -> Dict:
        """Assess if current trend is showing fatigue"""
        
        if len(candles) < 8:
            return {'fatigue_level': 'unknown', 'signals': []}
        
        recent_candles = candles[-8:]
        fatigue_signals = []
        
        # Check for decreasing momentum
        if self._is_momentum_decreasing(recent_candles):
            fatigue_signals.append('decreasing_momentum')
        
        # Check for divergence patterns
        if self._has_strength_divergence(recent_candles):
            fatigue_signals.append('strength_divergence')
        
        # Check for pattern exhaustion
        if self._has_pattern_exhaustion(recent_candles):
            fatigue_signals.append('pattern_exhaustion')
        
        # Determine fatigue level
        fatigue_level = (
            'high' if len(fatigue_signals) >= 2 else
            'medium' if len(fatigue_signals) == 1 else
            'low'
        )
        
        return {
            'fatigue_level': fatigue_level,
            'signals': fatigue_signals,
            'signal_count': len(fatigue_signals)
        }
    
    def _is_momentum_decreasing(self, candles: List[Dict]) -> bool:
        """Check if momentum is decreasing"""
        
        if len(candles) < 4:
            return False
        
        # Compare recent candle strengths
        first_half = candles[:len(candles)//2]
        second_half = candles[len(candles)//2:]
        
        avg_strength_first = sum(c['strength'] for c in first_half) / len(first_half)
        avg_strength_second = sum(c['strength'] for c in second_half) / len(second_half)
        
        return avg_strength_second < avg_strength_first * 0.8
    
    def _has_strength_divergence(self, candles: List[Dict]) -> bool:
        """Check for strength divergence"""
        
        if len(candles) < 6:
            return False
        
        # Look for weakening candles in trend direction
        trend_direction = self._get_dominant_direction(candles)
        trend_candles = [c for c in candles if c['direction'] == trend_direction]
        
        if len(trend_candles) < 3:
            return False
        
        # Check if trend candles are getting weaker
        strengths = [c['strength'] for c in trend_candles]
        return len(strengths) >= 3 and strengths[-1] < strengths[0] * 0.7
    
    def _has_pattern_exhaustion(self, candles: List[Dict]) -> bool:
        """Check for pattern exhaustion"""
        
        # Too many consecutive candles in same direction
        consecutive_count = 1
        last_direction = candles[-1]['direction']
        
        for candle in reversed(candles[:-1]):
            if candle['direction'] == last_direction:
                consecutive_count += 1
            else:
                break
        
        return consecutive_count >= 5  # 5+ consecutive candles = exhaustion
    
    def _get_dominant_direction(self, candles: List[Dict]) -> str:
        """Get dominant direction from candles"""
        
        bullish_count = sum(1 for c in candles if c['direction'] == 'bullish')
        return 'bullish' if bullish_count > len(candles) / 2 else 'bearish'
    
    def _analyze_momentum_shifts(self, candles: List[Dict]) -> Dict:
        """Analyze momentum shifts and changes"""
        
        if len(candles) < 5:
            return {'shifts': [], 'current_momentum': 'unknown'}
        
        momentum_shifts = []
        
        # Look for momentum shift patterns
        for i in range(2, len(candles)):
            prev_momentum = self._calculate_local_momentum(candles[i-2:i])
            curr_momentum = self._calculate_local_momentum(candles[i-1:i+1])
            
            # Detect significant momentum change
            if abs(curr_momentum - prev_momentum) > 0.4:
                momentum_shifts.append({
                    'position': i,
                    'direction': 'bullish' if curr_momentum > prev_momentum else 'bearish',
                    'strength': abs(curr_momentum - prev_momentum)
                })
        
        # Current momentum
        current_momentum = self._calculate_local_momentum(candles[-3:])
        
        return {
            'shifts': momentum_shifts[-3:],  # Last 3 shifts
            'current_momentum': current_momentum,
            'shift_count': len(momentum_shifts)
        }
    
    def _calculate_local_momentum(self, candles: List[Dict]) -> float:
        """Calculate momentum for a small group of candles"""
        
        if not candles:
            return 0
        
        bullish_strength = sum(c['strength'] for c in candles if c['direction'] == 'bullish')
        bearish_strength = sum(c['strength'] for c in candles if c['direction'] == 'bearish')
        
        total_strength = bullish_strength + bearish_strength
        if total_strength == 0:
            return 0
        
        return (bullish_strength - bearish_strength) / total_strength
    
    def _detect_institutional_activity(self, candles: List[Dict], patterns: List[Dict]) -> Dict:
        """Detect signs of institutional trading activity"""
        
        institutional_signals = []
        
        # Large candle bodies indicate institutional involvement
        for candle in candles[-5:]:
            if candle['strength'] > 0.8 and candle['total_height'] > 50:
                institutional_signals.append({
                    'type': 'large_volume_candle',
                    'direction': candle['direction'],
                    'strength': candle['strength']
                })
        
        # Engulfing patterns often show institutional activity
        for pattern in patterns:
            if 'engulfing' in pattern['type']:
                institutional_signals.append({
                    'type': 'institutional_engulfing',
                    'pattern': pattern['type'],
                    'confidence': pattern['confidence']
                })
        
        # Assess activity level
        activity_level = (
            'high' if len(institutional_signals) >= 3 else
            'medium' if len(institutional_signals) >= 1 else
            'low'
        )
        
        return {
            'signals': institutional_signals,
            'activity_level': activity_level,
            'signal_count': len(institutional_signals)
        }
    
    def _calculate_market_sentiment(self, trap_analysis: Dict, liquidity_analysis: Dict, 
                                   market_phase: Dict, trend_fatigue: Dict, 
                                   momentum_analysis: Dict) -> Dict:
        """Calculate overall market sentiment score"""
        
        sentiment_score = 0.5  # Neutral starting point
        confidence = 0.5
        
        # Adjust based on trap risk
        if trap_analysis['risk_level'] == 'high':
            sentiment_score -= 0.2
        elif trap_analysis['risk_level'] == 'low':
            sentiment_score += 0.1
        
        # Adjust based on market phase
        phase = market_phase.get('phase', 'unknown')
        if phase == 'markup':
            sentiment_score += 0.2
        elif phase == 'markdown':
            sentiment_score -= 0.2
        elif phase == 'accumulation':
            sentiment_score += 0.1
        elif phase == 'distribution':
            sentiment_score -= 0.1
        
        # Adjust based on trend fatigue
        fatigue_level = trend_fatigue.get('fatigue_level', 'unknown')
        if fatigue_level == 'high':
            sentiment_score -= 0.15
        elif fatigue_level == 'low':
            sentiment_score += 0.1
        
        # Adjust based on momentum
        current_momentum = momentum_analysis.get('current_momentum', 0)
        sentiment_score += current_momentum * 0.3
        
        # Normalize score
        sentiment_score = max(0, min(1, sentiment_score))
        
        # Calculate confidence
        confidence = min(1.0, (
            market_phase.get('confidence', 0) * 0.4 +
            (1 - (len(trap_analysis.get('detected', [])) * 0.1)) * 0.3 +
            abs(current_momentum) * 0.3
        ))
        
        # Determine sentiment label
        if sentiment_score >= 0.7:
            sentiment_label = 'very_bullish'
        elif sentiment_score >= 0.6:
            sentiment_label = 'bullish'
        elif sentiment_score >= 0.4:
            sentiment_label = 'neutral'
        elif sentiment_score >= 0.3:
            sentiment_label = 'bearish'
        else:
            sentiment_label = 'very_bearish'
        
        return {
            'score': sentiment_score,
            'label': sentiment_label,
            'confidence': confidence
        }
    
    def _generate_market_narrative(self, trap_analysis: Dict, liquidity_analysis: Dict, 
                                 market_phase: Dict) -> str:
        """Generate human-readable market narrative"""
        
        narratives = []
        
        # Phase narrative
        phase = market_phase.get('phase', 'unknown')
        if phase == 'markup':
            narratives.append("Market in strong upward movement phase")
        elif phase == 'markdown':
            narratives.append("Market in selling pressure phase")
        elif phase == 'accumulation':
            narratives.append("Market in consolidation/accumulation phase")
        elif phase == 'distribution':
            narratives.append("Market showing distribution patterns")
        
        # Trap narrative
        trap_risk = trap_analysis.get('risk_level', 'unknown')
        if trap_risk == 'high':
            narratives.append("High trap risk - be cautious of false moves")
        elif trap_analysis.get('detected'):
            trap_types = [t['type'] for t in trap_analysis['detected']]
            narratives.append(f"Detected: {', '.join(trap_types)}")
        
        # Liquidity narrative
        liquidity_behavior = liquidity_analysis.get('behavior', 'unknown')
        if liquidity_behavior == 'active_zone_testing':
            narratives.append("Active testing of key price zones")
        elif liquidity_behavior == 'zone_approach':
            narratives.append("Approaching important liquidity zone")
        
        return ". ".join(narratives) if narratives else "Market structure unclear"
    
    def _generate_insufficient_data_context(self) -> Dict:
        """Generate context when insufficient data available"""
        
        return {
            'traps': {'detected': [], 'risk_level': 'unknown'},
            'liquidity': {'zones': [], 'behavior': 'unknown'},
            'market_phase': {'phase': 'insufficient_data', 'confidence': 0},
            'trend_fatigue': {'fatigue_level': 'unknown', 'signals': []},
            'momentum': {'shifts': [], 'current_momentum': 0},
            'institutional': {'signals': [], 'activity_level': 'unknown'},
            'sentiment': {'score': 0.5, 'label': 'neutral', 'confidence': 0},
            'market_narrative': 'Insufficient data for market analysis',
            'confidence': 0,
            'timestamp': datetime.now().isoformat()
        }
    
    def _calculate_context_confidence(self, candles: List[Dict]) -> float:
        """Calculate confidence in context analysis"""
        
        # Base confidence on data quality and quantity
        data_quality = min(len(candles) / 20, 1.0)  # More candles = better
        
        # Adjust for candle quality
        if candles:
            avg_strength = sum(c['strength'] for c in candles) / len(candles)
            candle_quality = avg_strength
        else:
            candle_quality = 0
        
        confidence = (data_quality * 0.6 + candle_quality * 0.4)
        return min(confidence, 0.95)  # Cap at 95%