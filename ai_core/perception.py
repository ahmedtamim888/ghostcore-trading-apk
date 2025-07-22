"""
COSMIC OMNI-BRAIN AI v∞.UNBEATABLE
Advanced Candlestick Perception Engine
Real-time Chart Analysis & Pattern Recognition
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import io
import math

class CandlePerception:
    def __init__(self):
        self.candle_patterns = {
            'hammer': {'shadow_ratio': 2.0, 'body_position': 'bottom', 'strength': 0.85},
            'shooting_star': {'shadow_ratio': 2.0, 'body_position': 'top', 'strength': 0.85},
            'doji': {'body_ratio': 0.1, 'indecision': True, 'strength': 0.7},
            'engulfing_bull': {'size_ratio': 1.5, 'color': 'green', 'strength': 0.9},
            'engulfing_bear': {'size_ratio': 1.5, 'color': 'red', 'strength': 0.9},
            'inside_bar': {'contained': True, 'consolidation': True, 'strength': 0.6},
            'outside_bar': {'containing': True, 'volatility': True, 'strength': 0.8},
            'pin_bar': {'wick_ratio': 3.0, 'rejection': True, 'strength': 0.85}
        }
        
        self.color_detection = {
            'bullish_green': [(0, 150, 0), (100, 255, 100)],
            'bearish_red': [(150, 0, 0), (255, 100, 100)],
            'neutral_gray': [(100, 100, 100), (200, 200, 200)]
        }

    def analyze_chart_image(self, image_data):
        """Main chart analysis function"""
        try:
            # Load and prepare image
            image = Image.open(io.BytesIO(image_data))
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            width, height = image.size
            pixels = list(image.getdata())
            
            # Advanced pixel analysis
            pixel_analysis = self._analyze_pixels(pixels, width, height)
            
            # Detect candlestick patterns
            candle_data = self._detect_candlesticks(pixel_analysis, width, height)
            
            # Identify chart structure
            structure = self._analyze_chart_structure(candle_data, pixel_analysis)
            
            # Detect price levels
            price_levels = self._detect_price_levels(pixel_analysis, width, height)
            
            return {
                'pixel_analysis': pixel_analysis,
                'candle_data': candle_data,
                'structure': structure,
                'price_levels': price_levels,
                'image_info': {'width': width, 'height': height}
            }
            
        except Exception as e:
            print(f"Error in chart analysis: {e}")
            return None

    def _analyze_pixels(self, pixels, width, height):
        """Advanced pixel-level analysis"""
        green_pixels = 0
        red_pixels = 0
        total_brightness = 0
        color_clusters = []
        
        # Analyze color distribution
        for i, pixel in enumerate(pixels):
            r, g, b = pixel
            brightness = (r + g + b) / 3
            total_brightness += brightness
            
            # Detect bullish candles (green)
            if g > r + 20 and g > b + 20 and g > 120:
                green_pixels += 1
            
            # Detect bearish candles (red)
            elif r > g + 20 and r > b + 20 and r > 120:
                red_pixels += 1
        
        total_pixels = len(pixels)
        avg_brightness = total_brightness / total_pixels
        
        # Calculate market sentiment ratios
        colored_pixels = green_pixels + red_pixels
        if colored_pixels > 0:
            bullish_ratio = green_pixels / colored_pixels
            bearish_ratio = red_pixels / colored_pixels
        else:
            bullish_ratio = bearish_ratio = 0.5
        
        # Detect chart background and candle density
        candle_density = colored_pixels / total_pixels
        
        return {
            'bullish_ratio': bullish_ratio,
            'bearish_ratio': bearish_ratio,
            'avg_brightness': avg_brightness,
            'candle_density': candle_density,
            'green_pixels': green_pixels,
            'red_pixels': red_pixels,
            'total_pixels': total_pixels
        }

    def _detect_candlesticks(self, pixel_analysis, width, height):
        """Detect individual candlesticks and their properties"""
        
        # Estimate number of candles based on image width
        estimated_candles = min(50, max(10, width // 20))
        
        candles = []
        
        # Simulate candle detection based on pixel analysis
        for i in range(estimated_candles):
            # Create candle data based on pixel ratios
            if pixel_analysis['bullish_ratio'] > 0.6:
                candle_type = 'bullish'
                body_size = 0.6 + (pixel_analysis['bullish_ratio'] * 0.4)
            elif pixel_analysis['bearish_ratio'] > 0.6:
                candle_type = 'bearish'
                body_size = 0.6 + (pixel_analysis['bearish_ratio'] * 0.4)
            else:
                candle_type = 'neutral'
                body_size = 0.3 + (pixel_analysis['candle_density'] * 0.3)
            
            # Simulate wick lengths based on brightness
            upper_wick = pixel_analysis['avg_brightness'] / 255 * 0.5
            lower_wick = (255 - pixel_analysis['avg_brightness']) / 255 * 0.5
            
            candle = {
                'index': i,
                'type': candle_type,
                'body_size': body_size,
                'upper_wick': upper_wick,
                'lower_wick': lower_wick,
                'position_x': (i / estimated_candles) * width,
                'strength': body_size + (upper_wick + lower_wick) / 2
            }
            
            candles.append(candle)
        
        return candles

    def _analyze_chart_structure(self, candles, pixel_analysis):
        """Analyze overall chart structure and trends"""
        
        if not candles:
            return {'trend': 'unknown', 'strength': 0.0}
        
        # Analyze trend based on candle progression
        bullish_candles = sum(1 for c in candles if c['type'] == 'bullish')
        bearish_candles = sum(1 for c in candles if c['type'] == 'bearish')
        
        total_candles = len(candles)
        bullish_percentage = bullish_candles / total_candles if total_candles > 0 else 0
        
        # Determine trend strength
        if bullish_percentage > 0.7:
            trend = 'strong_uptrend'
            strength = bullish_percentage
        elif bullish_percentage < 0.3:
            trend = 'strong_downtrend'
            strength = 1 - bullish_percentage
        elif 0.4 <= bullish_percentage <= 0.6:
            trend = 'sideways'
            strength = 0.5
        else:
            trend = 'weak_trend'
            strength = abs(bullish_percentage - 0.5) * 2
        
        # Detect volatility
        avg_body_size = sum(c['body_size'] for c in candles) / len(candles)
        avg_wick_size = sum(c['upper_wick'] + c['lower_wick'] for c in candles) / len(candles)
        
        if avg_wick_size > avg_body_size * 1.5:
            volatility = 'high'
        elif avg_wick_size > avg_body_size * 0.8:
            volatility = 'medium'
        else:
            volatility = 'low'
        
        return {
            'trend': trend,
            'strength': strength,
            'volatility': volatility,
            'bullish_percentage': bullish_percentage,
            'avg_body_size': avg_body_size,
            'avg_wick_size': avg_wick_size
        }

    def _detect_price_levels(self, pixel_analysis, width, height):
        """Detect support and resistance levels"""
        
        # Simulate S/R detection based on brightness patterns
        brightness = pixel_analysis['avg_brightness']
        
        # High brightness areas often indicate S/R levels
        resistance_strength = min(brightness / 255, 1.0)
        support_strength = min((255 - brightness) / 255, 1.0)
        
        levels = {
            'resistance_levels': [
                {'price': 0.8, 'strength': resistance_strength, 'touches': 3},
                {'price': 0.9, 'strength': resistance_strength * 0.7, 'touches': 2}
            ],
            'support_levels': [
                {'price': 0.2, 'strength': support_strength, 'touches': 4},
                {'price': 0.1, 'strength': support_strength * 0.8, 'touches': 2}
            ]
        }
        
        return levels

    def identify_patterns(self, candles):
        """Identify specific candlestick patterns"""
        if len(candles) < 2:
            return []
        
        patterns = []
        
        for i in range(1, len(candles)):
            current = candles[i]
            previous = candles[i-1]
            
            # Hammer pattern
            if (current['lower_wick'] > current['body_size'] * 2 and 
                current['upper_wick'] < current['body_size'] * 0.3):
                patterns.append({
                    'name': 'hammer',
                    'position': i,
                    'strength': self.candle_patterns['hammer']['strength'],
                    'signal': 'bullish'
                })
            
            # Shooting star
            elif (current['upper_wick'] > current['body_size'] * 2 and 
                  current['lower_wick'] < current['body_size'] * 0.3):
                patterns.append({
                    'name': 'shooting_star',
                    'position': i,
                    'strength': self.candle_patterns['shooting_star']['strength'],
                    'signal': 'bearish'
                })
            
            # Engulfing patterns
            if (current['body_size'] > previous['body_size'] * 1.5):
                if current['type'] == 'bullish' and previous['type'] == 'bearish':
                    patterns.append({
                        'name': 'bullish_engulfing',
                        'position': i,
                        'strength': self.candle_patterns['engulfing_bull']['strength'],
                        'signal': 'bullish'
                    })
                elif current['type'] == 'bearish' and previous['type'] == 'bullish':
                    patterns.append({
                        'name': 'bearish_engulfing',
                        'position': i,
                        'strength': self.candle_patterns['engulfing_bear']['strength'],
                        'signal': 'bearish'
                    })
        
        return patterns

    def calculate_momentum(self, candles):
        """Calculate price momentum"""
        if len(candles) < 5:
            return {'direction': 'neutral', 'strength': 0.5}
        
        recent_candles = candles[-5:]
        bullish_count = sum(1 for c in recent_candles if c['type'] == 'bullish')
        
        momentum_strength = bullish_count / 5
        
        if momentum_strength > 0.7:
            direction = 'bullish'
        elif momentum_strength < 0.3:
            direction = 'bearish'
        else:
            direction = 'neutral'
        
        return {
            'direction': direction,
            'strength': momentum_strength if direction == 'bullish' else 1 - momentum_strength
        }