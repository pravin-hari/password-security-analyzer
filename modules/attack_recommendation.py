"""
Password Attack Recommendation Engine
Detects the most effective attack method for cracking a password.
"""

import re
from typing import Dict
from pathlib import Path


class AttackRecommendationEngine:
    """Detects best attack method and estimates crack time."""
    
    def __init__(self):
        self.common_passwords = self._load_common_passwords()
        self.guesses_per_second = 1_000_000_000  # 1 billion per second
    
    def _load_common_passwords(self):
        """Load common passwords from dataset."""
        try:
            dataset_path = Path(__file__).parent.parent / "dataset" / "common_passwords.txt"
            if dataset_path.exists():
                with open(dataset_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return [line.strip().lower() for line in f if line.strip()]
        except Exception:
            pass
        return [
            "123456", "password", "12345678", "qwerty", "123456789",
            "12345", "1234", "111111", "1234567", "dragon",
            "123123", "baseball", "iloveyou", "trustno1", "sunshine",
            "master", "welcome", "shadow", "ashley", "football",
            "jesus", "michael", "ninja", "mustang", "password1",
            "admin", "letmein", "login", "starwars", "hello",
            "charlie", "donald", "princess", "qwerty123", "abc123"
        ]
    
    def detect_attack(self, password: str) -> Dict:
        """Detect the best attack method for the password."""
        if not password:
            return self._empty_result()
        
        password_lower = password.lower()
        
        # Check for Common Password Attack
        if password_lower in self.common_passwords:
            return {
                'best_attack': 'Common Password Attack',
                'description': 'Password found in common password database',
                'estimated_crack_time': 'Instant',
                'crack_time_seconds': 0,
                'difficulty': 'Extremely Easy',
                'probability': '100%',
                'recommendation': 'Never use common passwords. Use a unique combination.'
            }
        
        # Check for Dictionary Attack (contains common words)
        dictionary_words = [
            'dragon', 'football', 'monkey', 'sunshine', 'master', 'welcome',
            'shadow', 'ashley', 'jesus', 'michael', 'ninja', 'mustang',
            'charlie', 'donald', 'princess', 'admin', 'login', 'starwars',
            'hello', 'baseball', 'iloveyou', 'trustno1', 'superman', 'batman'
        ]
        
        contains_word = any(word in password_lower for word in dictionary_words)
        
        # Check for Hybrid Attack (word + numbers)
        has_letters = bool(re.search(r'[a-zA-Z]', password))
        has_numbers = bool(re.search(r'\d', password))
        has_word_number_pattern = has_letters and has_numbers
        
        if has_word_number_pattern and contains_word:
            char_set_size = self._get_char_set_size(password)
            combinations = char_set_size ** len(password)
            seconds = combinations / self.guesses_per_second
            
            return {
                'best_attack': 'Hybrid Attack',
                'description': 'Password contains word + numbers pattern',
                'estimated_crack_time': self._format_time(seconds),
                'crack_time_seconds': seconds,
                'difficulty': 'Easy' if seconds < 60 else 'Moderate',
                'probability': 'High' if seconds < 3600 else 'Medium',
                'recommendation': 'Avoid using common words with numbers. Use random characters.'
            }
        
        # Check for Dictionary Attack (only letters)
        if password.isalpha():
            return {
                'best_attack': 'Dictionary Attack',
                'description': 'Password contains only alphabetical characters',
                'estimated_crack_time': 'Few Seconds',
                'crack_time_seconds': 5,
                'difficulty': 'Easy',
                'probability': 'High',
                'recommendation': 'Add numbers and special characters to increase complexity.'
            }
        
        # Check for Hybrid Attack (letters + numbers without words)
        if has_word_number_pattern and not contains_word:
            char_set_size = self._get_char_set_size(password)
            combinations = char_set_size ** len(password)
            seconds = combinations / self.guesses_per_second
            
            return {
                'best_attack': 'Hybrid Attack',
                'description': 'Password contains letters and numbers',
                'estimated_crack_time': self._format_time(seconds),
                'crack_time_seconds': seconds,
                'difficulty': self._get_difficulty(seconds),
                'probability': 'Medium',
                'recommendation': 'Consider adding special characters for better security.'
            }
        
        # Brute Force Attack (random characters)
        char_set_size = self._get_char_set_size(password)
        combinations = char_set_size ** len(password)
        seconds = combinations / self.guesses_per_second
        
        return {
            'best_attack': 'Brute Force Attack',
            'description': 'Password uses random character combination',
            'estimated_crack_time': self._format_time(seconds),
            'crack_time_seconds': seconds,
            'difficulty': self._get_difficulty(seconds),
            'probability': 'Low' if seconds > 31536000 else 'Medium',
            'recommendation': 'Good password! Consider making it longer for extra security.'
        }
    
    def _get_char_set_size(self, password: str) -> int:
        """Calculate character set size."""
        size = 0
        if any(c.islower() for c in password):
            size += 26
        if any(c.isupper() for c in password):
            size += 26
        if any(c.isdigit() for c in password):
            size += 10
        if any(c in '!@#$%^&*()_+-=[]{}|;:\'",.<>?/`~\\' for c in password):
            size += 32
        return size if size > 0 else 1
    
    def _format_time(self, seconds: float) -> str:
        """Format time duration."""
        if seconds < 1:
            return "Instant"
        elif seconds < 60:
            return f"{int(seconds)} seconds"
        elif seconds < 3600:
            return f"{int(seconds / 60)} minutes"
        elif seconds < 86400:
            return f"{int(seconds / 3600)} hours"
        elif seconds < 31536000:
            return f"{int(seconds / 86400)} days"
        elif seconds < 31536000 * 100:
            return f"{int(seconds / 31536000)} years"
        else:
            return "Millions of years"
    
    def _get_difficulty(self, seconds: float) -> str:
        """Get difficulty rating."""
        if seconds < 1:
            return 'Extremely Easy'
        elif seconds < 60:
            return 'Easy'
        elif seconds < 3600:
            return 'Moderate'
        elif seconds < 86400:
            return 'Difficult'
        elif seconds < 31536000:
            return 'Very Difficult'
        elif seconds < 31536000 * 100:
            return 'Extremely Difficult'
        else:
            return 'Nearly Impossible'
    
    def _empty_result(self) -> Dict:
        return {
            'best_attack': 'N/A',
            'description': 'Please enter a password',
            'estimated_crack_time': 'N/A',
            'crack_time_seconds': 0,
            'difficulty': 'N/A',
            'probability': 'N/A',
            'recommendation': ''
        }


def detect_best_attack(password: str) -> Dict:
    """Detect best attack method for password."""
    engine = AttackRecommendationEngine()
    return engine.detect_attack(password)

