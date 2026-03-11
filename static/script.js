/**
 * Password Security Analyzer - JavaScript
 * Hacker/Cyber Theme with Terminal Console Output
 */

// DOM Elements
const passwordInput = document.getElementById('passwordInput');
const toggleVisibilityBtn = document.getElementById('toggleVisibility');
const analyzeBtn = document.getElementById('analyzeBtn');
const clearBtn = document.getElementById('clearBtn');
const loadingState = document.getElementById('loadingState');
const resultsDashboard = document.getElementById('resultsDashboard');

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    toggleVisibilityBtn.addEventListener('click', togglePasswordVisibility);
    analyzeBtn.addEventListener('click', analyzePassword);
    clearBtn.addEventListener('click', clearResults);
    
    passwordInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            analyzePassword();
        }
    });
    
    let debounceTimer;
    passwordInput.addEventListener('input', () => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            if (passwordInput.value.length > 0) {
                analyzePassword();
            }
        }, 500);
    });
});

function togglePasswordVisibility() {
    const type = passwordInput.type === 'password' ? 'text' : 'password';
    passwordInput.type = type;
    const icon = toggleVisibilityBtn.querySelector('i');
    icon.className = type === 'password' ? 'fas fa-eye' : 'fas fa-eye-slash';
}

async function analyzePassword() {
    const password = passwordInput.value;
    
    if (!password) {
        showError('Please enter a password to analyze');
        return;
    }
    
    loadingState.classList.remove('hidden');
    resultsDashboard.classList.add('hidden');
    
    try {
        const response = await fetch('/full-analysis', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ password: password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data);
        } else {
            showError(data.error || 'An error occurred during analysis');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to connect to server. Please try again.');
    } finally {
        loadingState.classList.add('hidden');
        resultsDashboard.classList.remove('hidden');
    }
}

function displayResults(data) {
    const { strength, crack_time, breach, simulation, attack_recommendation } = data;
    
    displayStrength(strength);
    displayCrackTime(crack_time);
    displayBreachStatus(breach);
    displayAttackRecommendation(attack_recommendation);
    displayAttackSimulation(simulation, passwordInput.value);
    displaySuggestions(strength, breach, simulation);
}

function displayStrength(strength) {
    const strengthBar = document.getElementById('strengthBar');
    const strengthLabel = document.getElementById('strengthLabel');
    const strengthScore = document.getElementById('strengthScore');
    const strengthDetails = document.getElementById('strengthDetails');
    
    strengthBar.className = 'strength-fill ' + strength.strength.toLowerCase();
    strengthLabel.textContent = strength.strength;
    strengthLabel.className = 'strength-label ' + strength.strength.toLowerCase();
    strengthScore.textContent = `Score: ${strength.score}/7`;
    
    strengthDetails.innerHTML = '';
    const checks = strength.details;
    
    const checkItems = [
        { key: 'length', label: 'Length check' },
        { key: 'uppercase', label: 'Uppercase letters' },
        { key: 'lowercase', label: 'Lowercase letters' },
        { key: 'numbers', label: 'Numbers' },
        { key: 'special_chars', label: 'Special characters' },
        { key: 'no_common_patterns', label: 'No common patterns' },
        { key: 'no_repeated_chars', label: 'No repeated characters' }
    ];
    
    checkItems.forEach(item => {
        const check = checks[item.key];
        const li = document.createElement('li');
        if (check.passed) {
            li.innerHTML = `<i class="fas fa-check"></i> ${check.message}`;
        } else {
            li.innerHTML = `<i class="fas fa-times"></i> ${check.required}`;
        }
        strengthDetails.appendChild(li);
    });
}

function displayCrackTime(crackTime) {
    const crackTimeValue = document.getElementById('crackTimeValue');
    const entropyValue = document.getElementById('entropyValue');
    const combinationsValue = document.getElementById('combinationsValue');
    const difficultyValue = document.getElementById('difficultyValue');
    const scenarioGrid = document.getElementById('scenarioGrid');
    
    crackTimeValue.textContent = crackTime.overall_time;
    entropyValue.textContent = crackTime.entropy + ' bits';
    combinationsValue.textContent = crackTime.combinations_formatted;
    difficultyValue.textContent = crackTime.difficulty;
    
    scenarioGrid.innerHTML = '';
    const scenarios = crackTime.crack_times;
    
    const scenarioLabels = {
        'online': 'Online Attack',
        'offline_slow': 'Offline (Slow Hash)',
        'offline_fast': 'Offline (Fast Hash)',
        'gpu_cluster': 'GPU Cluster',
        'supercomputer': 'Supercomputer'
    };
    
    for (const [key, time] of Object.entries(scenarios)) {
        const div = document.createElement('div');
        div.className = 'scenario-item';
        div.innerHTML = `
            <span class="scenario-label">${scenarioLabels[key] || key}</span>
            <span class="scenario-time">${time}</span>
        `;
        scenarioGrid.appendChild(div);
    }
}

