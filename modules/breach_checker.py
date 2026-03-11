"""
Dark Web Password Leak Checker
Checks if a password has been found in data breaches using HaveIBeenPwned API.
"""

import hashlib
import requests
from typing import Dict


class BreachChecker:
    """Checks password against breach databases using HaveIBeenPwned API."""
    
    API_URL = "https://api.pwnedpasswords.com/range/"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Password-Security-Analyzer'
        })
    
    def check(self, password: str) -> Dict:
        """Check if password has been in any data breaches."""
        if not password:
            return self._empty_result()
        
        try:
            sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
            prefix = sha1_hash[:5]
            suffix = sha1_hash[5:]
            
            response = self.session.get(f"{self.API_URL}{prefix}", timeout=10)
            
            if response.status_code == 200:
                hashes = response.text.splitlines()
                breach_count = self._find_matching_hash(suffix, hashes)
                
                if breach_count > 0:
                    return {
                        'found': True,
                        'count': breach_count,
                        'severity': self._get_severity(breach_count),
                        'message': f"This password has appeared in {breach_count:,} data breaches",
                        'recommendation': self._get_recommendation(breach_count),
                        'safe': False
                    }
                else:
                    return {
                        'found': False,
                        'count': 0,
                        'severity': 'Safe',
                        'message': "This password hasn't been found in any known data breaches",
                        'recommendation': "Safe to use, but always use unique passwords for each account",
                        'safe': True
                    }
            else:
                return self._error_result(f"API error: {response.status_code}")
                
        except requests.exceptions.Timeout:
            return self._error_result("Request timed out. Please try again.")
        except requests.exceptions.RequestException as e:
            return self._error_result(f"Connection error: {str(e)}")
        except Exception as e:
            return self._error_result(f"Unexpected error: {str(e)}")
    
    def _find_matching_hash(self, suffix: str, hashes: list) -> int:
        for line in hashes:
            try:
                hash_part, count_part = line.split(':')
                if hash_part == suffix:
                    return int(count_part)
            except (ValueError, IndexError):
                continue
        return 0
    
    def _get_severity(self, count: int) -> str:
        if count == 0:
            return 'Safe'
        elif count < 10:
            return 'Low Risk'
        elif count < 100:
            return 'Medium Risk'
        elif count < 1000:
            return 'High Risk'
        elif count < 10000:
            return 'Very High Risk'
        else:
            return 'Critical'
    
    def _get_recommendation(self, count: int) -> str:
        if count < 10:
            return "Consider using a different password as a precaution."
        elif count < 100:
            return "This password is moderately common. Use a stronger, unique password."
        elif count < 1000:
            return "This password is commonly used by hackers. Change it immediately."
        elif count < 10000:
            return "Extremely common password! Never use this password."
        else:
            return "CRITICAL: This password is extremely exposed. Change it NOW!"
    
    def _empty_result(self) -> Dict:
        return {
            'found': False,
            'count': 0,
            'severity': 'N/A',
            'message': 'Please enter a password to check',
            'recommendation': '',
            'safe': None
        }
    
    def _error_result(self, error_message: str) -> Dict:
        return {
            'found': False,
            'count': -1,
            'severity': 'Error',
            'message': error_message,
            'recommendation': 'Please try again later',
            'safe': None,
            'error': True
        }


def check_breach(password: str) -> Dict:
    """Check password breach status."""
    checker = BreachChecker()
    return checker.check(password)

