"""
AI-Based Password Crack Time Predictor
Predicts how long it would take to crack a password using entropy calculations.
"""

import math
from typing import Dict


class CrackTimePredictor:
    """Predicts password cracking time using entropy and mathematical models."""
    
    def __init__(self):
        self.guesses_per_second = {
            'offline_slow': 1e4,
            'offline_fast': 1e10,
            'online': 100,
            'gpu_cluster': 1e12,
            'supercomputer': 1e14
        }
        self.char_sets = {
            'lowercase': 26,
            'uppercase': 26,
            'digits': 10,
            'special': 32
        }
    
    def predict(self, password: str) -> Dict:
        """Predict cracking time for a password."""
        if not password:
            return self._empty_result()
        
        entropy = self._calculate_entropy(password)
        char_set_size = self._get_char_set_size(password)
        combinations = char_set_size ** len(password)
        avg_guesses = combinations / 2
        
        crack_times = {}
        for scenario, gps in self.guesses_per_second.items():
            seconds = avg_guesses / gps
            crack_times[scenario] = self._format_time(seconds)
        
        overall_time = self._calculate_overall_time(avg_guesses)
        difficulty = self._get_difficulty(entropy)
        
        return {
            'entropy': round(entropy, 2),
            'char_set_size': char_set_size,
            'combinations': combinations,
            'combinations_formatted': self._format_number(combinations),
            'crack_times': crack_times,
            'overall_time': overall_time,
            'difficulty': difficulty,
            'recommendation': self._get_recommendation(difficulty)
        }
    
    def _calculate_entropy(self, password: str) -> float:
        char_set_size = self._get_char_set_size(password)
        entropy = len(password) * math.log2(char_set_size) if char_set_size > 0 else 0
        return entropy
    
    def _get_char_set_size(self, password: str) -> int:
        size = 0
        if any(c.islower() for c in password):
            size += self.char_sets['lowercase']
        if any(c.isupper() for c in password):
            size += self.char_sets['uppercase']
        if any(c.isdigit() for c in password):
            size += self.char_sets['digits']
        if any(c in '!@#$%^&*()_+-=[]{}|;:\'",.<>?/`~\\' for c in password):
            size += self.char_sets['special']
        return size if size > 0 else 1
    
    def _format_time(self, seconds: float) -> str:
        if seconds < 1:
            return "Instantly"
        elif seconds < 60:
            return f"{round(seconds)} seconds"
        elif seconds < 3600:
            return f"{round(seconds / 60)} minutes"
        elif seconds < 86400:
            return f"{round(seconds / 3600)} hours"
        elif seconds < 31536000:
            return f"{round(seconds / 86400)} days"
        elif seconds < 31536000 * 100:
            return f"{round(seconds / 31536000)} years"
        elif seconds < 31536000 * 1000000:
            return f"{round(seconds / 31536000 / 1000)} thousand years"
        else:
            return "Millions of years"
    
    def _calculate_overall_time(self, combinations: float) -> str:
        gps = self.guesses_per_second['offline_fast']
        seconds = combinations / gps
        return self._format_time(seconds)
    
    def _format_number(self, num: float) -> str:
        if num < 1000:
            return str(int(num))
        elif num < 1e6:
            return f"{num/1e3:.2f}K"
        elif num < 1e9:
            return f"{num/1e6:.2f}M"
        elif num < 1e12:
            return f"{num/1e9:.2f}B"
        else:
            return f"{num/1e12:.2f}T"
    
    def _get_difficulty(self, entropy: float) -> str:
        if entropy < 28:
            return 'Very Weak'
        elif entropy < 36:
            return 'Weak'
        elif entropy < 60:
            return 'Reasonable'
        elif entropy < 80:
            return 'Strong'
        else:
            return 'Very Strong'
    
    def _get_recommendation(self, difficulty: str) -> str:
        recommendations = {
            'Very Weak': 'This password can be cracked instantly. Use a longer password with mixed characters.',
            'Weak': 'This password is vulnerable. Add more characters and use a mix of types.',
            'Reasonable': 'Decent password but could be improved. Consider making it longer.',
            'Strong': 'Good password! Consider adding a few more characters for extra security.',
            'Very Strong': 'Excellent password! Very difficult to crack.'
        }
        return recommendations.get(difficulty, '')
    
    def _empty_result(self) -> Dict:
        return {
            'entropy': 0,
            'char_set_size': 0,
            'combinations': 0,
            'combinations_formatted': '0',
            'crack_times': {k: 'N/A' for k in self.guesses_per_second.keys()},
            'overall_time': 'N/A',
            'difficulty': 'N/A',
            'recommendation': 'Please enter a password'
        }


def predict_crack_time(password: str) -> Dict:
    """Predict crack time for a password."""
    predictor = CrackTimePredictor()
    return predictor.predict(password)

