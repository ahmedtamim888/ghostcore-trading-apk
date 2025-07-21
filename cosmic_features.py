#!/usr/bin/env python3
"""
🔮 COSMIC OMNI-BRAIN AI - ADVANCED TRADING FEATURES
Enhanced features for professional signal analysis
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

class CosmicTradingFeatures:
    def __init__(self):
        self.db_path = 'cosmic_signals.db'
        self.init_database()
        
    def init_database(self):
        """Initialize the signal tracking database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Signals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                broker TEXT NOT NULL,
                pair TEXT NOT NULL,
                timeframe TEXT NOT NULL,
                signal TEXT NOT NULL,
                confidence INTEGER NOT NULL,
                strategy TEXT NOT NULL,
                market_health INTEGER NOT NULL,
                volatility TEXT NOT NULL,
                trend TEXT NOT NULL,
                manipulation_risk INTEGER NOT NULL,
                reasoning TEXT NOT NULL,
                result TEXT DEFAULT 'pending',
                profit_loss REAL DEFAULT 0.0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Performance metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                total_signals INTEGER DEFAULT 0,
                winning_signals INTEGER DEFAULT 0,
                losing_signals INTEGER DEFAULT 0,
                win_rate REAL DEFAULT 0.0,
                total_profit REAL DEFAULT 0.0,
                avg_confidence REAL DEFAULT 0.0,
                best_strategy TEXT DEFAULT '',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Market analysis table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS market_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                broker TEXT NOT NULL,
                market_condition TEXT NOT NULL,
                volatility_level TEXT NOT NULL,
                trend_strength INTEGER NOT NULL,
                manipulation_detected BOOLEAN DEFAULT FALSE,
                liquidity_level TEXT NOT NULL,
                recommended_action TEXT NOT NULL,
                confidence_adjustment REAL DEFAULT 0.0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def log_signal(self, signal_data: Dict) -> int:
        """Log a signal to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO signals (
                timestamp, broker, pair, timeframe, signal, confidence,
                strategy, market_health, volatility, trend, manipulation_risk, reasoning
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            signal_data.get('broker', 'Unknown'),
            signal_data.get('pair', 'Unknown'),
            signal_data.get('timeframe', '1M'),
            signal_data.get('signal', 'NO SIGNAL'),
            signal_data.get('confidence', 0),
            signal_data.get('strategy', 'Unknown'),
            signal_data.get('market_health', 0),
            signal_data.get('volatility', 'Unknown'),
            signal_data.get('trend', 'Unknown'),
            signal_data.get('manipulation_risk', 0),
            signal_data.get('reasoning', 'No reasoning provided')
        ))
        
        signal_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return signal_id
        
    def update_signal_result(self, signal_id: int, result: str, profit_loss: float):
        """Update signal result after trade completion"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE signals 
            SET result = ?, profit_loss = ?
            WHERE id = ?
        ''', (result, profit_loss, signal_id))
        
        conn.commit()
        conn.close()
        
    def get_signal_history(self, limit: int = 50) -> List[Dict]:
        """Get recent signal history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM signals 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (limit,))
        
        columns = [description[0] for description in cursor.description]
        signals = []
        
        for row in cursor.fetchall():
            signal_dict = dict(zip(columns, row))
            signals.append(signal_dict)
            
        conn.close()
        return signals
        
    def calculate_performance_metrics(self, days: int = 30) -> Dict:
        """Calculate performance metrics for the last N days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        since_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total_signals,
                SUM(CASE WHEN result = 'win' THEN 1 ELSE 0 END) as winning_signals,
                SUM(CASE WHEN result = 'loss' THEN 1 ELSE 0 END) as losing_signals,
                AVG(confidence) as avg_confidence,
                SUM(profit_loss) as total_profit,
                strategy as best_strategy
            FROM signals 
            WHERE created_at >= ?
            AND result != 'pending'
            GROUP BY strategy
            ORDER BY COUNT(*) DESC
        ''', (since_date,))
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return {
                'total_signals': 0,
                'winning_signals': 0,
                'losing_signals': 0,
                'win_rate': 0.0,
                'avg_confidence': 0.0,
                'total_profit': 0.0,
                'best_strategy': 'No data'
            }
            
        total_signals = sum(row[0] for row in results)
        winning_signals = sum(row[1] for row in results)
        losing_signals = sum(row[2] for row in results)
        win_rate = (winning_signals / max(winning_signals + losing_signals, 1)) * 100
        avg_confidence = sum(row[3] for row in results if row[3]) / len(results)
        total_profit = sum(row[4] for row in results if row[4])
        best_strategy = results[0][5] if results else 'Unknown'
        
        return {
            'total_signals': total_signals,
            'winning_signals': winning_signals,
            'losing_signals': losing_signals,
            'win_rate': round(win_rate, 2),
            'avg_confidence': round(avg_confidence, 2),
            'total_profit': round(total_profit, 2),
            'best_strategy': best_strategy
        }
        
    def get_strategy_performance(self) -> Dict[str, Dict]:
        """Get performance breakdown by strategy"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                strategy,
                COUNT(*) as total,
                SUM(CASE WHEN result = 'win' THEN 1 ELSE 0 END) as wins,
                AVG(confidence) as avg_confidence,
                SUM(profit_loss) as total_profit
            FROM signals 
            WHERE result != 'pending'
            GROUP BY strategy
            ORDER BY total DESC
        ''')
        
        strategies = {}
        for row in cursor.fetchall():
            strategy, total, wins, avg_conf, profit = row
            win_rate = (wins / max(total, 1)) * 100
            
            strategies[strategy] = {
                'total_signals': total,
                'wins': wins,
                'losses': total - wins,
                'win_rate': round(win_rate, 2),
                'avg_confidence': round(avg_conf or 0, 2),
                'total_profit': round(profit or 0, 2)
            }
            
        conn.close()
        return strategies
        
    def analyze_market_conditions(self, image_analysis: Dict) -> Dict:
        """Analyze current market conditions for risk assessment"""
        market_condition = 'normal'
        liquidity_level = 'medium'
        recommended_action = 'proceed'
        confidence_adjustment = 0.0
        
        # Analyze volatility
        volatility = image_analysis.get('volatility', 'medium').lower()
        manipulation_risk = image_analysis.get('manipulation_risk', 0)
        market_health = image_analysis.get('market_health', 50)
        
        # Determine market condition
        if manipulation_risk > 70:
            market_condition = 'highly_manipulated'
            confidence_adjustment = -20.0
            recommended_action = 'avoid'
        elif manipulation_risk > 50:
            market_condition = 'manipulated'
            confidence_adjustment = -10.0
            recommended_action = 'caution'
        elif volatility == 'high' and market_health < 40:
            market_condition = 'volatile_unhealthy'
            confidence_adjustment = -15.0
            recommended_action = 'reduce_exposure'
        elif market_health > 80:
            market_condition = 'healthy'
            confidence_adjustment = 5.0
            recommended_action = 'favorable'
            
        # Determine liquidity level
        if volatility == 'low' and market_health > 70:
            liquidity_level = 'high'
        elif volatility == 'high' or manipulation_risk > 60:
            liquidity_level = 'low'
            
        analysis = {
            'market_condition': market_condition,
            'liquidity_level': liquidity_level,
            'recommended_action': recommended_action,
            'confidence_adjustment': confidence_adjustment,
            'risk_level': 'high' if manipulation_risk > 60 else 'medium' if manipulation_risk > 30 else 'low'
        }
        
        # Log to database
        self.log_market_analysis(analysis, image_analysis)
        
        return analysis
        
    def log_market_analysis(self, analysis: Dict, image_analysis: Dict):
        """Log market analysis to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO market_analysis (
                timestamp, broker, market_condition, volatility_level,
                trend_strength, manipulation_detected, liquidity_level,
                recommended_action, confidence_adjustment
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            image_analysis.get('broker', 'Unknown'),
            analysis['market_condition'],
            image_analysis.get('volatility', 'medium'),
            image_analysis.get('market_health', 50),
            image_analysis.get('manipulation_risk', 0) > 50,
            analysis['liquidity_level'],
            analysis['recommended_action'],
            analysis['confidence_adjustment']
        ))
        
        conn.commit()
        conn.close()
        
    def get_risk_management_recommendations(self, signal_data: Dict, market_analysis: Dict) -> Dict:
        """Generate risk management recommendations"""
        confidence = signal_data.get('confidence', 0)
        manipulation_risk = signal_data.get('manipulation_risk', 0)
        market_health = signal_data.get('market_health', 50)
        
        # Base position size (percentage of capital)
        base_position_size = 2.0  # 2% base position
        
        # Adjust based on confidence
        if confidence >= 90:
            position_multiplier = 1.5
        elif confidence >= 80:
            position_multiplier = 1.2
        elif confidence >= 70:
            position_multiplier = 1.0
        else:
            position_multiplier = 0.5
            
        # Adjust based on market conditions
        if market_analysis['risk_level'] == 'high':
            position_multiplier *= 0.5
        elif market_analysis['risk_level'] == 'low':
            position_multiplier *= 1.2
            
        # Adjust based on market health
        if market_health < 40:
            position_multiplier *= 0.7
        elif market_health > 80:
            position_multiplier *= 1.1
            
        recommended_position_size = min(base_position_size * position_multiplier, 5.0)  # Max 5%
        
        # Stop loss recommendations
        if confidence >= 85:
            stop_loss_pips = 10
        elif confidence >= 75:
            stop_loss_pips = 15
        else:
            stop_loss_pips = 20
            
        # Take profit recommendations
        take_profit_pips = stop_loss_pips * 2  # 2:1 risk-reward ratio
        
        return {
            'recommended_position_size': round(recommended_position_size, 2),
            'stop_loss_pips': stop_loss_pips,
            'take_profit_pips': take_profit_pips,
            'risk_reward_ratio': '1:2',
            'max_daily_trades': 10 if market_analysis['risk_level'] == 'low' else 5,
            'trading_session': 'recommended' if market_health > 60 else 'caution'
        }
        
    def export_performance_report(self, days: int = 30) -> str:
        """Export detailed performance report"""
        metrics = self.calculate_performance_metrics(days)
        strategy_performance = self.get_strategy_performance()
        signal_history = self.get_signal_history(100)
        
        report = f"""
🔮 COSMIC OMNI-BRAIN AI - PERFORMANCE REPORT
============================================
Report Period: Last {days} days
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 OVERALL PERFORMANCE
----------------------
Total Signals: {metrics['total_signals']}
Winning Signals: {metrics['winning_signals']}
Losing Signals: {metrics['losing_signals']}
Win Rate: {metrics['win_rate']}%
Average Confidence: {metrics['avg_confidence']}%
Total Profit/Loss: {metrics['total_profit']}
Best Strategy: {metrics['best_strategy']}

📈 STRATEGY BREAKDOWN
---------------------
"""
        
        for strategy, data in strategy_performance.items():
            report += f"""
{strategy}:
  - Total Signals: {data['total_signals']}
  - Win Rate: {data['win_rate']}%
  - Average Confidence: {data['avg_confidence']}%
  - Total P&L: {data['total_profit']}
"""
        
        report += f"""
🕐 RECENT SIGNALS
-----------------
"""
        
        for signal in signal_history[:10]:
            report += f"""
{signal['timestamp']}: {signal['signal']} | {signal['pair']} | {signal['confidence']}% | {signal['strategy']} | Result: {signal['result']}
"""
        
        # Save report to file
        report_filename = f"cosmic_performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_filename, 'w') as f:
            f.write(report)
            
        return report_filename
        
    def get_trading_dashboard_data(self) -> Dict:
        """Get comprehensive data for trading dashboard"""
        performance = self.calculate_performance_metrics(30)
        recent_signals = self.get_signal_history(10)
        strategy_performance = self.get_strategy_performance()
        
        # Calculate trend analysis
        signals_today = self.get_signal_history_by_date(datetime.now().date())
        signals_yesterday = self.get_signal_history_by_date(datetime.now().date() - timedelta(days=1))
        
        return {
            'performance': performance,
            'recent_signals': recent_signals,
            'strategy_performance': strategy_performance,
            'daily_summary': {
                'today_signals': len(signals_today),
                'yesterday_signals': len(signals_yesterday),
                'trend': 'up' if len(signals_today) > len(signals_yesterday) else 'down'
            },
            'risk_metrics': {
                'avg_manipulation_risk': self.get_avg_manipulation_risk(),
                'avg_market_health': self.get_avg_market_health(),
                'recommended_action': self.get_current_market_recommendation()
            }
        }
        
    def get_signal_history_by_date(self, date) -> List[Dict]:
        """Get signals for a specific date"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        date_str = date.strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT * FROM signals 
            WHERE date(created_at) = ?
            ORDER BY created_at DESC
        ''', (date_str,))
        
        columns = [description[0] for description in cursor.description]
        signals = []
        
        for row in cursor.fetchall():
            signal_dict = dict(zip(columns, row))
            signals.append(signal_dict)
            
        conn.close()
        return signals
        
    def get_avg_manipulation_risk(self) -> float:
        """Get average manipulation risk from recent signals"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT AVG(manipulation_risk) 
            FROM signals 
            WHERE created_at >= datetime('now', '-7 days')
        ''')
        
        result = cursor.fetchone()[0]
        conn.close()
        
        return round(result or 0, 2)
        
    def get_avg_market_health(self) -> float:
        """Get average market health from recent signals"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT AVG(market_health) 
            FROM signals 
            WHERE created_at >= datetime('now', '-7 days')
        ''')
        
        result = cursor.fetchone()[0]
        conn.close()
        
        return round(result or 0, 2)
        
    def get_current_market_recommendation(self) -> str:
        """Get current market recommendation based on recent analysis"""
        avg_manipulation = self.get_avg_manipulation_risk()
        avg_health = self.get_avg_market_health()
        
        if avg_manipulation > 60:
            return 'avoid_trading'
        elif avg_manipulation > 40 or avg_health < 50:
            return 'trade_with_caution'
        elif avg_health > 75:
            return 'favorable_conditions'
        else:
            return 'normal_conditions'