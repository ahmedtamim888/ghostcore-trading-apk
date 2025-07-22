"""
🔮 COSMIC OMNI-BRAIN AI - STRATEGY ENGINE
Dynamic strategy generation with infinite adaptability
"""

from typing import Dict, List, Any, Optional, Tuple
import random
from datetime import datetime, timezone, timedelta

class DynamicStrategyEngine:
    """
    🧠 ULTIMATE STRATEGY GENERATOR
    Creates unique, adaptive strategies for each chart analysis
    """
    
    def __init__(self):
        self.name = "COSMIC STRATEGY ENGINE"
        self.version = "∞.UNBEATABLE"
        
        # Dynamic strategy templates
        self.strategy_templates = {
            'trap_fade_reversal': {
                'conditions': ['trap_detected', 'reversal_pattern'],
                'confidence_base': 0.85,
                'description': 'Fade false breakouts and ride reversals'
            },
            'momentum_flip': {
                'conditions': ['momentum_shift', 'volume_confirmation'],
                'confidence_base': 0.80,
                'description': 'Catch momentum changes at key levels'
            },
            'liquidity_exhaustion': {
                'conditions': ['liquidity_zones', 'exhaustion_signals'],
                'confidence_base': 0.75,
                'description': 'Trade exhaustion at liquidity zones'
            },
            'breakout_continuation': {
                'conditions': ['clean_breakout', 'trend_alignment'],
                'confidence_base': 0.90,
                'description': 'Ride continuation after strong breakouts'
            },
            'pattern_memory_logic': {
                'conditions': ['pattern_recognition', 'historical_success'],
                'confidence_base': 0.70,
                'description': 'Use pattern memory for high-probability setups'
            },
            'institutional_shadow': {
                'conditions': ['institutional_activity', 'large_orders'],
                'confidence_base': 0.95,
                'description': 'Follow institutional footprints'
            },
            'volatility_compression': {
                'conditions': ['low_volatility', 'compression_pattern'],
                'confidence_base': 0.78,
                'description': 'Trade expansion after compression'
            },
            'sentiment_divergence': {
                'conditions': ['sentiment_extreme', 'price_divergence'],
                'confidence_base': 0.82,
                'description': 'Contrarian plays at sentiment extremes'
            }
        }
        
        # Market condition weights
        self.condition_weights = {
            'trending': {'breakout_continuation': 1.5, 'momentum_flip': 1.2},
            'ranging': {'liquidity_exhaustion': 1.4, 'volatility_compression': 1.3},
            'volatile': {'trap_fade_reversal': 1.6, 'sentiment_divergence': 1.2},
            'institutional': {'institutional_shadow': 2.0, 'pattern_memory_logic': 1.1}
        }
        
        # Signal strength multipliers
        self.strength_multipliers = {
            'confluence_levels': {
                1: 1.0,
                2: 1.15,
                3: 1.30,
                4: 1.50,
                5: 1.75
            },
            'market_phase': {
                'markup': 1.2,
                'markdown': 1.2,
                'accumulation': 0.9,
                'distribution': 0.8
            }
        }
        
    def generate_dynamic_strategy(self, chart_data: Dict, market_context: Dict) -> Dict:
        """
        🚀 GENERATE UNIQUE ADAPTIVE STRATEGY
        Creates a fresh strategy for each analysis
        """
        
        print("🔮 COSMIC STRATEGY: Generating dynamic strategy...")
        
        # Extract key data
        candles = chart_data.get('candles', [])
        price_levels = chart_data.get('price_levels', {})
        patterns = chart_data.get('patterns', [])
        
        if not candles:
            return self._generate_no_trade_strategy()
        
        # 1. Analyze market conditions
        market_conditions = self._analyze_market_conditions(chart_data, market_context)
        
        # 2. Identify confluence factors
        confluence_factors = self._identify_confluence_factors(chart_data, market_context)
        
        # 3. Select optimal strategy template
        selected_strategy = self._select_optimal_strategy(market_conditions, confluence_factors)
        
        # 4. Customize strategy for current conditions
        customized_strategy = self._customize_strategy(
            selected_strategy, chart_data, market_context, confluence_factors
        )
        
        # 5. Calculate strategy confidence
        strategy_confidence = self._calculate_strategy_confidence(
            customized_strategy, confluence_factors, market_conditions
        )
        
        # 6. Generate entry/exit logic
        entry_logic = self._generate_entry_logic(customized_strategy, candles)
        
        # 7. Add risk management
        risk_management = self._generate_risk_management(customized_strategy, market_context)
        
        return {
            'strategy_name': customized_strategy['name'],
            'strategy_type': customized_strategy['type'],
            'description': customized_strategy['description'],
            'confidence': strategy_confidence,
            'market_conditions': market_conditions,
            'confluence_factors': confluence_factors,
            'entry_logic': entry_logic,
            'risk_management': risk_management,
            'expected_outcome': customized_strategy['expected_outcome'],
            'strategy_reasoning': customized_strategy['reasoning'],
            'unique_id': self._generate_strategy_id(),
            'timestamp': datetime.now().isoformat()
        }
    
    def _analyze_market_conditions(self, chart_data: Dict, market_context: Dict) -> Dict:
        """Analyze current market conditions for strategy selection"""
        
        trend = chart_data.get('trend', {})
        market_structure = chart_data.get('market_structure', {})
        sentiment = market_context.get('sentiment', {})
        market_phase = market_context.get('market_phase', {})
        
        conditions = {
            'trend_direction': trend.get('direction', 'unknown'),
            'trend_strength': trend.get('strength', 0),
            'market_structure': market_structure.get('structure', 'unknown'),
            'sentiment_label': sentiment.get('label', 'neutral'),
            'market_phase': market_phase.get('phase', 'unknown'),
            'volatility': market_phase.get('volatility', 0),
            'institutional_activity': market_context.get('institutional', {}).get('activity_level', 'low')
        }
        
        # Classify overall market state
        if conditions['trend_strength'] > 0.7:
            conditions['state'] = 'trending'
        elif conditions['volatility'] > 0.6:
            conditions['state'] = 'volatile'
        elif conditions['institutional_activity'] == 'high':
            conditions['state'] = 'institutional'
        else:
            conditions['state'] = 'ranging'
        
        return conditions
    
    def _identify_confluence_factors(self, chart_data: Dict, market_context: Dict) -> List[Dict]:
        """Identify factors that provide confluence for trading decision"""
        
        confluence_factors = []
        
        # Price level confluence
        price_levels = chart_data.get('price_levels', {})
        if price_levels.get('support') or price_levels.get('resistance'):
            confluence_factors.append({
                'type': 'price_levels',
                'strength': 0.8,
                'description': 'Strong support/resistance confluence'
            })
        
        # Pattern confluence
        patterns = chart_data.get('patterns', [])
        if patterns:
            confluence_factors.append({
                'type': 'pattern_recognition',
                'strength': 0.75,
                'description': f"Detected {len(patterns)} chart patterns"
            })
        
        # Trend confluence
        trend = chart_data.get('trend', {})
        if trend.get('strength', 0) > 0.6:
            confluence_factors.append({
                'type': 'trend_alignment',
                'strength': trend['strength'],
                'description': f"Strong {trend.get('direction', 'unknown')} trend"
            })
        
        # Market phase confluence
        market_phase = market_context.get('market_phase', {})
        if market_phase.get('confidence', 0) > 0.7:
            confluence_factors.append({
                'type': 'market_phase',
                'strength': market_phase['confidence'],
                'description': f"Clear {market_phase.get('phase', 'unknown')} phase"
            })
        
        # Sentiment confluence
        sentiment = market_context.get('sentiment', {})
        if sentiment.get('confidence', 0) > 0.7:
            confluence_factors.append({
                'type': 'sentiment_clarity',
                'strength': sentiment['confidence'],
                'description': f"Clear {sentiment.get('label', 'neutral')} sentiment"
            })
        
        # Trap/liquidity confluence
        traps = market_context.get('traps', {})
        if traps.get('detected'):
            confluence_factors.append({
                'type': 'trap_signals',
                'strength': 0.85,
                'description': 'Market trap patterns detected'
            })
        
        # Momentum confluence
        momentum = market_context.get('momentum', {})
        if momentum.get('shifts'):
            confluence_factors.append({
                'type': 'momentum_shifts',
                'strength': 0.7,
                'description': 'Clear momentum shift signals'
            })
        
        return confluence_factors
    
    def _select_optimal_strategy(self, market_conditions: Dict, confluence_factors: List[Dict]) -> Dict:
        """Select the best strategy template for current conditions"""
        
        market_state = market_conditions.get('state', 'ranging')
        
        # Get strategies weighted for current market state
        weighted_strategies = {}
        
        for strategy_name, template in self.strategy_templates.items():
            base_weight = template['confidence_base']
            
            # Apply market condition weights
            condition_multiplier = self.condition_weights.get(market_state, {}).get(strategy_name, 1.0)
            
            # Apply confluence bonus
            confluence_bonus = 0
            for factor in confluence_factors:
                if factor['type'] in template['conditions']:
                    confluence_bonus += factor['strength'] * 0.1
            
            final_weight = base_weight * condition_multiplier + confluence_bonus
            weighted_strategies[strategy_name] = final_weight
        
        # Select strategy with highest weight
        best_strategy = max(weighted_strategies, key=weighted_strategies.get)
        
        return {
            'name': best_strategy,
            'template': self.strategy_templates[best_strategy],
            'weight': weighted_strategies[best_strategy],
            'market_fit': weighted_strategies[best_strategy] / self.strategy_templates[best_strategy]['confidence_base']
        }
    
    def _customize_strategy(self, selected_strategy: Dict, chart_data: Dict, 
                          market_context: Dict, confluence_factors: List[Dict]) -> Dict:
        """Customize the selected strategy for current conditions"""
        
        strategy_name = selected_strategy['name']
        template = selected_strategy['template']
        
        # Generate unique strategy variant
        custom_name = f"{strategy_name.replace('_', ' ').title()} v{random.randint(1000, 9999)}"
        
        # Customize description based on current conditions
        market_conditions = self._analyze_market_conditions(chart_data, market_context)
        
        custom_description = self._generate_custom_description(
            template['description'], market_conditions, confluence_factors
        )
        
        # Generate strategy reasoning
        reasoning = self._generate_strategy_reasoning(
            strategy_name, market_conditions, confluence_factors
        )
        
        # Determine expected outcome
        expected_outcome = self._determine_expected_outcome(
            strategy_name, market_conditions, confluence_factors
        )
        
        return {
            'name': custom_name,
            'type': strategy_name,
            'description': custom_description,
            'reasoning': reasoning,
            'expected_outcome': expected_outcome,
            'confluence_count': len(confluence_factors),
            'market_fit': selected_strategy['market_fit']
        }
    
    def _generate_custom_description(self, base_description: str, 
                                   market_conditions: Dict, confluence_factors: List[Dict]) -> str:
        """Generate custom description for strategy"""
        
        market_state = market_conditions.get('state', 'unknown')
        trend_direction = market_conditions.get('trend_direction', 'unknown')
        
        custom_elements = []
        
        # Add market condition context
        if market_state == 'trending':
            custom_elements.append(f"leveraging {trend_direction} trend momentum")
        elif market_state == 'volatile':
            custom_elements.append("exploiting volatility patterns")
        elif market_state == 'institutional':
            custom_elements.append("following institutional footprints")
        else:
            custom_elements.append("targeting range-bound opportunities")
        
        # Add confluence context
        if len(confluence_factors) >= 3:
            custom_elements.append("with multiple confluence factors")
        elif len(confluence_factors) >= 2:
            custom_elements.append("with strong confluence")
        
        if custom_elements:
            return f"{base_description} - {', '.join(custom_elements)}"
        else:
            return base_description
    
    def _generate_strategy_reasoning(self, strategy_type: str, market_conditions: Dict, 
                                   confluence_factors: List[Dict]) -> str:
        """Generate reasoning for strategy selection"""
        
        reasons = []
        
        # Strategy-specific reasoning
        if strategy_type == 'trap_fade_reversal':
            reasons.append("Market showing trap patterns indicating false moves")
        elif strategy_type == 'momentum_flip':
            reasons.append("Momentum shift detected at key levels")
        elif strategy_type == 'liquidity_exhaustion':
            reasons.append("Liquidity zones showing exhaustion signals")
        elif strategy_type == 'breakout_continuation':
            reasons.append("Clean breakout with trend alignment")
        elif strategy_type == 'institutional_shadow':
            reasons.append("Institutional activity patterns detected")
        
        # Market condition reasoning
        market_state = market_conditions.get('state', 'unknown')
        if market_state == 'trending':
            reasons.append("Strong trending market supports directional plays")
        elif market_state == 'volatile':
            reasons.append("High volatility creates reversal opportunities")
        
        # Confluence reasoning
        confluence_count = len(confluence_factors)
        if confluence_count >= 3:
            reasons.append(f"Multiple confluence factors ({confluence_count}) increase probability")
        elif confluence_count >= 2:
            reasons.append("Strong confluence supports the setup")
        
        return ". ".join(reasons)
    
    def _determine_expected_outcome(self, strategy_type: str, market_conditions: Dict, 
                                  confluence_factors: List[Dict]) -> Dict:
        """Determine expected outcome for strategy"""
        
        # Base probabilities by strategy type
        base_probabilities = {
            'trap_fade_reversal': {'win_rate': 0.78, 'risk_reward': 1.5},
            'momentum_flip': {'win_rate': 0.75, 'risk_reward': 1.8},
            'liquidity_exhaustion': {'win_rate': 0.72, 'risk_reward': 1.6},
            'breakout_continuation': {'win_rate': 0.85, 'risk_reward': 2.0},
            'institutional_shadow': {'win_rate': 0.90, 'risk_reward': 2.5},
            'pattern_memory_logic': {'win_rate': 0.70, 'risk_reward': 1.4},
            'volatility_compression': {'win_rate': 0.73, 'risk_reward': 1.7},
            'sentiment_divergence': {'win_rate': 0.76, 'risk_reward': 1.9}
        }
        
        base_prob = base_probabilities.get(strategy_type, {'win_rate': 0.65, 'risk_reward': 1.3})
        
        # Adjust for confluence
        confluence_bonus = len(confluence_factors) * 0.05
        adjusted_win_rate = min(0.95, base_prob['win_rate'] + confluence_bonus)
        
        # Adjust for market conditions
        market_state = market_conditions.get('state', 'ranging')
        if market_state in ['trending', 'institutional']:
            adjusted_win_rate *= 1.1
        elif market_state == 'volatile':
            adjusted_win_rate *= 0.95
        
        adjusted_win_rate = min(0.95, adjusted_win_rate)
        
        return {
            'win_rate': adjusted_win_rate,
            'risk_reward_ratio': base_prob['risk_reward'],
            'expected_value': adjusted_win_rate * base_prob['risk_reward'] - (1 - adjusted_win_rate),
            'confidence_level': 'high' if adjusted_win_rate > 0.8 else 'medium' if adjusted_win_rate > 0.7 else 'low'
        }
    
    def _calculate_strategy_confidence(self, customized_strategy: Dict, 
                                     confluence_factors: List[Dict], market_conditions: Dict) -> float:
        """Calculate overall confidence in the strategy"""
        
        # Base confidence from strategy type
        base_confidence = 0.7
        
        # Market fit bonus
        market_fit = customized_strategy.get('market_fit', 1.0)
        market_bonus = (market_fit - 1.0) * 0.2
        
        # Confluence bonus
        confluence_count = len(confluence_factors)
        confluence_bonus = min(confluence_count * 0.05, 0.2)
        
        # Expected outcome bonus
        expected_outcome = customized_strategy.get('expected_outcome', {})
        outcome_bonus = (expected_outcome.get('win_rate', 0.7) - 0.7) * 0.3
        
        # Trend strength bonus
        trend_strength = market_conditions.get('trend_strength', 0)
        trend_bonus = trend_strength * 0.1
        
        total_confidence = base_confidence + market_bonus + confluence_bonus + outcome_bonus + trend_bonus
        
        return min(0.98, max(0.3, total_confidence))
    
    def _generate_entry_logic(self, customized_strategy: Dict, candles: List[Dict]) -> Dict:
        """Generate specific entry logic for the strategy"""
        
        strategy_type = customized_strategy['type']
        
        if not candles:
            return {'signal': 'NO TRADE', 'reason': 'Insufficient data'}
        
        last_candle = candles[-1]
        recent_candles = candles[-3:] if len(candles) >= 3 else candles
        
        # Strategy-specific entry logic
        if strategy_type == 'trap_fade_reversal':
            return self._trap_fade_entry_logic(recent_candles)
        elif strategy_type == 'momentum_flip':
            return self._momentum_flip_entry_logic(recent_candles)
        elif strategy_type == 'breakout_continuation':
            return self._breakout_continuation_entry_logic(recent_candles)
        elif strategy_type == 'liquidity_exhaustion':
            return self._liquidity_exhaustion_entry_logic(recent_candles)
        else:
            return self._generic_entry_logic(recent_candles)
    
    def _trap_fade_entry_logic(self, candles: List[Dict]) -> Dict:
        """Entry logic for trap fade reversal strategy"""
        
        if len(candles) < 2:
            return {'signal': 'NO TRADE', 'reason': 'Insufficient candles for trap analysis'}
        
        last_candle = candles[-1]
        prev_candle = candles[-2]
        
        # Look for reversal after potential trap
        if (prev_candle['direction'] != last_candle['direction'] and 
            last_candle['strength'] > 0.6):
            
            signal = 'CALL' if last_candle['direction'] == 'bullish' else 'PUT'
            return {
                'signal': signal,
                'reason': f'Trap fade reversal - {last_candle["direction"]} reversal after potential trap',
                'entry_candle': last_candle['id'],
                'confidence_boost': 0.1
            }
        
        return {'signal': 'NO TRADE', 'reason': 'No clear trap reversal pattern'}
    
    def _momentum_flip_entry_logic(self, candles: List[Dict]) -> Dict:
        """Entry logic for momentum flip strategy"""
        
        if len(candles) < 3:
            return {'signal': 'NO TRADE', 'reason': 'Insufficient candles for momentum analysis'}
        
        # Check for momentum change
        recent_strengths = [c['strength'] for c in candles]
        if recent_strengths[-1] > recent_strengths[-2] * 1.2:
            
            last_candle = candles[-1]
            signal = 'CALL' if last_candle['direction'] == 'bullish' else 'PUT'
            
            return {
                'signal': signal,
                'reason': f'Momentum flip detected - {last_candle["direction"]} strength increase',
                'entry_candle': last_candle['id'],
                'confidence_boost': 0.15
            }
        
        return {'signal': 'NO TRADE', 'reason': 'No clear momentum flip'}
    
    def _breakout_continuation_entry_logic(self, candles: List[Dict]) -> Dict:
        """Entry logic for breakout continuation strategy"""
        
        last_candle = candles[-1]
        
        # Look for strong breakout candle
        if last_candle['strength'] > 0.7 and last_candle['pattern'] in ['marubozu', 'long_body']:
            
            signal = 'CALL' if last_candle['direction'] == 'bullish' else 'PUT'
            
            return {
                'signal': signal,
                'reason': f'Strong {last_candle["direction"]} breakout continuation',
                'entry_candle': last_candle['id'],
                'confidence_boost': 0.2
            }
        
        return {'signal': 'NO TRADE', 'reason': 'No strong breakout pattern detected'}
    
    def _liquidity_exhaustion_entry_logic(self, candles: List[Dict]) -> Dict:
        """Entry logic for liquidity exhaustion strategy"""
        
        last_candle = candles[-1]
        
        # Look for exhaustion patterns (long wicks)
        if (last_candle['ratios']['upper_wick'] > 0.4 or 
            last_candle['ratios']['lower_wick'] > 0.4):
            
            # Determine direction based on wick
            if last_candle['ratios']['upper_wick'] > last_candle['ratios']['lower_wick']:
                signal = 'PUT'  # Upper wick rejection
                reason = 'Upper wick rejection at resistance'
            else:
                signal = 'CALL'  # Lower wick rejection
                reason = 'Lower wick rejection at support'
            
            return {
                'signal': signal,
                'reason': reason,
                'entry_candle': last_candle['id'],
                'confidence_boost': 0.1
            }
        
        return {'signal': 'NO TRADE', 'reason': 'No clear exhaustion signals'}
    
    def _generic_entry_logic(self, candles: List[Dict]) -> Dict:
        """Generic entry logic for other strategies"""
        
        last_candle = candles[-1]
        
        # Simple momentum-based logic
        if last_candle['strength'] > 0.6:
            signal = 'CALL' if last_candle['direction'] == 'bullish' else 'PUT'
            
            return {
                'signal': signal,
                'reason': f'Strong {last_candle["direction"]} momentum',
                'entry_candle': last_candle['id'],
                'confidence_boost': 0.05
            }
        
        return {'signal': 'NO TRADE', 'reason': 'Insufficient signal strength'}
    
    def _generate_risk_management(self, customized_strategy: Dict, market_context: Dict) -> Dict:
        """Generate risk management parameters"""
        
        sentiment = market_context.get('sentiment', {})
        volatility = market_context.get('market_phase', {}).get('volatility', 0.5)
        
        # Base risk parameters
        base_risk = 2.0  # 2% risk per trade
        
        # Adjust for volatility
        if volatility > 0.7:
            risk_multiplier = 0.8  # Reduce risk in high volatility
        elif volatility < 0.3:
            risk_multiplier = 1.2  # Increase risk in low volatility
        else:
            risk_multiplier = 1.0
        
        # Adjust for confidence
        confidence = customized_strategy.get('confidence', 0.7)
        confidence_multiplier = 0.8 + (confidence * 0.4)  # 0.8 to 1.2 range
        
        adjusted_risk = base_risk * risk_multiplier * confidence_multiplier
        
        return {
            'risk_per_trade': f"{adjusted_risk:.1f}%",
            'stop_loss': "Next candle close against position",
            'take_profit': "1.5-2.0x risk reward ratio",
            'position_sizing': "Based on account risk tolerance",
            'max_trades_per_day': 3,
            'avoid_conditions': [
                "Major news events",
                "Market close proximity",
                "Extreme volatility spikes"
            ]
        }
    
    def _generate_strategy_id(self) -> str:
        """Generate unique strategy ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_suffix = random.randint(1000, 9999)
        return f"COSMIC_STRATEGY_{timestamp}_{random_suffix}"
    
    def _generate_no_trade_strategy(self) -> Dict:
        """Generate no-trade strategy when conditions are unclear"""
        
        return {
            'strategy_name': 'NO TRADE - Market Unclear',
            'strategy_type': 'no_trade',
            'description': 'Market conditions do not meet criteria for high-probability trades',
            'confidence': 0.0,
            'market_conditions': {'state': 'unclear'},
            'confluence_factors': [],
            'entry_logic': {'signal': 'NO TRADE', 'reason': 'Insufficient market clarity'},
            'risk_management': {'recommendation': 'Wait for clearer setup'},
            'expected_outcome': {'win_rate': 0.0, 'risk_reward_ratio': 0.0},
            'strategy_reasoning': 'No clear strategy applicable to current market conditions',
            'unique_id': self._generate_strategy_id(),
            'timestamp': datetime.now().isoformat()
        }