function displayBreachStatus(breach) {
    const breachStatus = document.getElementById('breachStatus');
    const breachIcon = breachStatus.querySelector('.breach-icon');
    const breachMessage = document.getElementById('breachMessage');
    const breachCount = document.getElementById('breachCount');
    const breachRecommendation = document.getElementById('breachRecommendation');
    
    breachIcon.className = 'breach-icon';
    
    if (breach.safe === true) {
        breachIcon.classList.add('safe');
        breachIcon.innerHTML = '<i class="fas fa-check-circle"></i>';
        breachMessage.textContent = breach.message;
        breachCount.textContent = '';
    } else if (breach.safe === false) {
        breachIcon.classList.add('danger');
        breachIcon.innerHTML = '<i class="fas fa-exclamation-triangle"></i>';
        breachMessage.textContent = breach.message;
        breachCount.textContent = `${breach.count.toLocaleString()} breaches found`;
    } else {
        breachIcon.innerHTML = '<i class="fas fa-question-circle"></i>';
        breachMessage.textContent = 'Enter a password to check';
        breachCount.textContent = '';
    }
    
    breachRecommendation.innerHTML = `<p>${breach.recommendation}</p>`;
}

// Display Attack Recommendation Engine results
function displayAttackRecommendation(attackRec) {
    const bestAttack = document.getElementById('bestAttack');
    const attackDescription = document.getElementById('attackDescription');
    const attackDifficulty = document.getElementById('attackDifficulty');
    const attackProbability = document.getElementById('attackProbability');
    const attackRecommendation = document.getElementById('attackRecommendation');
    
    bestAttack.textContent = attackRec.best_attack;
    attackDescription.textContent = attackRec.description;
    attackDifficulty.textContent = attackRec.difficulty;
    attackProbability.textContent = attackRec.probability;
    attackRecommendation.textContent = attackRec.recommendation;
    
    // Color coding based on difficulty
    const difficultyColors = {
        'Extremely Easy': '#FF4C4C',
        'Easy': '#FF6B6B',
        'Moderate': '#FFD700',
        'Difficult': '#FFA500',
        'Very Difficult': '#9ACD32',
        'Extremely Difficult': '#32CD32',
        'Nearly Impossible': '#00FF41'
    };
    attackDifficulty.style.color = difficultyColors[attackRec.difficulty] || '#00FF41';
    
    const probColors = {
        '100%': '#FF4C4C',
        'High': '#FF6B6B',
        'Medium': '#FFD700',
        'Low': '#32CD32'
    };
    attackProbability.style.color = probColors[attackRec.probability] || '#00FF41';
}

function displayAttackSimulation(simulation, password) {
    const simulationLog = document.getElementById('simulationLog');
    const dictionaryResult = document.getElementById('dictionaryResult');
    const bruteForceResult = document.getElementById('bruteForceResult');
    const rainbowResult = document.getElementById('rainbowResult');
    const securityScoreValue = document.getElementById('securityScoreValue');
    const securityRating = document.getElementById('securityRating');
    const scoreCircle = document.getElementById('scoreCircle');
    
    simulationLog.innerHTML = '';
    
    const logMessages = [
        { type: 'info', text: '[INIT] Starting attack simulation framework...' },
        { type: 'info', text: '[LOAD] Loading password dictionary database...' },
        { type: 'info', text: '[LOAD] Loading rainbow table hashes...' },
        { type: 'info', text: '[READY] All modules initialized successfully' },
        { type: 'info', text: '[ATTACK] Initiating dictionary attack...' },
    ];
    
    const dictionary = simulation.dictionary_attack;
    if (dictionary.success) {
        logMessages.push({ type: 'warning', text: `[TRY] ${password}` });
        logMessages.push({ type: 'danger', text: `[CRACKED] Password found in ${dictionary.attempts} attempts` });
    } else {
        logMessages.push({ type: 'success', text: `[FAILED] Dictionary attack unsuccessful` });
    }
    
    logMessages.push({ type: 'info', text: '[ATTACK] Initiating brute force attack...' });
    
    const bruteForce = simulation.brute_force_attack;
    logMessages.push({ type: 'info', text: `[CALC] Possible combinations: ${bruteForce.combinations_formatted}` });
    logMessages.push({ type: 'info', text: `[ESTIMATE] Time to crack: ${bruteForce.estimated_time}` });
    
    const rainbow = simulation.rainbow_table_attack;
    if (rainbow.vulnerable) {
        logMessages.push({ type: 'danger', text: '[WARNING] Rainbow table vulnerability detected!' });
    } else {
        logMessages.push({ type: 'success', text: '[SECURE] Password not in rainbow table range' });
    }
    
    logMessages.push({ type: 'info', text: '[ANALYSIS] Computing security metrics...' });
    logMessages.push({ type: 'success', text: '[COMPLETE] Analysis finished successfully' });
    
    logMessages.forEach((msg, index) => {
        const p = document.createElement('p');
        p.className = 'console-line ' + msg.type;
        p.textContent = msg.text;
        p.style.animationDelay = `${index * 0.15}s`;
        simulationLog.appendChild(p);
    });
    
    dictionaryResult.textContent = dictionary.success ? 
        `CRACKED in ${dictionary.attempts} attempts` : 
        'Failed - Not in dictionary';
    dictionaryResult.style.color = dictionary.success ? '#FF4C4C' : '#00FF41';
    
    bruteForceResult.textContent = `${bruteForce.estimated_time} (${bruteForce.success_probability})`;
    
    rainbowResult.textContent = rainbow.vulnerable ? 
        'Vulnerable - At risk' : 
        'Protected - Safe';
    rainbowResult.style.color = rainbow.vulnerable ? '#FF4C4C' : '#00FF41';
    
    const combined = simulation.combined_analysis;
    securityScoreValue.textContent = combined.security_score;
    securityRating.textContent = combined.rating;
    securityRating.className = combined.rating.toLowerCase();
    
    const score = combined.security_score;
    const circumference = 2 * Math.PI * 45;
    const offset = circumference - (score / 100) * circumference;
    
    setTimeout(() => {
        scoreCircle.style.strokeDashoffset = offset;
        if (score >= 80) {
            scoreCircle.style.stroke = '#00FF41';
        } else if (score >= 60) {
            scoreCircle.style.stroke = '#00FF41';
        } else if (score >= 40) {
            scoreCircle.style.stroke = '#FFD700';
        } else {
            scoreCircle.style.stroke = '#FF4C4C';
        }
    }, 100);
}

