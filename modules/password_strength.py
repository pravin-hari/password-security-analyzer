"""
Password Strength Analyzer Module
Analyzes password security based on multiple parameters.
"""

import re
from typing import Dict, List, Tuple


class PasswordStrengthAnalyzer:
    """Analyzes password strength based on various security rules."""
    
    def __init__(self):
        self.min_length = 8
        self.max_length = 128
    
    def analyze(self, password: str) -> Dict:
        """Analyze password and return strength metrics."""
        if not password:
            return {
                'score': 0,
                'strength': 'Empty',
                'level': 0,
                'suggestions': ['Please enter a password'],
                'details': {}
            }
        
        checks = {
            'length': self._check_length(password),
            'uppercase': self._check_uppercase(password),
            'lowercase': self._check_lowercase(password),
            'numbers': self._check_numbers(password),
            'special_chars': self._check_special_chars(password),
            'no_common_patterns': self._check_common_patterns(password),
            'no_repeated_chars': self._check_repeated_chars(password)
        }
        
        score = sum(check['passed'] for check in checks.values())
        strength, level = self._get_strength_level(score)
        suggestions = self._generate_suggestions(checks, score)
        
        return {
            'score': score,
            'strength': strength,
            'level': level,
            'suggestions': suggestions,
            'details': checks
        }
    
    def _check_length(self, password: str) -> Dict:
        length = len(password)
        passed = length >= self.min_length
        return {
            'passed': passed,
            'message': f"Length: {length} characters",
            'required': f"Minimum {self.min_length} characters",
            'score_value': 1 if passed else 0
        }
    
    def _check_uppercase(self, password: str) -> Dict:
        has_upper = bool(re.search(r'[A-Z]', password))
        return {
            'passed': has_upper,
            'message': "Contains uppercase letters" if has_upper else "No uppercase letters",
            'required': "Add uppercase letters (A-Z)",
            'score_value': 1 if has_upper else 0
        }
    
    def _check_lowercase(self, password: str) -> Dict:
        has_lower = bool(re.search(r'[a-z]', password))
        return {
            'passed': has_lower,
            'message': "Contains lowercase letters" if has_lower else "No lowercase letters",
            'required': "Add lowercase letters (a-z)",
            'score_value': 1 if has_lower else 0
        }
    
    def _check_numbers(self, password: str) -> Dict:
        has_numbers = bool(re.search(r'\d', password))
        return {
            'passed': has_numbers,
            'message': "Contains numbers" if has_numbers else "No numbers",
            'required': "Add numbers (0-9)",
            'score_value': 1 if has_numbers else 0
        }
    
    def _check_special_chars(self, password: str) -> Dict:
        has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:\'",.<>?/`~\\]', password))
        return {
            'passed': has_special,
            'message': "Contains special characters" if has_special else "No special characters",
            'required': "Add special characters (!@#$%^&*)",
            'score_value': 1 if has_special else 0
        }
    
    def _check_common_patterns(self, password: str) -> Dict:
        common_patterns = [
            r'^123', r'456', r'789', r'012',
            r'abc', r'xyz',
            r'(.)\1{2,}',
            r'password', r'admin', r'root',
            r'qwerty', r'asdf', r'zxcv',
        ]
        has_pattern = any(re.search(pattern, password.lower()) for pattern in common_patterns)
        return {
            'passed': not has_pattern,
            'message': "No common patterns detected" if not has_pattern else "Contains common patterns",
            'required': "Avoid common patterns",
            'score_value': 1 if not has_pattern else 0
        }
    
    def _check_repeated_chars(self, password: str) -> Dict:
        has_repeated = bool(re.search(r'(.)\1{2,}', password))
        return {
            'passed': not has_repeated,
            'message': "No excessive repetition" if not has_repeated else "Contains repeated characters",
            'required': "Avoid repeating characters",
            'score_value': 1 if not has_repeated else 0
        }
    
    def _get_strength_level(self, score: int) -> Tuple[str, int]:
        if score <= 2:
            return 'Weak', 1
        elif score <= 4:
            return 'Medium', 2
        else:
            return 'Strong', 3
    
    def _generate_suggestions(self, checks: Dict, score: int) -> List[str]:
        suggestions = []
        if not checks['length']['passed']:
            suggestions.append(f"Increase password length to at least {self.min_length} characters")
        if not checks['uppercase']['passed']:
            suggestions.append("Add uppercase letters (A-Z)")
        if not checks['lowercase']['passed']:
            suggestions.append("Add lowercase letters (a-z)")
        if not checks['numbers']['passed']:
            suggestions.append("Add numbers (0-9)")
        if not checks['special_chars']['passed']:
            suggestions.append("Add special characters (!@#$%^&*)")
        if not checks['no_common_patterns']['passed']:
            suggestions.append("Avoid common patterns like '123', 'abc', 'password'")
        if not checks['no_repeated_chars']['passed']:
            suggestions.append("Avoid repeating characters")
        if score >= 5:
            suggestions.append("Great password! Consider making it even longer for extra security")
        return suggestions


def analyze_password(password: str) -> Dict:
    """Analyze password strength."""
    analyzer = PasswordStrengthAnalyzer()
    return analyzer.analyze(password)

