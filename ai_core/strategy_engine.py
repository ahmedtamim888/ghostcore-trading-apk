"""
COSMIC OMNI-BRAIN AI v∞.UNBEATABLE
Dynamic Strategy Engine
Adaptive Logic Generation & Execution
"""

import random
import math
from datetime import datetime, timezone, timedelta

class DynamicStrategyEngine:
    def __init__(self):
        self.strategy_components = {
            'trend_following': {
                'momentum_continuation': {'strength': 0.85, 'risk': 0.3},
                'trend_pullback': {'strength': 0.75, 'risk': 0.4},
                'breakout_continuation': {'strength': 0.8, 'risk': 0.35}
            },
            'counter_trend': {
                'exhaustion_reversal': {'strength': 0.9, 'risk': 0.5},
                'oversold_bounce': {'strength': 0.8, 'risk': 0.45},
                'trap_fade': {'strength': 0.85, 'risk': 0.4}
            },
            'pattern_based': {
                'candlestick_reversal': {'strength': 0.8, 'risk': 0.4},
                'support_resistance': {'strength': 0.75, 'risk': 0.35},
                'pattern_completion': {'strength': 0.8, 'risk': 0.3}
            },
            'liquidity_based': {
                'liquidity_grab_fade': {'strength': 0.9, 'risk': 0.4},
                'stop_hunt_reversal': {'strength': 0.85, 'risk': 0.45},
                'absorption_play': {'strength': 0.8, 'risk': 0.35}
            },
            'time_based': {
                'session_open_momentum': {'strength': 0.75, 'risk': 0.4},
                'lunch_hour_reversal': {'strength': 0.7, 'risk': 0.5},
                'close_positioning': {'strength': 0.8, 'risk': 0.3}
            }
        }
        
        self.market_conditions = {
            'trending': ['momentum_continuation', 'trend_pullback', 'breakout_continuation'],
            'ranging': ['support_resistance', 'trap_fade', 'liquidity_grab_fade'],
            'volatile': ['exhaustion_reversal', 'stop_hunt_reversal', 'pattern_completion'],
            'quiet': ['absorption_play', 'session_open_momentum', 'candlestick_reversal']
        }

    def generate_dynamic_strategy(self, chart_data, market_context, current_time):
        """Generate a unique strategy for this specific chart"""
        
        # Extract key components
        structure = chart_data['structure']
        psychology = market_context['dominant_emotion']
        institutional = market_context['institutional_activity']
        traps = market_context.get('traps', [])
        
        # Build unique strategy architecture
        strategy_architecture = self._build_strategy_architecture(
            structure, psychology, institutional, traps, current_time
        )
        
        # Generate entry logic
        entry_logic = self._generate_entry_logic(strategy_architecture, chart_data)
        
        # Calculate confidence
        confidence = self._calculate_strategy_confidence(
            strategy_architecture, entry_logic, market_context
        )
        
        # Create strategy name
        strategy_name = self._create_unique_strategy_name(strategy_architecture)
        
        return {
            'name': strategy_name,
            'architecture': strategy_architecture,
            'entry_logic': entry_logic,
            'confidence': confidence,
            'signal': entry_logic['signal'],
            'reasoning': self._generate_reasoning(strategy_architecture, entry_logic),
            'risk_level': self._assess_risk_level(strategy_architecture, confidence)
        }

    def _build_strategy_architecture(self, structure, psychology, institutional, traps, current_time):
        """Build unique strategy architecture for this market condition"""
        
        # Determine market condition
        if structure['trend'] in ['strong_uptrend', 'strong_downtrend']:
            condition = 'trending'
        elif structure['volatility'] == 'high':
            condition = 'volatile'
        elif structure['trend'] == 'sideways':
            condition = 'ranging'
        else:
            condition = 'quiet'
        
        # Select primary strategy type based on conditions
        primary_strategies = self.market_conditions[condition]
        primary_strategy = self._select_optimal_strategy(
            primary_strategies, structure, psychology, institutional
        )
        
        # Add confluence factors
        confluence_factors = self._identify_confluence_factors(
            structure, psychology, institutional, traps
        )
        
        # Time-based adjustments
        time_factor = self._get_time_factor(current_time)
        
        return {
            'primary_strategy': primary_strategy,
            'market_condition': condition,
            'confluence_factors': confluence_factors,
            'time_factor': time_factor,
            'adaptation_score': self._calculate_adaptation_score(structure, psychology)
        }

    def _select_optimal_strategy(self, available_strategies, structure, psychology, institutional):
        """Select the best strategy from available options"""
        
        scores = {}
        
        for strategy in available_strategies:
            score = 0.0
            
            # Score based on structure alignment
            if strategy == 'momentum_continuation' and structure['strength'] > 0.7:
                score += 0.4
            elif strategy == 'exhaustion_reversal' and structure['strength'] > 0.8:
                score += 0.5
            elif strategy == 'trap_fade' and psychology['emotion'] in ['greed', 'fear']:
                score += 0.6
            elif strategy == 'liquidity_grab_fade' and institutional['activity'] == 'accumulation':
                score += 0.5
            elif strategy == 'support_resistance' and structure['trend'] == 'sideways':
                score += 0.4
            
            # Add psychology alignment
            if psychology['emotion'] == 'greed' and 'reversal' in strategy:
                score += 0.3
            elif psychology['emotion'] == 'fear' and 'bounce' in strategy:
                score += 0.3
            
            scores[strategy] = score
        
        # Return highest scoring strategy
        return max(scores.items(), key=lambda x: x[1])[0]

    def _identify_confluence_factors(self, structure, psychology, institutional, traps):
        """Identify factors that support the strategy"""
        
        factors = []
        
        # Trend alignment
        if structure['strength'] > 0.7:
            factors.append({
                'type': 'trend_strength',
                'value': structure['strength'],
                'weight': 0.3
            })
        
        # Psychology extremes
        if psychology['intensity'] > 0.8:
            factors.append({
                'type': 'psychology_extreme',
                'value': psychology['intensity'],
                'weight': 0.4
            })
        
        # Institutional activity
        if institutional['confidence'] > 0.6:
            factors.append({
                'type': 'institutional_signal',
                'value': institutional['confidence'],
                'weight': 0.3
            })
        
        # Trap signals
        for trap in traps:
            if trap['probability'] > 0.6:
                factors.append({
                    'type': 'trap_signal',
                    'value': trap['probability'],
                    'weight': 0.25
                })
        
        return factors

    def _generate_entry_logic(self, architecture, chart_data):
        """Generate specific entry logic for the strategy"""
        
        primary_strategy = architecture['primary_strategy']
        structure = chart_data['structure']
        confluence = architecture['confluence_factors']
        
        # Base signal determination
        if 'continuation' in primary_strategy:
            if structure['trend'] == 'strong_uptrend':
                base_signal = 'CALL'
            elif structure['trend'] == 'strong_downtrend':
                base_signal = 'PUT'
            else:
                base_signal = 'NO TRADE'
        
        elif 'reversal' in primary_strategy or 'fade' in primary_strategy:
            if structure['trend'] == 'strong_uptrend':
                base_signal = 'PUT'  # Fade the uptrend
            elif structure['trend'] == 'strong_downtrend':
                base_signal = 'CALL'  # Fade the downtrend
            else:
                base_signal = 'NO TRADE'
        
        elif 'bounce' in primary_strategy:
            if structure['bullish_percentage'] < 0.3:
                base_signal = 'CALL'  # Oversold bounce
            else:
                base_signal = 'NO TRADE'
        
        else:
            # Support/resistance or pattern-based
            if len(confluence) > 2:
                # Multiple confluence factors suggest direction
                avg_confluence = sum(f['value'] for f in confluence) / len(confluence)
                if avg_confluence > 0.7:
                    base_signal = 'CALL' if structure['bullish_percentage'] > 0.5 else 'PUT'
                else:
                    base_signal = 'NO TRADE'
            else:
                base_signal = 'NO TRADE'
        
        # Generate entry conditions
        entry_conditions = self._create_entry_conditions(primary_strategy, structure)
        
        return {
            'signal': base_signal,
            'entry_conditions': entry_conditions,
            'confluence_score': len(confluence)
        }

    def _create_entry_conditions(self, strategy, structure):
        """Create specific entry conditions"""
        
        conditions = []
        
        if 'momentum' in strategy:
            conditions.append(f"Momentum strength > {structure['strength']:.1f}")
            conditions.append("Volume confirmation required")
        
        elif 'reversal' in strategy:
            conditions.append("Exhaustion signals present")
            conditions.append(f"Trend strength at extreme ({structure['strength']:.1f})")
        
        elif 'fade' in strategy:
            conditions.append("False breakout confirmed")
            conditions.append("Quick reversal expected")
        
        elif 'bounce' in strategy:
            conditions.append("Oversold conditions")
            conditions.append("Support level holding")
        
        return conditions

    def _calculate_strategy_confidence(self, architecture, entry_logic, market_context):
        """Calculate confidence in the strategy"""
        
        base_confidence = 0.5
        
        # Primary strategy strength
        strategy_name = architecture['primary_strategy']
        if strategy_name in ['exhaustion_reversal', 'liquidity_grab_fade']:
            base_confidence += 0.2
        elif strategy_name in ['momentum_continuation', 'trap_fade']:
            base_confidence += 0.15
        else:
            base_confidence += 0.1
        
        # Confluence factors boost
        confluence_boost = len(architecture['confluence_factors']) * 0.05
        base_confidence += confluence_boost
        
        # Market psychology alignment
        psychology = market_context['dominant_emotion']
        if psychology['intensity'] > 0.8:
            base_confidence += 0.1
        
        # Institutional activity alignment
        institutional = market_context['institutional_activity']
        if institutional['confidence'] > 0.7:
            base_confidence += 0.08
        
        # Time factor adjustment
        time_boost = architecture['time_factor'] * 0.05
        base_confidence += time_boost
        
        # Adaptation score (uniqueness bonus)
        adaptation_bonus = architecture['adaptation_score'] * 0.1
        base_confidence += adaptation_bonus
        
        return min(base_confidence, 0.98)  # Cap at 98%

    def _get_time_factor(self, current_time):
        """Get time-based factor (0.0 to 1.0)"""
        hour = current_time.hour
        
        # Peak trading hours (9-11 AM, 2-4 PM UTC+6)
        if 9 <= hour <= 11 or 14 <= hour <= 16:
            return 1.0
        # Good trading hours
        elif 8 <= hour <= 18:
            return 0.8
        # Quiet hours
        else:
            return 0.4

    def _calculate_adaptation_score(self, structure, psychology):
        """Calculate how well adapted the strategy is"""
        
        # Higher adaptation for unique market conditions
        uniqueness = 0.0
        
        # Unusual trend combinations
        if structure['trend'] == 'weak_trend' and structure['volatility'] == 'high':
            uniqueness += 0.3
        
        # Extreme psychology states
        if psychology['emotion'] in ['euphoria', 'panic']:
            uniqueness += 0.4
        
        # Mixed signals (requires adaptation)
        if abs(structure['bullish_percentage'] - 0.5) < 0.1:
            uniqueness += 0.2
        
        return min(uniqueness, 1.0)

    def _create_unique_strategy_name(self, architecture):
        """Create a unique name for the strategy"""
        
        primary = architecture['primary_strategy'].replace('_', ' ').title()
        condition = architecture['market_condition'].title()
        confluence_count = len(architecture['confluence_factors'])
        
        if confluence_count >= 3:
            modifier = "Multi-Confluence"
        elif confluence_count == 2:
            modifier = "Dual-Signal"
        else:
            modifier = "Single-Factor"
        
        return f"{modifier} {primary}"

    def _generate_reasoning(self, architecture, entry_logic):
        """Generate human-readable reasoning"""
        
        primary = architecture['primary_strategy']
        confluence = architecture['confluence_factors']
        signal = entry_logic['signal']
        
        reasoning = f"Strategy: {primary.replace('_', ' ').title()}"
        
        if signal != 'NO TRADE':
            reasoning += f" | Signal: {signal} direction identified"
            
            if confluence:
                confluence_types = [f['type'] for f in confluence]
                reasoning += f" | Confluence: {', '.join(confluence_types)}"
        
        return reasoning

    def _assess_risk_level(self, architecture, confidence):
        """Assess the risk level of the strategy"""
        
        primary = architecture['primary_strategy']
        confluence_count = len(architecture['confluence_factors'])
        
        # Base risk from strategy type
        if 'reversal' in primary or 'fade' in primary:
            base_risk = 0.5  # Higher risk strategies
        else:
            base_risk = 0.3  # Lower risk strategies
        
        # Reduce risk with more confluence
        risk_reduction = confluence_count * 0.05
        
        # Reduce risk with higher confidence
        confidence_reduction = (confidence - 0.5) * 0.2
        
        final_risk = max(base_risk - risk_reduction - confidence_reduction, 0.1)
        
        if final_risk > 0.4:
            return 'high'
        elif final_risk > 0.25:
            return 'medium'
        else:
            return 'low'