"""
Real-Time Password Attack Simulator
Demonstrates how hackers attempt to crack passwords using various techniques.
"""

import time
from typing import Dict, List
from pathlib import Path


class AttackSimulator:
    """Simulates different password attack scenarios for educational purposes."""
    
    def __init__(self):
        self.common_passwords = self._load_common_passwords()
        self.max_dictionary_attempts = 1000
    
    def _load_common_passwords(self) -> List[str]:
        """Load common passwords from dataset file."""
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
            "charlie", "donald", "princess", "qwerty123", "abc123",
            "password123", "admin123", "root", "toor", "passw0rd"
        ]
    
    def simulate_all(self, password: str) -> Dict:
        """Run all attack simulations."""
        if not password:
            return self._empty_result()
        
        results = {
            'dictionary_attack': self._simulate_dictionary_attack(password),
            'brute_force_attack': self._simulate_brute_force_attack(password),
            'rainbow_table_attack': self._simulate_rainbow_table_attack(password),
            'combined_analysis': self._generate_combined_analysis(password)
        }
        return results
    
    def _simulate_dictionary_attack(self, password: str) -> Dict:
        """Simulate dictionary attack using common passwords."""
        start_time = time.time()
        password_lower = password.lower()
        
        attempts = 0
        found = False
        cracked_at = -1
        
        for i, common_pwd in enumerate(self.common_passwords[:self.max_dictionary_attempts]):
            attempts += 1
            if common_pwd == password_lower:
                found = True
                cracked_at = attempts
                break
            variations = [
                common_pwd + "123",
                common_pwd + "1",
                common_pwd.capitalize(),
                common_pwd.upper(),
                common_pwd + "!",
                common_pwd + "@",
            ]
            for var in variations:
                attempts += 1
                if var == password_lower:
                    found = True
                    cracked_at = attempts
                    break
            if found:
                break
        
        elapsed_time = time.time() - start_time
        
        return {
            'attack_type': 'Dictionary Attack',
            'success': found,
            'attempts': attempts,
            'cracked_at': cracked_at if found else None,
            'time_taken': round(elapsed_time, 4),
            'description': 'Tries common passwords and their variations',
            'recommendation': self._get_dictionary_recommendation(found)
        }
    
    def _simulate_brute_force_attack(self, password: str) -> Dict:
        """Simulate brute force attack."""
        start_time = time.time()
        length = len(password)
        
        char_types = 0
        if any(c.islower() for c in password):
            char_types += 26
        if any(c.isupper() for c in password):
            char_types += 26
        if any(c.isdigit() for c in password):
            char_types += 10
        if any(c in '!@#$%^&*()_+-=[]{}|;:\'",.<>?/`~\\' for c in password):
            char_types += 32
        
        char_types = char_types if char_types > 0 else 1
        total_combinations = char_types ** length
        
        guesses_per_second = 10_000_000_000
        estimated_seconds = (total_combinations / 2) / guesses_per_second
        
        success_probability = self._calculate_success_probability(password)
        elapsed_time = time.time() - start_time
        
        return {
            'attack_type': 'Brute Force Attack',
            'success_probability': success_probability,
            'total_combinations': total_combinations,
            'combinations_formatted': self._format_number(total_combinations),
            'estimated_time': self._format_time(estimated_seconds),
            'estimated_seconds': estimated_seconds,
            'time_taken': round(elapsed_time, 4),
            'description': 'Tries every possible character combination',
            'recommendation': self._get_brute_force_recommendation(estimated_seconds)
        }
    
    def _simulate_rainbow_table_attack(self, password: str) -> Dict:
        """Simulate rainbow table attack."""
        start_time = time.time()
        password_lower = password.lower()
        
        is_vulnerable = (
            len(password) < 8 or 
            password_lower in self.common_passwords[:100] or
            self._is_common_pattern(password)
        )
        
        lookup_time = 0.001 if is_vulnerable else 0.1
        elapsed_time = time.time() - start_time + lookup_time
        
        return {
            'attack_type': 'Rainbow Table Attack',
            'vulnerable': is_vulnerable,
            'description': 'Uses pre-computed hash tables for fast cracking',
            'lookup_time': f"{lookup_time * 1000:.2f} ms" if is_vulnerable else "N/A",
            'recommendation': self._get_rainbow_recommendation(is_vulnerable)
        }
    
    def _generate_combined_analysis(self, password: str) -> Dict:
        """Generate overall security analysis."""
        score = 0
        
        length = len(password)
        if length >= 16:
            score += 30
        elif length >= 12:
            score += 25
        elif length >= 10:
            score += 20
        elif length >= 8:
            score += 15
        else:
            score += 5
        
        char_types = 0
        if any(c.islower() for c in password):
            char_types += 1
        if any(c.isupper() for c in password):
            char_types += 1
        if any(c.isdigit() for c in password):
            char_types += 1
        if any(c in '!@#$%^&*()_+-=[]{}|;:\'",.<>?/`~\\' for c in password):
            char_types += 1
        
        score += char_types * 15
        
        if password.lower() not in self.common_passwords[:100]:
            score += 25
        else:
            score -= 30
        
        score = max(0, min(100, score))
        
        if score >= 80:
            rating = 'Excellent'
        elif score >= 60:
            rating = 'Good'
        elif score >= 40:
            rating = 'Fair'
        elif score >= 20:
            rating = 'Poor'
        else:
            rating = 'Critical'
        
        return {
            'security_score': score,
            'rating': rating,
            'summary': self._get_summary(rating),
            'recommendations': self._get_final_recommendations(password)
        }
    
    def _calculate_success_probability(self, password: str) -> str:
        length = len(password)
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in '!@#$%^&*()_+-=[]{}|;:\'",.<>?/`~\\' for c in password)
        
        type_count = sum([has_lower, has_upper, has_digit, has_special])
        
        if length < 6:
            return "Extremely High"
        elif length < 8:
            return "Very High" if type_count < 3 else "High"
        elif length < 10:
            return "High" if type_count < 3 else "Medium"
        elif length < 12:
            return "Medium" if type_count < 3 else "Low"
        elif length < 14:
            return "Low" if type_count < 3 else "Very Low"
        else:
            return "Extremely Low"
    
    def _is_common_pattern(self, password: str) -> bool:
        import re
        patterns = [r'^123', r'456', r'789', r'012', r'abc', r'xyz', r'(.)\1{2,}', r'qwerty', r'password']
        return any(re.search(pattern, password.lower()) for pattern in patterns)
    
    def _format_time(self, seconds: float) -> str:
        if seconds < 0.001:
            return "Instantly"
        elif seconds < 1:
            return f"{seconds * 1000:.2f} ms"
        elif seconds < 60:
            return f"{seconds:.2f} seconds"
        elif seconds < 3600:
            return f"{seconds / 60:.2f} minutes"
        elif seconds < 86400:
            return f"{seconds / 3600:.2f} hours"
        elif seconds < 31536000:
            return f"{seconds / 86400:.2f} days"
        elif seconds < 31536000 * 1000:
            return f"{seconds / 31536000:.2f} years"
        else:
            return "Millions of years"
    
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
    
    def _get_dictionary_recommendation(self, success: bool) -> str:
        if success:
            return "Use a password that is NOT in any common password list."
        return "Good! Your password is not in common password databases."
    
    def _get_brute_force_recommendation(self, seconds: float) -> str:
        if seconds < 1:
            return "CRITICAL: Use a much longer password with mixed characters!"
        elif seconds < 60:
            return "Very vulnerable. Add more characters and variety."
        elif seconds < 3600:
            return "Vulnerable. Consider making your password longer."
        elif seconds < 86400:
            return "Moderate security. A longer password would be better."
        elif seconds < 31536000:
            return "Decent password but could be improved."
        return "Strong password! Very difficult to crack by brute force."
    
    def _get_rainbow_recommendation(self, vulnerable: bool) -> str:
        if vulnerable:
            return "Use a longer password with unique characters."
        return "Good! Your password is likely safe from rainbow table attacks."
    
    def _get_summary(self, rating: str) -> str:
        summaries = {
            'Excellent': "Your password has excellent security!",
            'Good': "Your password provides good security.",
            'Fair': "Your password is reasonably secure but could be improved.",
            'Poor': "Your password is vulnerable to attacks.",
            'Critical': "Your password is critically weak!"
        }
        return summaries.get(rating, "")
    
    def _get_final_recommendations(self, password: str) -> List[str]:
        recommendations = []
        if len(password) < 12:
            recommendations.append("Use at least 12 characters")
        if not any(c.isupper() for c in password):
            recommendations.append("Add uppercase letters")
        if not any(c.islower() for c in password):
            recommendations.append("Add lowercase letters")
        if not any(c.isdigit() for c in password):
            recommendations.append("Add numbers")
        if not any(c in '!@#$%^&*()_+-=[]{}|;:\'",.<>?/`~\\' for c in password):
            recommendations.append("Add special characters")
        if password.lower() in self.common_passwords[:100]:
            recommendations.append("Avoid common passwords")
        if len(recommendations) == 0:
            recommendations.append("Great password! Consider using a password manager.")
        return recommendations
    
    def _empty_result(self) -> Dict:
        return {
            'dictionary_attack': {'success': None},
            'brute_force_attack': {'estimated_time': 'N/A'},
            'rainbow_table_attack': {'vulnerable': None},
            'combined_analysis': {'rating': 'N/A'}
        }


def simulate_attacks(password: str) -> Dict:
    """Simulate attacks on a password."""
    simulator = AttackSimulator()
    return simulator.simulate_all(password)

