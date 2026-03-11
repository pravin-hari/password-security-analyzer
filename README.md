# Intelligent Password Security Analyzer

A web-based cybersecurity tool that analyzes password strength, predicts password cracking time using AI techniques, checks if the password has been exposed in leaked databases, and simulates real-time password attacks to educate users about password security risks.

## Features

### 1. Password Strength Analyzer
- Evaluates password security based on multiple parameters
- Checks: length, uppercase, lowercase, numbers, special characters, patterns
- Provides strength score (Weak/Medium/Strong)

### 2. AI Crack Time Predictor
- Predicts how long it would take to crack a password
- Uses entropy calculations
- Provides estimates for different attack scenarios:
  - Online attacks
  - Offline attacks (slow/fast hash)
  - GPU cluster attacks
  - Supercomputer attacks

### 3. Dark Web Password Leak Checker
- Checks if password has been found in data breaches
- Uses HaveIBeenPwned API with k-Anonymity model
- Provides severity rating and recommendations

### 4. Attack Simulator
- Simulates real-world hacking techniques:
  - Dictionary Attack
  - Brute Force Attack
  - Rainbow Table Attack
- Provides overall security score

## Project Structure

```
password-security-analyzer/
├── app.py                    # Flask backend
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── templates/
│   └── index.html           # Frontend HTML
├── static/
│   ├── style.css           # Styling
│   └── script.js           # Frontend JavaScript
├── modules/
│   ├── __init__.py
│   ├── password_strength.py      # Password strength analysis
│   ├── crack_time_predictor.py   # AI-based crack time prediction
│   ├── breach_checker.py         # HaveIBeenPwned API integration
│   └── attack_simulator.py       # Attack simulation
└── dataset/
    └── common_passwords.txt      # Common passwords for dictionary attack
```

## Installation

1. Navigate to the project directory:
   ```bash
   cd password-security-analyzer
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Enter a password to analyze and view the results.

## API Endpoints

- `GET /` - Main page
- `POST /analyze` - Analyze password strength
- `POST /simulate` - Run attack simulation
- `POST /full-analysis` - Complete analysis (all features)
- `GET /health` - Health check endpoint

## Example API Usage

```bash
# Full analysis
curl -X POST http://localhost:5000/full-analysis \
  -H "Content-Type: application/json" \
  -d '{"password": "MySecureP@ss123"}'
```

## Security Concepts Demonstrated

- Password entropy
- Hashing techniques (SHA-1 for breach checking)
- Brute-force attacks
- Dictionary attacks
- Rainbow table attacks
- Data breach detection
- Password best practices

## Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python, Flask
- **Security**: hashlib, bcrypt
- **API**: HaveIBeenPwned

## Disclaimer

This tool is for educational purposes only. It demonstrates password security concepts and should not be used as the sole method for password security assessment. Always follow best practices for password management and use password managers.

## License

MIT License

