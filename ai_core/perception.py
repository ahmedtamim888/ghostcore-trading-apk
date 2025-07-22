"""
🔮 COSMIC OMNI-BRAIN AI - PERCEPTION MODULE
Advanced computer vision for candlestick chart analysis
"""

import cv2
import numpy as np
from typing import List, Dict, Tuple, Optional
import json

class CandlePerception:
    """
    Advanced candlestick pattern recognition and chart structure analysis
    """
    
    def __init__(self):
        self.name = "COSMIC PERCEPTION ENGINE"
        self.version = "∞.UNBEATABLE"
        
        # Candle pattern templates
        self.patterns = {
            'doji': {'body_ratio': 0.1, 'wick_ratio': 0.8},
            'hammer': {'body_ratio': 0.3, 'lower_wick': 2.0},
            'shooting_star': {'body_ratio': 0.3, 'upper_wick': 2.0},
            'engulfing': {'body_comparison': 1.5},
            'marubozu': {'body_ratio': 0.9, 'wick_ratio': 0.1}
        }
        
        # Color detection ranges (HSV)
        self.color_ranges = {
            'green': [(50, 50, 50), (80, 255, 255)],
            'red': [(0, 50, 50), (10, 255, 255)],
            'white': [(0, 0, 180), (180, 30, 255)],
            'black': [(0, 0, 0), (180, 255, 50)]
        }
        
    def detect_candlesticks(self, image: np.ndarray) -> List[Dict]:
        """
        🧠 ULTIMATE CANDLE DETECTION
        Extracts all candlestick data from chart image
        """
        
        print("🔮 COSMIC PERCEPTION: Analyzing chart structure...")
        
        # Convert to different color spaces for analysis
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect candle bodies and wicks
        candles = []
        
        # 1. Find vertical lines (wicks)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, 
                               minLineLength=5, maxLineGap=3)
        
        # 2. Find rectangular shapes (candle bodies)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 3. Group lines and rectangles into candles
        potential_candles = self._group_candle_components(lines, contours, image.shape)
        
        # 4. Extract candle properties
        for i, candle_data in enumerate(potential_candles):
            candle = self._extract_candle_properties(candle_data, hsv, i)
            if candle:
                candles.append(candle)
        
        # 5. Sort candles by x-position (time order)
        candles.sort(key=lambda x: x['position']['x'])
        
        print(f"🎯 DETECTED {len(candles)} CANDLESTICKS")
        
        return candles
    
    def _group_candle_components(self, lines: np.ndarray, contours: List, image_shape: Tuple) -> List[Dict]:
        """Group detected lines and contours into candle structures"""
        
        height, width = image_shape[:2]
        candle_width = width // 100  # Estimate candle width
        
        potential_candles = []
        
        if lines is not None:
            # Group vertical lines by proximity
            vertical_lines = []
            for line in lines:
                x1, y1, x2, y2 = line[0]
                if abs(x2 - x1) < 5:  # Nearly vertical
                    vertical_lines.append({
                        'x': (x1 + x2) // 2,
                        'y1': min(y1, y2),
                        'y2': max(y1, y2),
                        'length': abs(y2 - y1)
                    })
            
            # Find rectangles near vertical lines
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                
                # Look for nearby vertical lines
                nearby_lines = [line for line in vertical_lines 
                              if abs(line['x'] - (x + w//2)) < candle_width]
                
                if nearby_lines and h > 5:  # Minimum body height
                    candle_data = {
                        'body': {'x': x, 'y': y, 'width': w, 'height': h},
                        'wicks': nearby_lines,
                        'center_x': x + w // 2
                    }
                    potential_candles.append(candle_data)
        
        return potential_candles
    
    def _extract_candle_properties(self, candle_data: Dict, hsv_image: np.ndarray, index: int) -> Optional[Dict]:
        """Extract detailed properties from candle data"""
        
        body = candle_data['body']
        wicks = candle_data['wicks']
        
        # Extract colors from body region
        body_roi = hsv_image[body['y']:body['y']+body['height'], 
                            body['x']:body['x']+body['width']]
        
        if body_roi.size == 0:
            return None
            
        # Determine candle direction (bullish/bearish)
        color = self._detect_candle_color(body_roi)
        is_bullish = color in ['green', 'white']
        
        # Calculate wick lengths
        upper_wick = 0
        lower_wick = 0
        
        if wicks:
            main_wick = max(wicks, key=lambda x: x['length'])
            body_top = body['y']
            body_bottom = body['y'] + body['height']
            
            upper_wick = max(0, body_top - main_wick['y1'])
            lower_wick = max(0, main_wick['y2'] - body_bottom)
        
        # Calculate ratios for pattern recognition
        total_height = body['height'] + upper_wick + lower_wick
        body_ratio = body['height'] / total_height if total_height > 0 else 0
        upper_wick_ratio = upper_wick / total_height if total_height > 0 else 0
        lower_wick_ratio = lower_wick / total_height if total_height > 0 else 0
        
        # Detect pattern
        pattern = self._identify_pattern(body_ratio, upper_wick_ratio, lower_wick_ratio)
        
        return {
            'id': f"candle_{index}",
            'position': {
                'x': candle_data['center_x'],
                'y': body['y'] + body['height'] // 2
            },
            'body': {
                'height': body['height'],
                'width': body['width'],
                'top': body['y'],
                'bottom': body['y'] + body['height']
            },
            'wicks': {
                'upper': upper_wick,
                'lower': lower_wick
            },
            'ratios': {
                'body': body_ratio,
                'upper_wick': upper_wick_ratio,
                'lower_wick': lower_wick_ratio
            },
            'direction': 'bullish' if is_bullish else 'bearish',
            'color': color,
            'pattern': pattern,
            'total_height': total_height,
            'strength': self._calculate_candle_strength(body_ratio, total_height)
        }
    
    def _detect_candle_color(self, hsv_roi: np.ndarray) -> str:
        """Detect candle color from HSV region"""
        
        # Calculate color histograms
        color_scores = {}
        
        for color_name, (lower, upper) in self.color_ranges.items():
            lower = np.array(lower)
            upper = np.array(upper)
            mask = cv2.inRange(hsv_roi, lower, upper)
            score = np.sum(mask) / (hsv_roi.shape[0] * hsv_roi.shape[1] * 255)
            color_scores[color_name] = score
        
        # Return dominant color
        return max(color_scores, key=color_scores.get)
    
    def _identify_pattern(self, body_ratio: float, upper_wick_ratio: float, lower_wick_ratio: float) -> str:
        """Identify candlestick pattern based on ratios"""
        
        # Doji pattern
        if body_ratio < 0.15 and (upper_wick_ratio > 0.3 or lower_wick_ratio > 0.3):
            return 'doji'
        
        # Hammer pattern
        if body_ratio < 0.4 and lower_wick_ratio > 0.5 and upper_wick_ratio < 0.2:
            return 'hammer'
        
        # Shooting star pattern
        if body_ratio < 0.4 and upper_wick_ratio > 0.5 and lower_wick_ratio < 0.2:
            return 'shooting_star'
        
        # Marubozu pattern
        if body_ratio > 0.8:
            return 'marubozu'
        
        # Long body
        if body_ratio > 0.6:
            return 'long_body'
        
        # Small body
        if body_ratio < 0.3:
            return 'small_body'
        
        return 'standard'
    
    def _calculate_candle_strength(self, body_ratio: float, total_height: int) -> float:
        """Calculate candle strength score"""
        
        # Combine body ratio and absolute size
        size_factor = min(total_height / 50, 2.0)  # Normalize height
        strength = (body_ratio * 0.7 + size_factor * 0.3)
        
        return min(strength, 1.0)
    
    def detect_price_levels(self, image: np.ndarray, candles: List[Dict]) -> Dict:
        """
        🎯 SUPPORT/RESISTANCE DETECTION
        Identify key price levels from chart
        """
        
        print("🔮 COSMIC PERCEPTION: Detecting support/resistance levels...")
        
        if not candles:
            return {'support': [], 'resistance': []}
        
        # Extract price points
        highs = [candle['body']['top'] for candle in candles]
        lows = [candle['body']['bottom'] for candle in candles]
        
        # Find support levels (cluster of lows)
        support_levels = self._find_price_clusters(lows, tolerance=10)
        
        # Find resistance levels (cluster of highs)
        resistance_levels = self._find_price_clusters(highs, tolerance=10)
        
        return {
            'support': support_levels,
            'resistance': resistance_levels,
            'price_range': {
                'high': min(highs) if highs else 0,
                'low': max(lows) if lows else 0
            }
        }
    
    def _find_price_clusters(self, price_points: List[int], tolerance: int = 10) -> List[Dict]:
        """Find clusters of similar price levels"""
        
        if not price_points:
            return []
        
        clusters = []
        sorted_points = sorted(price_points)
        
        current_cluster = [sorted_points[0]]
        
        for point in sorted_points[1:]:
            if point - current_cluster[-1] <= tolerance:
                current_cluster.append(point)
            else:
                if len(current_cluster) >= 2:  # At least 2 touches
                    clusters.append({
                        'level': sum(current_cluster) // len(current_cluster),
                        'touches': len(current_cluster),
                        'strength': len(current_cluster) / len(price_points)
                    })
                current_cluster = [point]
        
        # Add final cluster
        if len(current_cluster) >= 2:
            clusters.append({
                'level': sum(current_cluster) // len(current_cluster),
                'touches': len(current_cluster),
                'strength': len(current_cluster) / len(price_points)
            })
        
        return sorted(clusters, key=lambda x: x['strength'], reverse=True)[:5]  # Top 5 levels
    
    def analyze_chart_structure(self, image: np.ndarray) -> Dict:
        """
        🧠 COMPLETE CHART ANALYSIS
        Master function for full chart perception
        """
        
        print("🔮 COSMIC PERCEPTION: Full chart analysis initiated...")
        
        # Detect all candlesticks
        candles = self.detect_candlesticks(image)
        
        # Detect price levels
        price_levels = self.detect_price_levels(image, candles)
        
        # Analyze trend structure
        trend_analysis = self._analyze_trend_structure(candles)
        
        # Detect chart patterns
        patterns = self._detect_chart_patterns(candles)
        
        # Market structure analysis
        market_structure = self._analyze_market_structure(candles, price_levels)
        
        return {
            'candles': candles,
            'price_levels': price_levels,
            'trend': trend_analysis,
            'patterns': patterns,
            'market_structure': market_structure,
            'analysis_quality': len(candles) / max(1, len(candles) * 0.1),  # Quality score
            'timestamp': self._get_timestamp()
        }
    
    def _analyze_trend_structure(self, candles: List[Dict]) -> Dict:
        """Analyze overall trend from candle sequence"""
        
        if len(candles) < 5:
            return {'direction': 'insufficient_data', 'strength': 0}
        
        # Calculate trend from recent candles
        recent_candles = candles[-10:]  # Last 10 candles
        
        bullish_count = sum(1 for c in recent_candles if c['direction'] == 'bullish')
        bearish_count = len(recent_candles) - bullish_count
        
        # Determine trend direction
        if bullish_count > bearish_count * 1.5:
            direction = 'uptrend'
            strength = bullish_count / len(recent_candles)
        elif bearish_count > bullish_count * 1.5:
            direction = 'downtrend'
            strength = bearish_count / len(recent_candles)
        else:
            direction = 'sideways'
            strength = 0.5
        
        return {
            'direction': direction,
            'strength': strength,
            'bullish_candles': bullish_count,
            'bearish_candles': bearish_count
        }
    
    def _detect_chart_patterns(self, candles: List[Dict]) -> List[Dict]:
        """Detect chart patterns from candle sequence"""
        
        patterns = []
        
        if len(candles) < 3:
            return patterns
        
        # Check for engulfing patterns
        for i in range(1, len(candles)):
            prev_candle = candles[i-1]
            curr_candle = candles[i]
            
            # Bullish engulfing
            if (prev_candle['direction'] == 'bearish' and 
                curr_candle['direction'] == 'bullish' and
                curr_candle['body']['height'] > prev_candle['body']['height'] * 1.2):
                
                patterns.append({
                    'type': 'bullish_engulfing',
                    'position': i,
                    'strength': curr_candle['strength'],
                    'confidence': 0.8
                })
            
            # Bearish engulfing
            elif (prev_candle['direction'] == 'bullish' and 
                  curr_candle['direction'] == 'bearish' and
                  curr_candle['body']['height'] > prev_candle['body']['height'] * 1.2):
                
                patterns.append({
                    'type': 'bearish_engulfing',
                    'position': i,
                    'strength': curr_candle['strength'],
                    'confidence': 0.8
                })
        
        return patterns
    
    def _analyze_market_structure(self, candles: List[Dict], price_levels: Dict) -> Dict:
        """Analyze market structure and key levels"""
        
        if not candles:
            return {'structure': 'unknown', 'quality': 0}
        
        # Analyze recent price action relative to support/resistance
        recent_candles = candles[-5:] if len(candles) >= 5 else candles
        
        structure_signals = []
        
        # Check interaction with support/resistance
        for level in price_levels.get('support', []):
            for candle in recent_candles:
                if abs(candle['body']['bottom'] - level['level']) < 20:
                    structure_signals.append('support_test')
        
        for level in price_levels.get('resistance', []):
            for candle in recent_candles:
                if abs(candle['body']['top'] - level['level']) < 20:
                    structure_signals.append('resistance_test')
        
        # Determine market structure
        if 'resistance_test' in structure_signals and 'support_test' not in structure_signals:
            structure = 'at_resistance'
        elif 'support_test' in structure_signals and 'resistance_test' not in structure_signals:
            structure = 'at_support'
        elif len(structure_signals) > 2:
            structure = 'range_bound'
        else:
            structure = 'trending'
        
        return {
            'structure': structure,
            'signals': structure_signals,
            'quality': len(structure_signals) / max(1, len(recent_candles))
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()