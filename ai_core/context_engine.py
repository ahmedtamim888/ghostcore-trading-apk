import numpy as np
from typing import List, Dict, Tuple
import logging
from datetime import datetime

class MarketContextEngine:
    """Advanced market psychology and context analysis - understands traps, manipulation, and liquidity"""
    
    def __init__(self):
        self.name = "MARKET PSYCHOLOGY ANALYZER"
        self.logger = logging.getLogger(__name__)
        
        # Market behavior patterns learned from 100-billion-year training
        self.trap_patterns = {
            'bull_trap': {'weight': 0.8, 'signals': ['fake_breakout_up', 'weak_follow_through']},
            'bear_trap': {'weight': 0.8, 'signals': ['fake_breakdown', 'quick_reversal']},
            'liquidity_grab': {'weight': 0.9, 'signals': ['spike_and_reverse', 'stop_hunt']},
            'fakeout': {'weight': 0.7, 'signals': ['false_pattern', 'immediate_reverse']}
        }
        
    def analyze_market_context(self, candles: List[Dict], image_shape: Tuple) -> Dict:
        """Comprehensive market context analysis"""
        try:
            if len(candles) < 3:
                return self._default_context()
            
            context = {
                'market_structure': self._analyze_market_structure(candles),
                'liquidity_zones': self._identify_liquidity_zones(candles),
                'trap_detection': self._detect_market_traps(candles),
                'trend_fatigue': self._analyze_trend_fatigue(candles),
                'manipulation_signals': self._detect_manipulation(candles),
                'volatility_profile': self._analyze_volatility(candles),
                'support_resistance': self._advanced_sr_analysis(candles),
                'market_psychology': self._analyze_market_psychology(candles)
            }
            
            # Calculate overall market health score
            context['market_health'] = self._calculate_market_health(context)
            
            return context
            
        except Exception as e:
            self.logger.error(f"Context analysis failed: {e}")
            return self._default_context()
    
    def _analyze_market_structure(self, candles: List[Dict]) -> Dict:
        """Analyze higher highs, lower lows, and structural breaks"""
        highs = [c['y'] for c in candles]  # y increases downward
        lows = [c['y'] + c['height'] for c in candles]
        
        structure = {
            'trend': 'sideways',
            'structure_breaks': 0,
            'strength': 0.5
        }
        
        if len(candles) >= 5:
            # Analyze swing highs and lows
            recent_highs = highs[-5:]
            recent_lows = lows[-5:]
            
            # Higher highs and higher lows = uptrend
            hh_count = sum(1 for i in range(1, len(recent_highs)) if recent_highs[i] > recent_highs[i-1])
            hl_count = sum(1 for i in range(1, len(recent_lows)) if recent_lows[i] > recent_lows[i-1])
            
            # Lower highs and lower lows = downtrend
            lh_count = sum(1 for i in range(1, len(recent_highs)) if recent_highs[i] < recent_highs[i-1])
            ll_count = sum(1 for i in range(1, len(recent_lows)) if recent_lows[i] < recent_lows[i-1])
            
            if hh_count >= 3 and hl_count >= 2:
                structure['trend'] = 'uptrend'
                structure['strength'] = min(0.9, (hh_count + hl_count) / 8)
            elif lh_count >= 3 and ll_count >= 2:
                structure['trend'] = 'downtrend'
                structure['strength'] = min(0.9, (lh_count + ll_count) / 8)
            
            # Detect structure breaks
            if len(candles) >= 3:
                last_3_candles = candles[-3:]
                alternating = all(last_3_candles[i]['type'] != last_3_candles[i+1]['type'] 
                                for i in range(len(last_3_candles)-1))
                if alternating:
                    structure['structure_breaks'] = 1
        
        return structure
    
    def _identify_liquidity_zones(self, candles: List[Dict]) -> Dict:
        """Identify areas where liquidity might be trapped"""
        zones = {
            'high_liquidity': [],
            'low_liquidity': [],
            'liquidity_sweep_risk': 0.0
        }
        
        if len(candles) < 4:
            return zones
        
        # Find areas with multiple touches (liquidity zones)
        y_positions = [c['center_y'] for c in candles]
        
        # Group similar price levels
        tolerance = 10  # pixel tolerance
        grouped_levels = []
        
        for y in y_positions:
            added_to_group = False
            for group in grouped_levels:
                if any(abs(y - existing_y) <= tolerance for existing_y in group):
                    group.append(y)
                    added_to_group = True
                    break
            
            if not added_to_group:
                grouped_levels.append([y])
        
        # Identify high liquidity zones (3+ touches)
        for group in grouped_levels:
            if len(group) >= 3:
                avg_level = sum(group) / len(group)
                zones['high_liquidity'].append({
                    'level': avg_level,
                    'touches': len(group),
                    'strength': min(1.0, len(group) / 5)
                })
        
        # Calculate liquidity sweep risk
        if zones['high_liquidity']:
            last_candle = candles[-1]
            for zone in zones['high_liquidity']:
                distance = abs(last_candle['center_y'] - zone['level'])
                if distance < 15:  # Close to liquidity zone
                    zones['liquidity_sweep_risk'] = zone['strength'] * 0.8
        
        return zones
    
    def _detect_market_traps(self, candles: List[Dict]) -> Dict:
        """Detect bull traps, bear traps, and other manipulation patterns"""
        traps = {
            'bull_trap_risk': 0.0,
            'bear_trap_risk': 0.0,
            'fakeout_risk': 0.0,
            'trap_signals': []
        }
        
        if len(candles) < 4:
            return traps
        
        last_4 = candles[-4:]
        
        # Bull trap detection: Strong up move followed by immediate reversal
        if (len(last_4) >= 3 and
            last_4[-3]['type'] == 'bullish' and last_4[-3]['height'] > 20 and
            last_4[-2]['type'] == 'bearish' and 
            last_4[-1]['type'] == 'bearish'):
            
            traps['bull_trap_risk'] = 0.7
            traps['trap_signals'].append('bull_trap_pattern')
        
        # Bear trap detection: Strong down move followed by immediate reversal
        if (len(last_4) >= 3 and
            last_4[-3]['type'] == 'bearish' and last_4[-3]['height'] > 20 and
            last_4[-2]['type'] == 'bullish' and 
            last_4[-1]['type'] == 'bullish'):
            
            traps['bear_trap_risk'] = 0.7
            traps['trap_signals'].append('bear_trap_pattern')
        
        # Fakeout detection: Alternating pattern with large candles
        alternating_count = 0
        for i in range(len(last_4) - 1):
            if last_4[i]['type'] != last_4[i+1]['type']:
                alternating_count += 1
        
        if alternating_count >= 2:
            avg_height = sum(c['height'] for c in last_4) / len(last_4)
            if avg_height > 18:  # Large volatile candles
                traps['fakeout_risk'] = 0.6
                traps['trap_signals'].append('volatile_fakeout')
        
        return traps
    
    def _analyze_trend_fatigue(self, candles: List[Dict]) -> Dict:
        """Detect when trends are losing momentum"""
        fatigue = {
            'bullish_fatigue': 0.0,
            'bearish_fatigue': 0.0,
            'reversal_probability': 0.0
        }
        
        if len(candles) < 6:
            return fatigue
        
        last_6 = candles[-6:]
        
        # Count consecutive candles of same type
        bullish_streak = 0
        bearish_streak = 0
        
        for candle in reversed(last_6):
            if candle['type'] == 'bullish':
                bullish_streak += 1
                break
            elif candle['type'] == 'bearish':
                bearish_streak += 1
                break
        
        # Analyze size degradation (fatigue signal)
        if bullish_streak >= 3:
            recent_bullish = [c for c in last_6 if c['type'] == 'bullish']
            if len(recent_bullish) >= 3:
                heights = [c['height'] for c in recent_bullish[-3:]]
                if len(heights) >= 2 and heights[-1] < heights[0] * 0.8:
                    fatigue['bullish_fatigue'] = 0.7
        
        if bearish_streak >= 3:
            recent_bearish = [c for c in last_6 if c['type'] == 'bearish']
            if len(recent_bearish) >= 3:
                heights = [c['height'] for c in recent_bearish[-3:]]
                if len(heights) >= 2 and heights[-1] < heights[0] * 0.8:
                    fatigue['bearish_fatigue'] = 0.7
        
        # Calculate reversal probability
        fatigue['reversal_probability'] = max(fatigue['bullish_fatigue'], fatigue['bearish_fatigue'])
        
        return fatigue
    
    def _detect_manipulation(self, candles: List[Dict]) -> Dict:
        """Detect signs of market manipulation"""
        manipulation = {
            'spike_risk': 0.0,
            'stop_hunt_risk': 0.0,
            'wash_trading_risk': 0.0,
            'manipulation_signals': []
        }
        
        if len(candles) < 5:
            return manipulation
        
        last_5 = candles[-5:]
        
        # Spike detection: One very large candle followed by smaller ones
        heights = [c['height'] for c in last_5]
        max_height = max(heights)
        avg_height = sum(heights) / len(heights)
        
        if max_height > avg_height * 2.5:
            manipulation['spike_risk'] = 0.8
            manipulation['manipulation_signals'].append('price_spike')
        
        # Stop hunt detection: Large move followed by immediate reversal
        if len(last_5) >= 3:
            large_candle = None
            for i, candle in enumerate(last_5[:-2]):
                if candle['height'] > avg_height * 1.5:
                    large_candle = (i, candle)
                    break
            
            if large_candle:
                idx, candle = large_candle
                next_2 = last_5[idx+1:idx+3]
                if (len(next_2) >= 2 and 
                    all(c['type'] != candle['type'] for c in next_2)):
                    manipulation['stop_hunt_risk'] = 0.7
                    manipulation['manipulation_signals'].append('stop_hunt')
        
        return manipulation
    
    def _analyze_volatility(self, candles: List[Dict]) -> Dict:
        """Analyze volatility patterns"""
        volatility = {
            'current_volatility': 0.0,
            'volatility_trend': 'stable',
            'breakout_potential': 0.0
        }
        
        if len(candles) < 4:
            return volatility
        
        # Calculate volatility based on candle sizes
        heights = [c['height'] for c in candles]
        recent_heights = heights[-4:]
        
        current_vol = np.std(recent_heights) if len(recent_heights) > 1 else 0
        volatility['current_volatility'] = current_vol / 10  # Normalize
        
        # Volatility trend
        if len(heights) >= 6:
            early_vol = np.std(heights[-6:-3]) if len(heights[-6:-3]) > 1 else 0
            late_vol = np.std(heights[-3:]) if len(heights[-3:]) > 1 else 0
            
            if late_vol > early_vol * 1.3:
                volatility['volatility_trend'] = 'increasing'
                volatility['breakout_potential'] = 0.7
            elif late_vol < early_vol * 0.7:
                volatility['volatility_trend'] = 'decreasing'
        
        return volatility
    
    def _advanced_sr_analysis(self, candles: List[Dict]) -> Dict:
        """Advanced support and resistance analysis"""
        sr_analysis = {
            'support_levels': [],
            'resistance_levels': [],
            'key_level_proximity': 0.0,
            'sr_strength': 0.0
        }
        
        if len(candles) < 5:
            return sr_analysis
        
        # Extract price levels
        highs = [c['y'] for c in candles]
        lows = [c['y'] + c['height'] for c in candles]
        
        # Find potential support levels (areas where price bounced)
        for i in range(1, len(lows) - 1):
            if lows[i] <= lows[i-1] and lows[i] <= lows[i+1]:
                # Local low found
                touches = sum(1 for low in lows if abs(low - lows[i]) <= 8)
                if touches >= 2:
                    sr_analysis['support_levels'].append({
                        'level': lows[i],
                        'touches': touches,
                        'strength': min(1.0, touches / 4)
                    })
        
        # Find potential resistance levels
        for i in range(1, len(highs) - 1):
            if highs[i] >= highs[i-1] and highs[i] >= highs[i+1]:
                # Local high found
                touches = sum(1 for high in highs if abs(high - highs[i]) <= 8)
                if touches >= 2:
                    sr_analysis['resistance_levels'].append({
                        'level': highs[i],
                        'touches': touches,
                        'strength': min(1.0, touches / 4)
                    })
        
        # Check proximity to key levels
        current_price = candles[-1]['center_y']
        min_distance = float('inf')
        
        all_levels = sr_analysis['support_levels'] + sr_analysis['resistance_levels']
        for level_info in all_levels:
            distance = abs(current_price - level_info['level'])
            min_distance = min(min_distance, distance)
        
        if min_distance != float('inf') and min_distance <= 15:
            sr_analysis['key_level_proximity'] = 1.0 - (min_distance / 15)
        
        # Calculate overall S/R strength
        if all_levels:
            avg_strength = sum(level['strength'] for level in all_levels) / len(all_levels)
            sr_analysis['sr_strength'] = avg_strength
        
        return sr_analysis
    
    def _analyze_market_psychology(self, candles: List[Dict]) -> Dict:
        """Analyze market psychology and sentiment"""
        psychology = {
            'sentiment': 'neutral',
            'fear_level': 0.0,
            'greed_level': 0.0,
            'uncertainty_level': 0.0,
            'conviction_level': 0.0
        }
        
        if len(candles) < 4:
            return psychology
        
        last_4 = candles[-4:]
        
        # Calculate sentiment based on candle types and sizes
        bullish_count = sum(1 for c in last_4 if c['type'] == 'bullish')
        bearish_count = len(last_4) - bullish_count
        
        if bullish_count >= 3:
            psychology['sentiment'] = 'bullish'
            psychology['greed_level'] = bullish_count / len(last_4)
        elif bearish_count >= 3:
            psychology['sentiment'] = 'bearish'
            psychology['fear_level'] = bearish_count / len(last_4)
        
        # Uncertainty from alternating patterns
        alternations = sum(1 for i in range(len(last_4)-1) 
                          if last_4[i]['type'] != last_4[i+1]['type'])
        psychology['uncertainty_level'] = alternations / (len(last_4) - 1)
        
        # Conviction from candle sizes
        avg_height = sum(c['height'] for c in last_4) / len(last_4)
        if avg_height > 20:
            psychology['conviction_level'] = min(1.0, avg_height / 30)
        
        return psychology
    
    def _calculate_market_health(self, context: Dict) -> float:
        """Calculate overall market health score"""
        health_score = 0.5  # Base score
        
        # Positive factors
        if context['market_structure']['trend'] in ['uptrend', 'downtrend']:
            health_score += 0.1 * context['market_structure']['strength']
        
        if context['support_resistance']['sr_strength'] > 0.6:
            health_score += 0.1
        
        if context['volatility_profile']['volatility_trend'] == 'stable':
            health_score += 0.1
        
        # Negative factors
        health_score -= 0.2 * context['trap_detection']['fakeout_risk']
        health_score -= 0.15 * context['manipulation_signals']['spike_risk']
        health_score -= 0.1 * context['trend_fatigue']['reversal_probability']
        
        return max(0.0, min(1.0, health_score))
    
    def _default_context(self) -> Dict:
        """Return default context when analysis fails"""
        return {
            'market_structure': {'trend': 'unknown', 'strength': 0.0},
            'liquidity_zones': {'high_liquidity': [], 'liquidity_sweep_risk': 0.0},
            'trap_detection': {'bull_trap_risk': 0.0, 'bear_trap_risk': 0.0, 'fakeout_risk': 0.0},
            'trend_fatigue': {'reversal_probability': 0.0},
            'manipulation_signals': {'spike_risk': 0.0, 'manipulation_signals': []},
            'volatility_profile': {'current_volatility': 0.0, 'volatility_trend': 'unknown'},
            'support_resistance': {'support_levels': [], 'resistance_levels': [], 'key_level_proximity': 0.0},
            'market_psychology': {'sentiment': 'neutral', 'fear_level': 0.0, 'greed_level': 0.0},
            'market_health': 0.5
        }