function displaySuggestions(strength, breach, simulation) {
    const suggestionsList = document.getElementById('suggestionsList');
    
    suggestionsList.innerHTML = '';
    
    const suggestions = [];
    
    if (strength.suggestions) {
        strength.suggestions.forEach(s => {
            if (!s.includes('Great password')) {
                suggestions.push(s);
            }
        });
    }
    
    if (breach.safe === false) {
        suggestions.push('This password has been found in data breaches. Change it immediately!');
    }
    
    const simSuggestions = simulation.combined_analysis.recommendations || [];
    simSuggestions.forEach(s => {
        if (!suggestions.includes(s)) {
            suggestions.push(s);
        }
    });
    
    if (suggestions.length < 3) {
        suggestions.push('Use a password manager to generate and store unique passwords');
        suggestions.push('Enable two-factor authentication whenever possible');
    }
    
    suggestions.slice(0, 6).forEach(suggestion => {
        const li = document.createElement('li');
        li.innerHTML = `
            <i class="fas fa-lightbulb"></i>
            <p>${suggestion}</p>
        `;
        suggestionsList.appendChild(li);
    });
}

function clearResults() {
    passwordInput.value = '';
    resultsDashboard.classList.add('hidden');
    loadingState.classList.add('hidden');
    
    document.getElementById('strengthBar').className = 'strength-fill';
    document.getElementById('strengthLabel').textContent = '-';
    document.getElementById('strengthScore').textContent = '-';
    document.getElementById('strengthDetails').innerHTML = '';
    document.getElementById('crackTimeValue').textContent = '-';
    document.getElementById('entropyValue').textContent = '-';
    document.getElementById('combinationsValue').textContent = '-';
    document.getElementById('difficultyValue').textContent = '-';
    document.getElementById('scenarioGrid').innerHTML = '';
    
    document.getElementById('bestAttack').textContent = '-';
    document.getElementById('attackDescription').textContent = '-';
    document.getElementById('attackDifficulty').textContent = '-';
    document.getElementById('attackProbability').textContent = '-';
    document.getElementById('attackRecommendation').textContent = '-';
    
    const breachIcon = document.querySelector('.breach-icon');
    breachIcon.className = 'breach-icon';
    breachIcon.innerHTML = '<i class="fas fa-question-circle"></i>';
    document.getElementById('breachMessage').textContent = 'Enter a password to check';
    document.getElementById('breachCount').textContent = '';
    document.getElementById('breachRecommendation').innerHTML = '';
    
    document.getElementById('simulationLog').innerHTML = '<p class="console-line">Waiting for password analysis...</p>';
    document.getElementById('dictionaryResult').textContent = '-';
    document.getElementById('bruteForceResult').textContent = '-';
    document.getElementById('rainbowResult').textContent = '-';
    document.getElementById('securityScoreValue').textContent = '-';
    document.getElementById('securityRating').textContent = '-';
    document.getElementById('scoreCircle').style.strokeDashoffset = 283;
    
    document.getElementById('suggestionsList').innerHTML = '';
}

function showError(message) {
    loadingState.classList.add('hidden');
    resultsDashboard.classList.remove('hidden');
    console.error(message);
}

