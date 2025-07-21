import random
import numpy as np
from typing import List, Dict, Tuple, Optional
import logging
from datetime import datetime

class DynamicStrategyEngine:
    """Dynamic strategy generation - creates fresh logic for every trade like a 100-billion-year AI"""
    
    def __init__(self):
        self.name = "COSMIC STRATEGY ENGINE"
        self.logger = logging.getLogger(__name__)
        
        # Strategy components that can be dynamically combined
        self.pattern_strategies = {
            'trap_fade': self._trap_fade_strategy,
            'momentum_flip': self._momentum_flip_strategy,
            'liquidity_exhaustion': self._liquidity_exhaustion_strategy,
            'breakout_continuation': self._breakout_continuation_strategy,
            'pattern_memory': self._pattern_memory_strategy,
            'volatility_expansion': self._volatility_expansion_strategy,
            'reversal_convergence': self._reversal_convergence_strategy,
            'smart_money_trace': self._smart_money_trace_strategy
        }
        
        # Dynamic weight adjustments based on market conditions
        self.adaptive_weights = {
            'trend_following': 1.0,
            'mean_reversion': 1.0,
            'breakout': 1.0,
            'pattern_recognition': 1.0,
            'sentiment_analysis': 1.0
        }
        
    def generate_signal(self, candles: List[Dict], market_context: Dict, image_shape: Tuple) -> Dict:
        """Generate completely dynamic trading signal with unique strategy"""
        try:
            if len(candles) < 3:
                return self._no_signal_response("Insufficient data")
            
            # Step 1: Dynamically select strategy components
            active_strategies = self._select_dynamic_strategies(candles, market_context)
            
            # Step 2: Generate multiple signal hypotheses
            signal_hypotheses = []
            for strategy_name, strategy_func in active_strategies.items():
                hypothesis = strategy_func(candles, market_context)
                if hypothesis:
                    hypothesis['strategy_name'] = strategy_name
                    signal_hypotheses.append(hypothesis)
            
            # Step 3: Apply meta-strategy fusion
            final_signal = self._fuse_strategies(signal_hypotheses, market_context)
            
            # Step 4: Apply dynamic risk filters
            filtered_signal = self._apply_risk_filters(final_signal, candles, market_context)
            
            # Step 5: Calculate dynamic confidence
            confidence = self._calculate_dynamic_confidence(filtered_signal, market_context, candles)
            
            # Step 6: Generate unique reasoning
            reasoning = self._generate_reasoning(filtered_signal, active_strategies, market_context)
            
            return {
                'signal': filtered_signal['direction'],
                'confidence': confidence,
                'strategy': filtered_signal['primary_strategy'],
                'reasoning': reasoning,
                'market_adaptation': self._get_market_adaptation(market_context),
                'risk_level': filtered_signal.get('risk_level', 'medium'),
                'entry_logic': filtered_signal.get('entry_logic', 'standard'),
                'signal_strength': filtered_signal.get('strength', 0.5)
            }
            
        except Exception as e:
            self.logger.error(f"Strategy generation failed: {e}")
            return self._no_signal_response(f"Analysis error: {str(e)}")
    
    def _select_dynamic_strategies(self, candles: List[Dict], market_context: Dict) -> Dict:
        """Dynamically select which strategies to activate based on conditions"""
        active_strategies = {}
        
        # Base conditions
        volatility = market_context['volatility_profile']['current_volatility']
        trend_strength = market_context['market_structure']['strength']
        trap_risk = max(
            market_context['trap_detection']['bull_trap_risk'],
            market_context['trap_detection']['bear_trap_risk']
        )
        
        # Always include core strategies with dynamic probability
        core_strategies = ['trap_fade', 'momentum_flip', 'pattern_memory']
        for strategy in core_strategies:
            if random.random() > 0.3:  # 70% chance for core strategies
                active_strategies[strategy] = self.pattern_strategies[strategy]
        
        # Conditional strategy activation
        if volatility > 0.6:
            active_strategies['volatility_expansion'] = self.pattern_strategies['volatility_expansion']
        
        if trend_strength > 0.7:
            active_strategies['breakout_continuation'] = self.pattern_strategies['breakout_continuation']
        
        if trap_risk > 0.5:
            active_strategies['trap_fade'] = self.pattern_strategies['trap_fade']
        
        if market_context['market_health'] > 0.7:
            active_strategies['smart_money_trace'] = self.pattern_strategies['smart_money_trace']
        
        # Liquidity-based activation
        if market_context['liquidity_zones']['liquidity_sweep_risk'] > 0.6:
            active_strategies['liquidity_exhaustion'] = self.pattern_strategies['liquidity_exhaustion']
        
        # Reversal conditions
        reversal_prob = market_context['trend_fatigue']['reversal_probability']
        if reversal_prob > 0.6:
            active_strategies['reversal_convergence'] = self.pattern_strategies['reversal_convergence']
        
        return active_strategies
    
    def _trap_fade_strategy(self, candles: List[Dict], market_context: Dict) -> Optional[Dict]:
        """Identify and fade market traps"""
        trap_signals = market_context['trap_detection']
        
        signal_strength = 0.0
        direction = None
        
        # Bull trap fade
        if trap_signals['bull_trap_risk'] > 0.6:
            direction = 'PUT'
            signal_strength = trap_signals['bull_trap_risk'] * 0.9
        
        # Bear trap fade
        elif trap_signals['bear_trap_risk'] > 0.6:
            direction = 'CALL'
            signal_strength = trap_signals['bear_trap_risk'] * 0.9
        
        # Fakeout fade
        elif trap_signals['fakeout_risk'] > 0.5:
            # Determine fade direction based on last candle
            last_candle = candles[-1]
            direction = 'PUT' if last_candle['type'] == 'bullish' else 'CALL'
            signal_strength = trap_signals['fakeout_risk'] * 0.8
        
        if direction and signal_strength > 0.5:
            return {
                'direction': direction,
                'strength': signal_strength,
                'risk_level': 'medium',
                'entry_logic': 'trap_fade',
                'primary_strategy': 'Trap Fade Reversal'
            }
        
        return None
    
    def _momentum_flip_strategy(self, candles: List[Dict], market_context: Dict) -> Optional[Dict]:
        """Detect momentum shifts and generate signals"""
        if len(candles) < 4:
            return None
        
        last_4 = candles[-4:]
        
        # Calculate momentum score
        bullish_momentum = sum(1 for c in last_4 if c['type'] == 'bullish')
        bearish_momentum = len(last_4) - bullish_momentum
        
        # Size-weighted momentum
        bullish_size = sum(c['height'] for c in last_4 if c['type'] == 'bullish')
        bearish_size = sum(c['height'] for c in last_4 if c['type'] == 'bearish')
        
        total_size = bullish_size + bearish_size
        if total_size == 0:
            return None
        
        bullish_weight = bullish_size / total_size
        bearish_weight = bearish_size / total_size
        
        # Momentum flip detection
        signal_strength = 0.0
        direction = None
        
        # Strong bullish momentum
        if bullish_weight > 0.65 and bullish_momentum >= 3:
            direction = 'CALL'
            signal_strength = bullish_weight * 0.85
        
        # Strong bearish momentum
        elif bearish_weight > 0.65 and bearish_momentum >= 3:
            direction = 'PUT'
            signal_strength = bearish_weight * 0.85
        
        # Momentum divergence (size vs count)
        elif abs(bullish_weight - (bullish_momentum / len(last_4))) > 0.3:
            if bullish_weight > 0.5:
                direction = 'CALL'
                signal_strength = 0.7
            else:
                direction = 'PUT'
                signal_strength = 0.7
        
        if direction and signal_strength > 0.6:
            return {
                'direction': direction,
                'strength': signal_strength,
                'risk_level': 'low',
                'entry_logic': 'momentum_follow',
                'primary_strategy': 'Momentum Flip'
            }
        
        return None
    
    def _liquidity_exhaustion_strategy(self, candles: List[Dict], market_context: Dict) -> Optional[Dict]:
        """Detect liquidity exhaustion and reversal points"""
        liquidity = market_context['liquidity_zones']
        
        if not liquidity['high_liquidity'] or liquidity['liquidity_sweep_risk'] < 0.5:
            return None
        
        last_candle = candles[-1]
        
        # Find closest liquidity zone
        closest_zone = None
        min_distance = float('inf')
        
        for zone in liquidity['high_liquidity']:
            distance = abs(last_candle['center_y'] - zone['level'])
            if distance < min_distance:
                min_distance = distance
                closest_zone = zone
        
        if not closest_zone or min_distance > 20:
            return None
        
        # Determine exhaustion direction
        direction = None
        signal_strength = closest_zone['strength'] * liquidity['liquidity_sweep_risk']
        
        # Price approaching from below (exhaustion up)
        if last_candle['center_y'] > closest_zone['level']:
            direction = 'PUT'
        # Price approaching from above (exhaustion down)
        else:
            direction = 'CALL'
        
        # Boost strength if recent volatility is high
        if market_context['volatility_profile']['current_volatility'] > 0.5:
            signal_strength *= 1.2
        
        if signal_strength > 0.6:
            return {
                'direction': direction,
                'strength': min(signal_strength, 1.0),
                'risk_level': 'high',
                'entry_logic': 'liquidity_exhaustion',
                'primary_strategy': 'Liquidity Exhaustion'
            }
        
        return None
    
    def _breakout_continuation_strategy(self, candles: List[Dict], market_context: Dict) -> Optional[Dict]:
        """Identify breakout and continuation patterns"""
        if len(candles) < 5:
            return None
        
        structure = market_context['market_structure']
        volatility = market_context['volatility_profile']
        
        # Need strong trend and increasing volatility for breakouts
        if structure['strength'] < 0.6 or volatility['breakout_potential'] < 0.6:
            return None
        
        last_3 = candles[-3:]
        
        # Check for breakout pattern
        avg_height = sum(c['height'] for c in last_3) / len(last_3)
        
        # Large candle followed by continuation
        breakout_detected = False
        direction = None
        
        for i, candle in enumerate(last_3):
            if candle['height'] > avg_height * 1.4:  # Large candle
                breakout_detected = True
                direction = 'CALL' if candle['type'] == 'bullish' else 'PUT'
                break
        
        if not breakout_detected:
            return None
        
        # Confirm with trend direction
        if structure['trend'] == 'uptrend' and direction == 'CALL':
            signal_strength = structure['strength'] * 0.9
        elif structure['trend'] == 'downtrend' and direction == 'PUT':
            signal_strength = structure['strength'] * 0.9
        else:
            signal_strength = 0.5  # Counter-trend breakout
        
        if signal_strength > 0.6:
            return {
                'direction': direction,
                'strength': signal_strength,
                'risk_level': 'medium',
                'entry_logic': 'breakout_follow',
                'primary_strategy': 'Breakout Continuation'
            }
        
        return None
    
    def _pattern_memory_strategy(self, candles: List[Dict], market_context: Dict) -> Optional[Dict]:
        """Use pattern memory and recognition"""
        if len(candles) < 6:
            return None
        
        last_6 = candles[-6:]
        
        # Detect specific patterns
        patterns_detected = []
        
        # Three soldiers pattern
        if (len(last_6) >= 3 and
            all(c['type'] == 'bullish' for c in last_6[-3:]) and
            all(last_6[-3:][i]['height'] >= last_6[-3:][i-1]['height'] * 0.8 
                for i in range(1, 3))):
            patterns_detected.append(('three_soldiers', 'CALL', 0.8))
        
        # Three crows pattern
        elif (len(last_6) >= 3 and
              all(c['type'] == 'bearish' for c in last_6[-3:]) and
              all(last_6[-3:][i]['height'] >= last_6[-3:][i-1]['height'] * 0.8 
                  for i in range(1, 3))):
            patterns_detected.append(('three_crows', 'PUT', 0.8))
        
        # Hammer pattern
        last_candle = last_6[-1]
        if (last_candle['body_ratio'] < 0.3 and 
            last_candle['height'] > 20):
            
            # Determine hammer direction
            if len(last_6) >= 2:
                prev_candle = last_6[-2]
                if prev_candle['type'] == 'bearish':
                    patterns_detected.append(('hammer_reversal', 'CALL', 0.7))
                else:
                    patterns_detected.append(('hanging_man', 'PUT', 0.6))
        
        # Select best pattern
        if patterns_detected:
            best_pattern = max(patterns_detected, key=lambda x: x[2])
            pattern_name, direction, strength = best_pattern
            
            return {
                'direction': direction,
                'strength': strength,
                'risk_level': 'low',
                'entry_logic': 'pattern_recognition',
                'primary_strategy': f'Pattern Memory: {pattern_name.replace("_", " ").title()}'
            }
        
        return None
    
    def _volatility_expansion_strategy(self, candles: List[Dict], market_context: Dict) -> Optional[Dict]:
        """Trade volatility expansion phases"""
        volatility = market_context['volatility_profile']
        
        if volatility['volatility_trend'] != 'increasing' or volatility['current_volatility'] < 0.5:
            return None
        
        last_candle = candles[-1]
        
        # High volatility + large candle = continuation signal
        if last_candle['height'] > 25:
            direction = 'CALL' if last_candle['type'] == 'bullish' else 'PUT'
            signal_strength = min(1.0, volatility['current_volatility'] * 1.2)
            
            return {
                'direction': direction,
                'strength': signal_strength,
                'risk_level': 'high',
                'entry_logic': 'volatility_expansion',
                'primary_strategy': 'Volatility Expansion'
            }
        
        return None
    
    def _reversal_convergence_strategy(self, candles: List[Dict], market_context: Dict) -> Optional[Dict]:
        """Multi-factor reversal detection"""
        fatigue = market_context['trend_fatigue']
        sr_analysis = market_context['support_resistance']
        
        reversal_signals = 0
        
        # Trend fatigue signal
        if fatigue['reversal_probability'] > 0.6:
            reversal_signals += 1
        
        # Key level proximity
        if sr_analysis['key_level_proximity'] > 0.7:
            reversal_signals += 1
        
        # Market psychology (extreme sentiment)
        psychology = market_context['market_psychology']
        if psychology['fear_level'] > 0.8 or psychology['greed_level'] > 0.8:
            reversal_signals += 1
        
        # Need at least 2 reversal signals
        if reversal_signals < 2:
            return None
        
        # Determine reversal direction
        last_candle = candles[-1]
        direction = 'PUT' if last_candle['type'] == 'bullish' else 'CALL'
        
        signal_strength = min(1.0, reversal_signals / 3 * 0.9)
        
        return {
            'direction': direction,
            'strength': signal_strength,
            'risk_level': 'medium',
            'entry_logic': 'reversal_convergence',
            'primary_strategy': 'Reversal Convergence'
        }
    
    def _smart_money_trace_strategy(self, candles: List[Dict], market_context: Dict) -> Optional[Dict]:
        """Follow smart money movements"""
        manipulation = market_context['manipulation_signals']
        
        # Look for stop hunt followed by real move
        if manipulation['stop_hunt_risk'] > 0.6 and len(candles) >= 3:
            last_3 = candles[-3:]
            
            # Find the manipulation candle
            manipulation_candle = None
            for candle in last_3:
                if candle['height'] > 25:  # Large move
                    manipulation_candle = candle
                    break
            
            if manipulation_candle:
                # Smart money moves opposite to manipulation
                direction = 'PUT' if manipulation_candle['type'] == 'bullish' else 'CALL'
                signal_strength = manipulation['stop_hunt_risk'] * 0.8
                
                return {
                    'direction': direction,
                    'strength': signal_strength,
                    'risk_level': 'medium',
                    'entry_logic': 'smart_money_follow',
                    'primary_strategy': 'Smart Money Trace'
                }
        
        return None
    
    def _fuse_strategies(self, hypotheses: List[Dict], market_context: Dict) -> Dict:
        """Fuse multiple strategy signals into one decision"""
        if not hypotheses:
            return {'direction': 'NO SIGNAL', 'strength': 0.0, 'primary_strategy': 'None'}
        
        # Weight strategies by confidence and market conditions
        weighted_signals = []
        
        for hypothesis in hypotheses:
            weight = self._calculate_strategy_weight(hypothesis, market_context)
            weighted_signals.append({
                'direction': hypothesis['direction'],
                'weight': weight,
                'strength': hypothesis['strength'],
                'strategy': hypothesis['primary_strategy']
            })
        
        # Aggregate signals
        call_weight = sum(s['weight'] * s['strength'] for s in weighted_signals if s['direction'] == 'CALL')
        put_weight = sum(s['weight'] * s['strength'] for s in weighted_signals if s['direction'] == 'PUT')
        
        if call_weight > put_weight and call_weight > 0.5:
            primary_strategy = max([s for s in weighted_signals if s['direction'] == 'CALL'], 
                                 key=lambda x: x['weight'] * x['strength'])['strategy']
            return {
                'direction': 'CALL',
                'strength': min(1.0, call_weight),
                'primary_strategy': primary_strategy,
                'risk_level': self._assess_risk_level(weighted_signals)
            }
        
        elif put_weight > call_weight and put_weight > 0.5:
            primary_strategy = max([s for s in weighted_signals if s['direction'] == 'PUT'], 
                                 key=lambda x: x['weight'] * x['strength'])['strategy']
            return {
                'direction': 'PUT',
                'strength': min(1.0, put_weight),
                'primary_strategy': primary_strategy,
                'risk_level': self._assess_risk_level(weighted_signals)
            }
        
        return {'direction': 'NO SIGNAL', 'strength': 0.0, 'primary_strategy': 'Conflicting Signals'}
    
    def _calculate_strategy_weight(self, hypothesis: Dict, market_context: Dict) -> float:
        """Calculate dynamic weight for each strategy"""
        base_weight = 1.0
        
        # Adjust based on market health
        health_multiplier = 0.5 + (market_context['market_health'] * 0.5)
        
        # Strategy-specific adjustments
        if 'Trap Fade' in hypothesis['primary_strategy']:
            # Higher weight in manipulated markets
            trap_risk = max(
                market_context['trap_detection']['bull_trap_risk'],
                market_context['trap_detection']['bear_trap_risk']
            )
            base_weight *= (1.0 + trap_risk)
        
        elif 'Momentum' in hypothesis['primary_strategy']:
            # Higher weight in trending markets
            trend_strength = market_context['market_structure']['strength']
            base_weight *= (1.0 + trend_strength * 0.5)
        
        elif 'Pattern Memory' in hypothesis['primary_strategy']:
            # Stable weight regardless of conditions
            base_weight *= 1.0
        
        return base_weight * health_multiplier
    
    def _assess_risk_level(self, weighted_signals: List[Dict]) -> str:
        """Assess overall risk level of the trade"""
        avg_strength = sum(s['strength'] for s in weighted_signals) / len(weighted_signals)
        
        if avg_strength > 0.8:
            return 'low'
        elif avg_strength > 0.6:
            return 'medium'
        else:
            return 'high'
    
    def _apply_risk_filters(self, signal: Dict, candles: List[Dict], market_context: Dict) -> Dict:
        """Apply dynamic risk management filters"""
        if signal['direction'] == 'NO SIGNAL':
            return signal
        
        # Market health filter
        if market_context['market_health'] < 0.3:
            signal['strength'] *= 0.7  # Reduce confidence in unhealthy markets
        
        # Volatility filter
        volatility = market_context['volatility_profile']['current_volatility']
        if volatility > 0.8:  # Extreme volatility
            signal['strength'] *= 0.8
            signal['risk_level'] = 'high'
        
        # Manipulation filter
        manipulation_risk = market_context['manipulation_signals']['spike_risk']
        if manipulation_risk > 0.7:
            signal['strength'] *= 0.6
        
        return signal
    
    def _calculate_dynamic_confidence(self, signal: Dict, market_context: Dict, candles: List[Dict]) -> float:
        """Calculate dynamic confidence score"""
        if signal['direction'] == 'NO SIGNAL':
            return 0.0
        
        base_confidence = signal['strength'] * 100
        
        # Adjust based on data quality
        if len(candles) >= 8:
            base_confidence *= 1.1  # More data = higher confidence
        elif len(candles) < 4:
            base_confidence *= 0.8  # Less data = lower confidence
        
        # Market structure adjustment
        structure_strength = market_context['market_structure']['strength']
        base_confidence *= (0.8 + structure_strength * 0.4)
        
        # Support/resistance proximity bonus
        sr_proximity = market_context['support_resistance']['key_level_proximity']
        if sr_proximity > 0.7:
            base_confidence *= 1.15
        
        return min(100.0, max(0.0, base_confidence))
    
    def _generate_reasoning(self, signal: Dict, active_strategies: Dict, market_context: Dict) -> str:
        """Generate human-readable reasoning for the signal"""
        if signal['direction'] == 'NO SIGNAL':
            return "Insufficient signal strength or conflicting market conditions detected."
        
        reasoning_parts = []
        
        # Primary strategy reasoning
        strategy = signal['primary_strategy']
        reasoning_parts.append(f"Primary Strategy: {strategy}")
        
        # Market condition reasoning
        market_health = market_context['market_health']
        if market_health > 0.7:
            reasoning_parts.append("Market showing healthy structure")
        elif market_health < 0.4:
            reasoning_parts.append("Caution: Market showing stress signals")
        
        # Specific condition reasoning
        if 'Trap Fade' in strategy:
            reasoning_parts.append("Detected market manipulation - fading the trap")
        elif 'Momentum' in strategy:
            reasoning_parts.append("Strong momentum alignment detected")
        elif 'Liquidity' in strategy:
            reasoning_parts.append("Liquidity exhaustion at key level")
        elif 'Pattern' in strategy:
            reasoning_parts.append("Classic pattern recognition confirmed")
        
        # Risk assessment
        risk_level = signal.get('risk_level', 'medium')
        reasoning_parts.append(f"Risk Level: {risk_level.title()}")
        
        return " | ".join(reasoning_parts)
    
    def _get_market_adaptation(self, market_context: Dict) -> str:
        """Describe how the AI adapted to current market conditions"""
        adaptations = []
        
        if market_context['volatility_profile']['current_volatility'] > 0.6:
            adaptations.append("High volatility adaptation")
        
        if market_context['trap_detection']['fakeout_risk'] > 0.5:
            adaptations.append("Anti-manipulation mode")
        
        if market_context['trend_fatigue']['reversal_probability'] > 0.6:
            adaptations.append("Reversal detection mode")
        
        if not adaptations:
            adaptations.append("Standard market conditions")
        
        return " + ".join(adaptations)
    
    def _no_signal_response(self, reason: str) -> Dict:
        """Return no signal response"""
        return {
            'signal': 'NO SIGNAL',
            'confidence': 0.0,
            'strategy': 'No Strategy',
            'reasoning': reason,
            'market_adaptation': 'Insufficient data',
            'risk_level': 'none',
            'entry_logic': 'none',
            'signal_strength': 0.0
        }