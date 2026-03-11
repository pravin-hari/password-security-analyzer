"""
Intelligent Password Security Analyzer with AI-Based Attack Simulation
Flask Backend Application
"""

from flask import Flask, render_template, request, jsonify
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from modules.password_strength import analyze_password
from modules.crack_time_predictor import predict_crack_time
from modules.breach_checker import check_breach
from modules.attack_simulator import simulate_attacks
from modules.attack_recommendation import detect_best_attack

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        
        if not data or 'password' not in data:
            return jsonify({'error': 'Password is required'}), 400
        
        password = data['password']
        
        strength_result = analyze_password(password)
        crack_time_result = predict_crack_time(password)
        attack_recommendation = detect_best_attack(password)
        
        result = {
            'success': True,
            'password': password,
            'strength': strength_result,
            'crack_time': crack_time_result,
            'attack_recommendation': attack_recommendation
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        data = request.get_json()
        
        if not data or 'password' not in data:
            return jsonify({'error': 'Password is required'}), 400
        
        password = data['password']
        simulation_result = simulate_attacks(password)
        
        result = {
            'success': True,
            'password': password,
            'simulation': simulation_result
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/breach-check', methods=['POST'])
def breach_check():
    try:
        data = request.get_json()
        
        if not data or 'password' not in data:
            return jsonify({'error': 'Password is required'}), 400
        
        password = data['password']
        breach_result = check_breach(password)
        
        result = {
            'success': True,
            'password': password,
            'breach': breach_result
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/full-analysis', methods=['POST'])
def full_analysis():
    try:
        data = request.get_json()
        
        if not data or 'password' not in data:
            return jsonify({'error': 'Password is required'}), 400
        
        password = data['password']
        
        strength_result = analyze_password(password)
        crack_time_result = predict_crack_time(password)
        breach_result = check_breach(password)
        simulation_result = simulate_attacks(password)
        attack_recommendation = detect_best_attack(password)
        
        result = {
            'success': True,
            'password': password,
            'strength': strength_result,
            'crack_time': crack_time_result,
            'breach': breach_result,
            'simulation': simulation_result,
            'attack_recommendation': attack_recommendation
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'Password Security Analyzer'
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

