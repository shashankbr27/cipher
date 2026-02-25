"""
LEGACY FLASK APPLICATION - UPDATED WITH AI

This is the original Flask-based implementation of the Cipher Game.
Updated to use Gemini 2.5 Flash for intelligent question evaluation and guess validation.

Uses:
- Gemini 2.5 Flash for AI-powered question answering
- AI-based guess validation (no more regex/fuzzy matching)
- Natural language question processing
"""
from flask import Flask, jsonify, request, render_template_string
import json
import random
import time
import hashlib
from datetime import datetime
import os
import google.generativeai as genai

app = Flask(__name__)

# Initialize Gemini API
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyBdn4OvKVSW5mTPSGr8fwE0WVh9lqlF2z0')
print(f"[INIT] Using API key: {GEMINI_API_KEY[:20]}...")
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-2.5-flash')
print(f"[INIT] Gemini model initialized: gemini-2.5-flash")

# ─────────────────────────────────────────────
#  GAME KNOWLEDGE BASE
# ─────────────────────────────────────────────

ITEMS = {
    "medium": [
        {
            "name": "Phishing Attack",
            "category": "cybersecurity",
            "description": "A social engineering attack using deceptive emails to steal credentials",
            "facts": {
                "is_a_concept": True, "is_physical": False, "is_a_person": False,
                "involves_computers": True, "is_malicious": True, "is_defensive": False,
                "requires_internet": True, "involves_human_error": True, "is_automated": False,
                "predates_2000": True, "is_illegal": True, "is_widely_known": True,
                "is_a_protocol": False, "is_a_tool": False, "involves_deception": True,
                "targets_individuals": True, "targets_organizations": True, "is_an_attack": True,
                "is_network_based": True, "involves_email": True
            }
        },
        {
            "name": "Ransomware",
            "category": "cybersecurity",
            "description": "Malicious software that encrypts files and demands payment for decryption",
            "facts": {
                "is_a_concept": False, "is_physical": False, "is_a_person": False,
                "involves_computers": True, "is_malicious": True, "is_defensive": False,
                "requires_internet": True, "involves_human_error": True, "is_automated": True,
                "predates_2000": False, "is_illegal": True, "is_widely_known": True,
                "is_a_protocol": False, "is_a_tool": True, "involves_deception": False,
                "targets_individuals": True, "targets_organizations": True, "is_an_attack": True,
                "is_network_based": True, "involves_email": False
            }
        },
        {
            "name": "SQL Injection",
            "category": "cybersecurity",
            "description": "An attack that inserts malicious SQL code into queries to manipulate databases",
            "facts": {
                "is_a_concept": True, "is_physical": False, "is_a_person": False,
                "involves_computers": True, "is_malicious": True, "is_defensive": False,
                "requires_internet": True, "involves_human_error": False, "is_automated": True,
                "predates_2000": True, "is_illegal": True, "is_widely_known": True,
                "is_a_protocol": False, "is_a_tool": False, "involves_deception": False,
                "targets_individuals": False, "targets_organizations": True, "is_an_attack": True,
                "is_network_based": True, "involves_email": False
            }
        },
        {
            "name": "Firewall",
            "category": "cybersecurity",
            "description": "A network security device that monitors and filters incoming/outgoing traffic",
            "facts": {
                "is_a_concept": False, "is_physical": True, "is_a_person": False,
                "involves_computers": True, "is_malicious": False, "is_defensive": True,
                "requires_internet": False, "involves_human_error": False, "is_automated": True,
                "predates_2000": True, "is_illegal": False, "is_widely_known": True,
                "is_a_protocol": False, "is_a_tool": True, "involves_deception": False,
                "targets_individuals": False, "targets_organizations": True, "is_an_attack": False,
                "is_network_based": True, "involves_email": False
            }
        },
        {
            "name": "DDoS Attack",
            "category": "cybersecurity",
            "description": "Distributed Denial of Service - flooding a target with traffic to disrupt service",
            "facts": {
                "is_a_concept": True, "is_physical": False, "is_a_person": False,
                "involves_computers": True, "is_malicious": True, "is_defensive": False,
                "requires_internet": True, "involves_human_error": False, "is_automated": True,
                "predates_2000": False, "is_illegal": True, "is_widely_known": True,
                "is_a_protocol": False, "is_a_tool": False, "involves_deception": False,
                "targets_individuals": False, "targets_organizations": True, "is_an_attack": True,
                "is_network_based": True, "involves_email": False
            }
        }
    ],
    "hard": [
        {
            "name": "Stuxnet",
            "category": "historical_cyber_event",
            "description": "First known cyberweapon targeting industrial control systems (Iranian nuclear program, 2010)",
            "facts": {
                "is_a_concept": False, "is_physical": False, "is_a_person": False,
                "involves_computers": True, "is_malicious": True, "is_defensive": False,
                "requires_internet": False, "involves_human_error": True, "is_automated": True,
                "predates_2000": False, "is_illegal": True, "is_widely_known": True,
                "is_a_protocol": False, "is_a_tool": True, "involves_deception": True,
                "targets_individuals": False, "targets_organizations": True, "is_an_attack": True,
                "is_network_based": False, "is_state_sponsored": True, "targets_infrastructure": True,
                "year_approx": 2010
            }
        },
        {
            "name": "Zero-Day Exploit",
            "category": "cybersecurity",
            "description": "An attack targeting an unknown/unpatched software vulnerability before vendors can fix it",
            "facts": {
                "is_a_concept": True, "is_physical": False, "is_a_person": False,
                "involves_computers": True, "is_malicious": True, "is_defensive": False,
                "requires_internet": True, "involves_human_error": False, "is_automated": True,
                "predates_2000": False, "is_illegal": True, "is_widely_known": False,
                "is_a_protocol": False, "is_a_tool": False, "involves_deception": False,
                "targets_individuals": False, "targets_organizations": True, "is_an_attack": True,
                "is_network_based": True, "is_state_sponsored": False, "targets_infrastructure": False,
                "year_approx": None
            }
        },
        {
            "name": "Advanced Persistent Threat",
            "category": "cybersecurity",
            "description": "Long-term targeted attack where an intruder gains and maintains unauthorized network access",
            "facts": {
                "is_a_concept": True, "is_physical": False, "is_a_person": False,
                "involves_computers": True, "is_malicious": True, "is_defensive": False,
                "requires_internet": True, "involves_human_error": True, "is_automated": False,
                "predates_2000": False, "is_illegal": True, "is_widely_known": False,
                "is_a_protocol": False, "is_a_tool": False, "involves_deception": True,
                "targets_individuals": False, "targets_organizations": True, "is_an_attack": True,
                "is_network_based": True, "is_state_sponsored": True, "targets_infrastructure": True,
                "year_approx": None
            }
        },
        {
            "name": "MITRE ATT&CK Framework",
            "category": "cybersecurity",
            "description": "A knowledge base of adversary tactics and techniques used by cybersecurity teams worldwide",
            "facts": {
                "is_a_concept": False, "is_physical": False, "is_a_person": False,
                "involves_computers": True, "is_malicious": False, "is_defensive": True,
                "requires_internet": False, "involves_human_error": False, "is_automated": False,
                "predates_2000": False, "is_illegal": False, "is_widely_known": False,
                "is_a_protocol": False, "is_a_tool": True, "involves_deception": False,
                "targets_individuals": False, "targets_organizations": False, "is_an_attack": False,
                "is_network_based": False, "is_state_sponsored": False, "targets_infrastructure": False,
                "year_approx": 2013
            }
        },
        {
            "name": "WannaCry",
            "category": "historical_cyber_event",
            "description": "2017 worldwide ransomware cryptoworm attack exploiting EternalBlue, affecting 200,000+ computers",
            "facts": {
                "is_a_concept": False, "is_physical": False, "is_a_person": False,
                "involves_computers": True, "is_malicious": True, "is_defensive": False,
                "requires_internet": True, "involves_human_error": False, "is_automated": True,
                "predates_2000": False, "is_illegal": True, "is_widely_known": True,
                "is_a_protocol": False, "is_a_tool": True, "involves_deception": False,
                "targets_individuals": True, "targets_organizations": True, "is_an_attack": True,
                "is_network_based": True, "is_state_sponsored": True, "targets_infrastructure": True,
                "year_approx": 2017
            }
        }
    ],
    "expert": [
        {
            "name": "Adversarial Machine Learning",
            "category": "ai_concept",
            "description": "Techniques that fool ML models by crafting inputs designed to cause misclassification",
            "facts": {
                "is_a_concept": True, "is_physical": False, "is_a_person": False,
                "involves_computers": True, "is_malicious": True, "is_defensive": False,
                "requires_internet": False, "involves_human_error": False, "is_automated": True,
                "predates_2000": False, "is_illegal": False, "is_widely_known": False,
                "is_a_protocol": False, "is_a_tool": False, "involves_deception": True,
                "targets_individuals": False, "targets_organizations": True, "is_an_attack": True,
                "is_network_based": False, "involves_ai": True, "involves_ml": True,
                "is_research_topic": True
            }
        },
        {
            "name": "Homomorphic Encryption",
            "category": "cybersecurity",
            "description": "Encryption allowing computation on ciphertexts without decrypting them first",
            "facts": {
                "is_a_concept": True, "is_physical": False, "is_a_person": False,
                "involves_computers": True, "is_malicious": False, "is_defensive": True,
                "requires_internet": False, "involves_human_error": False, "is_automated": True,
                "predates_2000": False, "is_illegal": False, "is_widely_known": False,
                "is_a_protocol": False, "is_a_tool": False, "involves_deception": False,
                "targets_individuals": False, "targets_organizations": False, "is_an_attack": False,
                "is_network_based": False, "involves_ai": False, "involves_ml": False,
                "is_research_topic": True
            }
        },
        {
            "name": "Prompt Injection",
            "category": "ai_concept",
            "description": "An attack that manipulates AI language models by embedding malicious instructions in inputs",
            "facts": {
                "is_a_concept": True, "is_physical": False, "is_a_person": False,
                "involves_computers": True, "is_malicious": True, "is_defensive": False,
                "requires_internet": True, "involves_human_error": False, "is_automated": False,
                "predates_2000": False, "is_illegal": False, "is_widely_known": False,
                "is_a_protocol": False, "is_a_tool": False, "involves_deception": True,
                "targets_individuals": False, "targets_organizations": True, "is_an_attack": True,
                "is_network_based": True, "involves_ai": True, "involves_ml": True,
                "is_research_topic": True
            }
        },
        {
            "name": "Quantum Key Distribution",
            "category": "cybersecurity",
            "description": "Secure communication using quantum mechanics to detect eavesdropping on cryptographic keys",
            "facts": {
                "is_a_concept": True, "is_physical": False, "is_a_person": False,
                "involves_computers": True, "is_malicious": False, "is_defensive": True,
                "requires_internet": False, "involves_human_error": False, "is_automated": True,
                "predates_2000": False, "is_illegal": False, "is_widely_known": False,
                "is_a_protocol": True, "is_a_tool": False, "involves_deception": False,
                "targets_individuals": False, "targets_organizations": False, "is_an_attack": False,
                "is_network_based": False, "involves_ai": False, "involves_ml": False,
                "is_research_topic": True
            }
        },
        {
            "name": "Supply Chain Attack",
            "category": "cybersecurity",
            "description": "Compromising software/hardware through trusted vendors before delivery (e.g. SolarWinds 2020)",
            "facts": {
                "is_a_concept": True, "is_physical": False, "is_a_person": False,
                "involves_computers": True, "is_malicious": True, "is_defensive": False,
                "requires_internet": True, "involves_human_error": True, "is_automated": False,
                "predates_2000": False, "is_illegal": True, "is_widely_known": False,
                "is_a_protocol": False, "is_a_tool": False, "involves_deception": True,
                "targets_individuals": False, "targets_organizations": True, "is_an_attack": True,
                "is_network_based": True, "involves_ai": False, "involves_ml": False,
                "is_research_topic": False
            }
        },
        {
            "name": "Federated Learning",
            "category": "ai_concept",
            "description": "ML technique training models across decentralized devices without sharing raw data",
            "facts": {
                "is_a_concept": True, "is_physical": False, "is_a_person": False,
                "involves_computers": True, "is_malicious": False, "is_defensive": True,
                "requires_internet": True, "involves_human_error": False, "is_automated": True,
                "predates_2000": False, "is_illegal": False, "is_widely_known": False,
                "is_a_protocol": False, "is_a_tool": False, "involves_deception": False,
                "targets_individuals": False, "targets_organizations": False, "is_an_attack": False,
                "is_network_based": True, "involves_ai": True, "involves_ml": True,
                "is_research_topic": True
            }
        }
    ]
}

# Leaderboard (starts empty - populated by real players)
LEADERBOARD = []

# Track recently used concepts per session to avoid repetition
recent_concepts = {}

# Question hint mapping
QUESTION_HINTS = {
    "is_a_concept": "Is it an abstract concept/idea (not a physical object or specific event)?",
    "is_physical": "Does it have a physical form (hardware, device)?",
    "is_a_person": "Is it a person?",
    "involves_computers": "Does it directly involve computers or digital systems?",
    "is_malicious": "Is it harmful or malicious in nature?",
    "is_defensive": "Is it used for defense or protection?",
    "requires_internet": "Does it require an internet connection to function?",
    "involves_human_error": "Does it often exploit human error or psychology?",
    "is_automated": "Is it typically automated or self-executing?",
    "predates_2000": "Did it exist before the year 2000?",
    "is_illegal": "Is it typically illegal?",
    "is_widely_known": "Is it commonly known to the general public?",
    "is_a_protocol": "Is it a protocol or standard?",
    "is_a_tool": "Is it a specific tool, software, or framework?",
    "involves_deception": "Does it involve deception or impersonation?",
    "targets_individuals": "Does it primarily target individuals?",
    "targets_organizations": "Does it primarily target organizations or enterprises?",
    "is_an_attack": "Is it classified as a cyberattack or attack technique?",
    "is_network_based": "Does it operate over a network?",
    "involves_email": "Does it involve email as a primary vector?",
    "is_state_sponsored": "Is it known to be state-sponsored?",
    "targets_infrastructure": "Does it target critical infrastructure?",
    "involves_ai": "Does it involve Artificial Intelligence?",
    "involves_ml": "Does it involve Machine Learning?",
    "is_research_topic": "Is it primarily an active research topic?",
    "year_approx": "Was it created/discovered after 2015?"
}

# Active game sessions
sessions = {}

def get_session_id(request):
    ip = request.remote_addr or "127.0.0.1"
    ua = request.headers.get('User-Agent', '')
    return hashlib.md5(f"{ip}{ua}".encode()).hexdigest()[:16]

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/start', methods=['POST'])
def start_game():
    """
    Start a new game, avoiding recently used concepts for variety.
    """
    data = request.json
    difficulty = data.get('difficulty', 'hard')
    sid = get_session_id(request)
    
    # Get available items for this difficulty
    items = ITEMS.get(difficulty, ITEMS['hard'])
    
    # Get recently used concepts for this session (last 5 games)
    if sid not in recent_concepts:
        recent_concepts[sid] = []
    
    recent = recent_concepts[sid]
    
    # Try to find a concept that hasn't been used recently
    available_items = [item for item in items if item['name'] not in recent]
    
    # If all concepts have been used recently, reset and use all
    if not available_items:
        recent_concepts[sid] = []
        available_items = items
        print(f"Session {sid}: All concepts used, resetting recent list")
    
    # Select a random concept from available ones
    item = random.choice(available_items)
    
    # Track this concept as recently used (keep last 5)
    recent_concepts[sid].append(item['name'])
    if len(recent_concepts[sid]) > 5:
        recent_concepts[sid].pop(0)
    
    print(f"Session {sid}: Selected '{item['name']}', Recent: {recent_concepts[sid]}")
    
    sessions[sid] = {
        "item": item,
        "difficulty": difficulty,
        "questions_asked": 0,
        "questions_log": [],
        "hints_used": 0,
        "hearts": 3,
        "game_over": False,
        "won": False,
        "started_at": time.time(),
        "wrong_guesses": 0
    }
    
    return jsonify({
        "status": "ok",
        "session_id": sid,
        "difficulty": difficulty,
        "category_hint": item["category"].replace("_", " ").title(),
        "questions_remaining": 20
    })

@app.route('/api/question', methods=['POST'])
def ask_question():
    """
    Handle user-submitted questions using AI evaluation.
    Uses Gemini 2.5 Flash to intelligently answer questions.
    """
    data = request.json
    sid = get_session_id(request)
    session = sessions.get(sid)
    
    if not session:
        return jsonify({"error": "No active game. Start a new game first."}), 400
    
    if session['game_over']:
        return jsonify({"error": "Game over."}), 400
    
    if session['questions_asked'] >= 20:
        return jsonify({"error": "No questions remaining."}), 400
    
    # Get user's question text
    question_text = data.get('question_text', '').strip()
    
    if not question_text:
        return jsonify({"error": "Question cannot be empty."}), 400
    
    if len(question_text) < 5:
        return jsonify({"error": "Question must be at least 5 characters."}), 400
    
    # Check if question was already asked (case-insensitive)
    question_lower = question_text.lower()
    asked_questions = [q['question'].lower() for q in session['questions_log']]
    if question_lower in asked_questions:
        return jsonify({"error": "You already asked this question."}), 400
    
    # Use AI to evaluate the question
    item = session['item']
    answer = evaluate_question_with_ai(question_text, item)
    
    session['questions_asked'] += 1
    session['questions_log'].append({
        "question": question_text,
        "answer": answer
    })
    
    return jsonify({
        "answer": answer,
        "questions_asked": session['questions_asked'],
        "questions_remaining": 20 - session['questions_asked'],
        "log": session['questions_log']
    })

def evaluate_question_with_ai(question: str, item: dict) -> str:
    """
    Use Gemini 2.5 Flash to evaluate a user's question with common sense.
    
    Args:
        question: The user's natural language question
        item: The concept dictionary with name, description, and facts
        
    Returns:
        "Yes", "No", or "Irrelevant"
    """
    # Format facts for the prompt
    facts_list = []
    for key, value in item['facts'].items():
        if value is True:
            facts_list.append(f"- {key.replace('_', ' ')}: Yes")
        elif value is False:
            facts_list.append(f"- {key.replace('_', ' ')}: No")
        elif value is not None:
            facts_list.append(f"- {key.replace('_', ' ')}: {value}")
    
    facts_text = "\n".join(facts_list) if facts_list else "No specific facts available"
    
    prompt = f"""You are a cybersecurity expert evaluating questions in a guessing game. Use COMMON SENSE and domain knowledge.

The SECRET CONCEPT is: {item['name']}
Category: {item['category']}
Description: {item['description']}

CONCEPT FACTS:
{facts_text}

PLAYER'S QUESTION: "{question}"

INSTRUCTIONS - USE COMMON SENSE:
1. Consider the REAL NATURE of the concept, not just binary facts
2. Use your cybersecurity knowledge to answer intelligently
3. Understand NUANCE - tools can be neutral, not purely attack or defense

EXAMPLES OF COMMON SENSE REASONING:
- "Is it an attack?" for "Phishing Attack" → YES (it's literally an attack)
- "Is it an attack?" for "DirBuster" → NO (it's a tool that CAN be used for attacks, but isn't an attack itself)
- "Is it defensive?" for "DirBuster" → NO (it's an enumeration tool, not defensive)
- "Is it a tool?" for "DirBuster" → YES (it's clearly a tool)
- "Is it malicious?" for "Firewall" → NO (firewalls are protective)
- "Is it malicious?" for "Ransomware" → YES (ransomware is inherently malicious)

KEY PRINCIPLES:
- ATTACKS are malicious actions (Phishing, DDoS, SQL Injection)
- TOOLS are software/utilities that can be used for various purposes (Nmap, DirBuster, Metasploit)
- DEFENSES are protective measures (Firewall, Antivirus, IDS)
- Some tools are NEUTRAL - they enumerate, scan, or analyze but aren't attacks themselves
- Consider the PRIMARY PURPOSE and nature of the concept

ANSWER GUIDELINES:
- "Yes" - The statement is TRUE about this concept
- "No" - The statement is FALSE about this concept  
- "Irrelevant" - The question doesn't make sense or can't be answered yes/no

Think like a cybersecurity professional. Return ONLY ONE WORD: "Yes", "No", or "Irrelevant"

Answer:"""

    try:
        response = gemini_model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.2,
                "max_output_tokens": 10,
            }
        )
        
        print(f"[AI DEBUG] Question: {question}")
        print(f"[AI DEBUG] Raw response: {response}")
        
        if response and hasattr(response, 'text') and response.text:
            answer = response.text.strip().strip('"').strip("'")
            print(f"[AI DEBUG] Parsed answer: {answer}")
            answer_lower = answer.lower()
            
            if "yes" in answer_lower:
                return "Yes"
            elif "no" in answer_lower:
                return "No"
            else:
                return "Irrelevant"
        else:
            print(f"[AI DEBUG] No text in response or response is None")
            # Check if response was blocked
            if response and hasattr(response, 'prompt_feedback'):
                print(f"[AI DEBUG] Prompt feedback: {response.prompt_feedback}")
            return "Irrelevant"
            
    except Exception as e:
        print(f"[AI ERROR] Exception: {str(e)}")
        print(f"[AI ERROR] Exception type: {type(e)}")
        import traceback
        traceback.print_exc()
        return "Irrelevant"

@app.route('/api/guess', methods=['POST'])
def make_guess():
    """
    Validate player's guess using AI instead of fuzzy matching.
    """
    data = request.json
    sid = get_session_id(request)
    session = sessions.get(sid)
    
    if not session:
        return jsonify({"error": "No active game."}), 400
    
    if session['game_over']:
        return jsonify({"error": "Game over."}), 400
    
    guess = data.get('guess', '').strip()
    
    if not guess or len(guess) < 3:
        return jsonify({"error": "Guess must be at least 3 characters."}), 400
    
    # Use AI to validate the guess
    item = session['item']
    is_correct = validate_guess_with_ai(guess, item)
    
    if is_correct:
        hints_used = session['hints_used']
        xp = 100 if hints_used == 0 else (70 if hints_used == 1 else 40)
        session['won'] = True
        session['game_over'] = True
        
        # Update leaderboard
        player_name = data.get('player_name', 'Anonymous')
        LEADERBOARD.append({
            "name": player_name,
            "score": xp + (session['questions_asked'] * -2) + (session['hearts'] * 10),
            "games": 1,
            "rank": 0
        })
        LEADERBOARD.sort(key=lambda x: x['score'], reverse=True)
        for i, entry in enumerate(LEADERBOARD[:10]):
            entry['rank'] = i + 1
        
        return jsonify({
            "correct": True,
            "xp_earned": xp,
            "item": session['item'],
            "questions_used": session['questions_asked'],
            "hearts_remaining": session['hearts']
        })
    else:
        session['hearts'] -= 1
        session['wrong_guesses'] += 1
        
        if session['hearts'] <= 0:
            session['game_over'] = True
            return jsonify({
                "correct": False,
                "game_over": True,
                "hearts_remaining": 0,
                "item": session['item'],
                "message": "Game Over! You've lost all your lives."
            })
        
        return jsonify({
            "correct": False,
            "game_over": False,
            "hearts_remaining": session['hearts'],
            "message": f"Wrong guess! {session['hearts']} {'heart' if session['hearts'] == 1 else 'hearts'} remaining."
        })

def validate_guess_with_ai(guess: str, item: dict) -> bool:
    """
    Use Gemini 2.5 Flash to validate if a guess matches the concept.
    
    Args:
        guess: The player's guess
        item: The concept dictionary with name, description, and category
        
    Returns:
        True if correct, False otherwise
    """
    prompt = f"""You are validating a player's guess in a cybersecurity guessing game.

The CORRECT ANSWER is: {item['name']}
Category: {item['category']}
Description: {item['description']}

The PLAYER'S GUESS is: "{guess}"

Determine if the player's guess is correct. Consider:
- Exact matches (case-insensitive)
- Common abbreviations (e.g., "DDoS" for "Distributed Denial of Service")
- Synonyms and alternative names (e.g., "Firewall" vs "Network Firewall")
- Minor spelling variations
- Partial matches that clearly refer to the same concept

IMPORTANT: Be reasonably strict. The guess should clearly refer to the same specific concept.
Do NOT accept vague or generic terms that could apply to many concepts.

Respond with ONLY one word:
- "CORRECT" if the guess matches the concept
- "INCORRECT" if the guess does not match

Answer:"""

    try:
        response = gemini_model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.1,
                "max_output_tokens": 10,
            }
        )
        
        if response and response.text:
            result = response.text.strip().upper()
            return "CORRECT" in result
        else:
            # Fallback to exact match
            return guess.lower() == item['name'].lower()
            
    except Exception as e:
        print(f"Error validating guess with AI: {str(e)}")
        # Fallback to exact match
        return guess.lower() == item['name'].lower()

@app.route('/api/hint', methods=['POST'])
def get_hint():
    sid = get_session_id(request)
    session = sessions.get(sid)
    
    if not session:
        return jsonify({"error": "No active game."}), 400
    
    item = session['item']
    hints = [
        f"Category: {item['category'].replace('_', ' ').title()}",
        f"The answer contains {len(item['name'])} characters.",
        f"First letter: '{item['name'][0]}'"
    ]
    
    hint_idx = min(session['hints_used'], len(hints) - 1)
    hint = hints[hint_idx]
    session['hints_used'] += 1
    
    return jsonify({
        "hint": hint,
        "hints_used": session['hints_used']
    })

@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    return jsonify({"leaderboard": LEADERBOARD[:10]})

@app.route('/api/session', methods=['GET'])
def get_session():
    sid = get_session_id(request)
    session = sessions.get(sid)
    if not session:
        return jsonify({"active": False})
    return jsonify({
        "active": not session['game_over'],
        "questions_asked": session['questions_asked'],
        "hearts": session['hearts'],
        "difficulty": session['difficulty'],
        "log": session['questions_log']
    })


HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CIPHER — Advanced 20 Questions</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Rajdhani:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;600&display=swap');

:root {
  --bg-deep: #020b18;
  --bg-dark: #041224;
  --bg-card: #061a2e;
  --bg-card2: #082040;
  --blue-900: #0a1628;
  --blue-800: #0d2040;
  --blue-700: #0f3460;
  --blue-600: #155fa0;
  --blue-500: #1e7fcb;
  --blue-400: #38a3e8;
  --blue-300: #6ec0f5;
  --blue-200: #a8d8fa;
  --green-900: #011a0d;
  --green-700: #065e2e;
  --green-500: #0d9f53;
  --green-400: #17c96a;
  --green-300: #4de890;
  --green-200: #8fffc0;
  --cyan: #00e5ff;
  --teal: #00bcd4;
  --accent: #00ff88;
  --warning: #ff9f1c;
  --danger: #ff3a5c;
  --text-primary: #e8f4ff;
  --text-secondary: #7ab5d8;
  --text-muted: #3d6e8a;
  --border: #0d3a5c;
  --glow-blue: 0 0 20px rgba(30,127,203,0.4);
  --glow-green: 0 0 20px rgba(13,159,83,0.4);
  --glow-cyan: 0 0 30px rgba(0,229,255,0.3);
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: 'Rajdhani', sans-serif;
  background: var(--bg-deep);
  color: var(--text-primary);
  min-height: 100vh;
  overflow-x: hidden;
  position: relative;
}

/* Animated background grid */
body::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image: 
    linear-gradient(rgba(30,127,203,0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(30,127,203,0.05) 1px, transparent 1px);
  background-size: 40px 40px;
  animation: gridPulse 8s ease-in-out infinite;
  pointer-events: none;
  z-index: 0;
}

body::after {
  content: '';
  position: fixed;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(ellipse at 30% 20%, rgba(0,229,255,0.04) 0%, transparent 50%),
              radial-gradient(ellipse at 70% 80%, rgba(13,159,83,0.05) 0%, transparent 50%);
  animation: ambientShift 15s ease-in-out infinite alternate;
  pointer-events: none;
  z-index: 0;
}

@keyframes gridPulse {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}

@keyframes ambientShift {
  0% { transform: translate(0, 0); }
  100% { transform: translate(30px, 20px); }
}

.app {
  position: relative;
  z-index: 1;
  max-width: 1100px;
  margin: 0 auto;
  padding: 20px 16px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* HEADER */
.header {
  text-align: center;
  padding: 24px 0 32px;
}

.logo {
  font-family: 'Orbitron', monospace;
  font-size: clamp(2rem, 6vw, 3.8rem);
  font-weight: 900;
  letter-spacing: 0.25em;
  background: linear-gradient(135deg, var(--cyan), var(--blue-400), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: none;
  filter: drop-shadow(0 0 24px rgba(0,229,255,0.5));
  animation: logoPulse 4s ease-in-out infinite;
}

@keyframes logoPulse {
  0%, 100% { filter: drop-shadow(0 0 20px rgba(0,229,255,0.4)); }
  50% { filter: drop-shadow(0 0 35px rgba(0,229,255,0.7)); }
}

.tagline {
  font-family: 'JetBrains Mono', monospace;
  font-size: clamp(0.65rem, 2vw, 0.85rem);
  color: var(--text-muted);
  letter-spacing: 0.3em;
  margin-top: 8px;
  text-transform: uppercase;
}

/* NAV TABS */
.nav-tabs {
  display: flex;
  gap: 4px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 6px;
  margin-bottom: 24px;
  width: fit-content;
  margin-left: auto;
  margin-right: auto;
}

.nav-tab {
  font-family: 'Orbitron', monospace;
  font-size: 0.65rem;
  letter-spacing: 0.1em;
  padding: 8px 18px;
  border: none;
  background: transparent;
  color: var(--text-muted);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.25s;
  text-transform: uppercase;
}

.nav-tab.active {
  background: linear-gradient(135deg, var(--blue-700), var(--blue-600));
  color: var(--cyan);
  box-shadow: var(--glow-blue);
}

.nav-tab:hover:not(.active) {
  color: var(--blue-300);
  background: var(--bg-card2);
}

/* VIEWS */
.view { display: none; animation: fadeIn 0.4s ease; }
.view.active { display: block; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* CARDS */
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 24px;
  position: relative;
  overflow: hidden;
}

.card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--blue-500), var(--cyan), var(--blue-500), transparent);
  animation: scanline 3s linear infinite;
}

@keyframes scanline {
  0% { opacity: 0; }
  50% { opacity: 1; }
  100% { opacity: 0; }
}

/* START SCREEN */
.difficulty-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  margin: 28px 0;
}

@media (max-width: 600px) {
  .difficulty-grid { grid-template-columns: 1fr; }
}

.diff-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 20px 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.diff-card::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at center, rgba(30,127,203,0.1), transparent 70%);
  opacity: 0;
  transition: opacity 0.3s;
}

.diff-card:hover::after, .diff-card.selected::after { opacity: 1; }

.diff-card.selected {
  border-color: var(--cyan);
  box-shadow: var(--glow-cyan), inset 0 0 20px rgba(0,229,255,0.05);
}

.diff-card:hover:not(.selected) {
  border-color: var(--blue-500);
  transform: translateY(-3px);
}

.diff-icon { font-size: 2rem; margin-bottom: 8px; }
.diff-name {
  font-family: 'Orbitron', monospace;
  font-size: 0.75rem;
  letter-spacing: 0.15em;
  color: var(--cyan);
  margin-bottom: 6px;
  text-transform: uppercase;
}

.diff-desc {
  font-size: 0.78rem;
  color: var(--text-muted);
  line-height: 1.4;
}

.diff-xp {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: var(--accent);
  margin-top: 8px;
}

/* RULES BOX */
.rules-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin: 20px 0;
}

@media (max-width: 500px) {
  .rules-grid { grid-template-columns: 1fr; }
}

.rule-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px;
  background: var(--bg-card2);
  border-radius: 10px;
  border: 1px solid rgba(13,58,92,0.5);
}

.rule-icon { font-size: 1.2rem; flex-shrink: 0; }
.rule-text { font-size: 0.82rem; color: var(--text-secondary); line-height: 1.4; }
.rule-text strong { color: var(--text-primary); }

/* BUTTONS */
.btn {
  font-family: 'Orbitron', monospace;
  font-size: 0.75rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 12px 28px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.25s ease;
  position: relative;
  overflow: hidden;
}

.btn::before {
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 100%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.07), transparent);
  transition: left 0.4s;
}

.btn:hover::before { left: 100%; }

.btn-primary {
  background: linear-gradient(135deg, var(--blue-600), var(--blue-500));
  color: var(--text-primary);
  box-shadow: var(--glow-blue);
}

.btn-primary:hover {
  background: linear-gradient(135deg, var(--blue-500), var(--blue-400));
  transform: translateY(-2px);
  box-shadow: 0 0 30px rgba(30,127,203,0.6);
}

.btn-success {
  background: linear-gradient(135deg, var(--green-700), var(--green-500));
  color: var(--text-primary);
  box-shadow: var(--glow-green);
}

.btn-success:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 30px rgba(13,159,83,0.6);
}

.btn-danger {
  background: linear-gradient(135deg, #7a1a28, #c0253d);
  color: var(--text-primary);
}

.btn-outline {
  background: transparent;
  border: 1px solid var(--blue-600);
  color: var(--blue-300);
}

.btn-outline:hover {
  background: var(--blue-700);
  color: var(--cyan);
}

.btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  transform: none !important;
}

.btn-lg { padding: 16px 40px; font-size: 0.85rem; }
.btn-sm { padding: 8px 16px; font-size: 0.65rem; }

/* GAME SCREEN */
.game-hud {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 12px;
  margin-bottom: 20px;
}

@media (max-width: 500px) {
  .game-hud { grid-template-columns: 1fr 1fr; }
}

.hud-item {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 14px 12px;
  text-align: center;
}

.hud-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.6rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.15em;
  margin-bottom: 6px;
}

.hud-value {
  font-family: 'Orbitron', monospace;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--cyan);
}

.hearts { font-size: 1.2rem; letter-spacing: 2px; }

.category-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(0,229,255,0.07);
  border: 1px solid rgba(0,229,255,0.2);
  border-radius: 8px;
  padding: 8px 16px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  color: var(--cyan);
  margin-bottom: 20px;
  letter-spacing: 0.1em;
}

/* QUESTION GRID */
.questions-section { margin-bottom: 20px; }

.section-title {
  font-family: 'Orbitron', monospace;
  font-size: 0.65rem;
  letter-spacing: 0.2em;
  color: var(--text-muted);
  text-transform: uppercase;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-title::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border);
}

.question-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

@media (min-width: 700px) {
  .question-grid { grid-template-columns: repeat(3, 1fr); }
}

@media (max-width: 400px) {
  .question-grid { grid-template-columns: 1fr; }
}

.q-btn {
  background: var(--bg-card2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 10px 12px;
  color: var(--text-secondary);
  font-family: 'Rajdhani', sans-serif;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
  line-height: 1.3;
}

.q-btn:hover:not(:disabled) {
  border-color: var(--blue-500);
  color: var(--text-primary);
  background: rgba(30,127,203,0.1);
  transform: translateY(-1px);
}

.q-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.q-btn.asked-yes {
  border-color: var(--green-400);
  background: rgba(13,159,83,0.1);
  color: var(--green-300);
}

.q-btn.asked-no {
  border-color: var(--danger);
  background: rgba(255,58,92,0.08);
  color: #ff7a92;
}

.q-btn.asked-irr {
  border-color: var(--warning);
  background: rgba(255,159,28,0.08);
  color: #ffcc7a;
}

/* ANSWER LOG */
.answer-log {
  max-height: 200px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding-right: 4px;
}

.answer-log::-webkit-scrollbar { width: 4px; }
.answer-log::-webkit-scrollbar-track { background: var(--bg-dark); }
.answer-log::-webkit-scrollbar-thumb { background: var(--blue-700); border-radius: 2px; }

.log-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 8px 12px;
  background: var(--bg-card2);
  border-radius: 8px;
  border-left: 3px solid transparent;
  animation: slideIn 0.3s ease;
  font-size: 0.82rem;
}

@keyframes slideIn {
  from { opacity: 0; transform: translateX(-10px); }
  to { opacity: 1; transform: translateX(0); }
}

.log-item.yes { border-left-color: var(--green-400); }
.log-item.no { border-left-color: var(--danger); }
.log-item.irr { border-left-color: var(--warning); }

.log-q { color: var(--text-secondary); flex: 1; }
.log-a { font-family: 'Orbitron', monospace; font-size: 0.65rem; font-weight: 700; white-space: nowrap; }
.log-a.yes { color: var(--green-300); }
.log-a.no { color: #ff7a92; }
.log-a.irr { color: #ffcc7a; }

/* GUESS SECTION */
.guess-section {
  margin-top: 20px;
}

.guess-row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.guess-input {
  flex: 1;
  min-width: 200px;
  background: var(--bg-card2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 12px 16px;
  color: var(--text-primary);
  font-family: 'Rajdhani', sans-serif;
  font-size: 1rem;
  font-weight: 500;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.guess-input:focus {
  border-color: var(--blue-500);
  box-shadow: var(--glow-blue);
}

.guess-input::placeholder { color: var(--text-muted); }

/* ANSWER FEEDBACK */
.feedback {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 14px 28px;
  border-radius: 12px;
  font-family: 'Orbitron', monospace;
  font-size: 0.8rem;
  letter-spacing: 0.1em;
  z-index: 1000;
  animation: feedbackAnim 0.4s ease;
  white-space: nowrap;
  max-width: 90vw;
  text-align: center;
}

@keyframes feedbackAnim {
  from { opacity: 0; transform: translateX(-50%) translateY(-20px); }
  to { opacity: 1; transform: translateX(-50%) translateY(0); }
}

.feedback.yes {
  background: linear-gradient(135deg, #062a18, #0d4a26);
  border: 1px solid var(--green-400);
  color: var(--green-200);
  box-shadow: var(--glow-green);
}

.feedback.no {
  background: linear-gradient(135deg, #2a0610, #4a0d1e);
  border: 1px solid var(--danger);
  color: #ffc0cc;
}

.feedback.irr {
  background: linear-gradient(135deg, #2a1a06, #4a2d0d);
  border: 1px solid var(--warning);
  color: #ffe0a0;
}

/* RESULT SCREEN */
.result-hero {
  text-align: center;
  padding: 32px 0;
}

.result-emoji { font-size: 4rem; margin-bottom: 16px; animation: bounce 0.8s ease; }

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  40% { transform: translateY(-20px); }
  60% { transform: translateY(-10px); }
}

.result-title {
  font-family: 'Orbitron', monospace;
  font-size: clamp(1.2rem, 4vw, 2rem);
  font-weight: 900;
  margin-bottom: 8px;
}

.result-title.win { color: var(--accent); text-shadow: 0 0 30px rgba(0,255,136,0.5); }
.result-title.lose { color: var(--danger); text-shadow: 0 0 30px rgba(255,58,92,0.5); }

.result-answer {
  background: var(--bg-card2);
  border: 1px solid var(--cyan);
  border-radius: 14px;
  padding: 20px;
  margin: 20px 0;
  box-shadow: var(--glow-cyan);
}

.result-answer-name {
  font-family: 'Orbitron', monospace;
  font-size: clamp(1rem, 3vw, 1.5rem);
  color: var(--cyan);
  margin-bottom: 8px;
}

.result-answer-desc {
  color: var(--text-secondary);
  font-size: 0.88rem;
  line-height: 1.5;
}

.xp-badge {
  display: inline-block;
  background: linear-gradient(135deg, #1a3a20, #0d9f53);
  border: 1px solid var(--green-400);
  border-radius: 50px;
  padding: 10px 28px;
  font-family: 'Orbitron', monospace;
  font-size: 1rem;
  color: var(--accent);
  margin: 12px 0;
  box-shadow: var(--glow-green);
  animation: xpPop 0.6s 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

@keyframes xpPop {
  from { transform: scale(0); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

/* OPTIMAL PATH */
.optimal-path {
  background: var(--bg-card2);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  margin-top: 16px;
}

.path-title {
  font-family: 'Orbitron', monospace;
  font-size: 0.65rem;
  letter-spacing: 0.2em;
  color: var(--blue-300);
  text-transform: uppercase;
  margin-bottom: 14px;
}

.path-step {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 0;
  border-bottom: 1px solid rgba(13,58,92,0.4);
  font-size: 0.82rem;
}

.path-step:last-child { border-bottom: none; }

.step-num {
  font-family: 'Orbitron', monospace;
  font-size: 0.65rem;
  background: var(--blue-700);
  color: var(--cyan);
  width: 22px;
  height: 22px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-weight: 700;
}

.step-q { color: var(--text-secondary); flex: 1; }
.step-a { font-weight: 600; }
.step-a.yes { color: var(--green-300); }
.step-a.no { color: #ff7a92; }

/* LEADERBOARD */
.lb-row {
  display: grid;
  grid-template-columns: 40px 1fr auto auto;
  gap: 12px;
  align-items: center;
  padding: 12px 16px;
  background: var(--bg-card2);
  border-radius: 10px;
  border: 1px solid var(--border);
  margin-bottom: 8px;
  transition: all 0.2s;
}

.lb-row:hover { border-color: var(--blue-500); }

.lb-rank {
  font-family: 'Orbitron', monospace;
  font-size: 0.9rem;
  font-weight: 700;
  text-align: center;
}

.lb-rank.gold { color: #ffd700; }
.lb-rank.silver { color: #c0c0c0; }
.lb-rank.bronze { color: #cd7f32; }
.lb-rank.other { color: var(--text-muted); }

.lb-name {
  font-family: 'Rajdhani', sans-serif;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-primary);
}

.lb-score {
  font-family: 'Orbitron', monospace;
  font-size: 0.85rem;
  color: var(--accent);
  font-weight: 700;
}

.lb-games {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: var(--text-muted);
  text-align: right;
}

/* PROGRESS BAR */
.progress-bar-outer {
  background: var(--bg-card2);
  border-radius: 100px;
  height: 6px;
  overflow: hidden;
  margin-top: 6px;
}

.progress-bar-inner {
  height: 100%;
  border-radius: 100px;
  background: linear-gradient(90deg, var(--blue-500), var(--cyan));
  transition: width 0.5s ease;
}

/* MISC */
.text-center { text-align: center; }
.mt-4 { margin-top: 16px; }
.mt-8 { margin-top: 32px; }
.flex { display: flex; }
.gap-3 { gap: 12px; }
.justify-center { justify-content: center; }
.flex-wrap { flex-wrap: wrap; }

.scan-line {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 2px;
  background: linear-gradient(90deg, transparent, var(--cyan), transparent);
  animation: scan 6s linear infinite;
  opacity: 0.3;
  pointer-events: none;
  z-index: 999;
}

@keyframes scan {
  from { top: -2px; }
  to { top: 100vh; }
}

.pulse-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--accent);
  display: inline-block;
  animation: pulseDot 2s ease-in-out infinite;
}

@keyframes pulseDot {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.5); opacity: 0.6; }
}

.spinner {
  width: 20px; height: 20px;
  border: 2px solid rgba(30,127,203,0.2);
  border-top-color: var(--cyan);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  display: inline-block;
}

@keyframes spin { to { transform: rotate(360deg); } }

.terminal-text {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.78rem;
  color: var(--text-muted);
}

.input-field {
  background: var(--bg-card2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 10px 14px;
  color: var(--text-primary);
  font-family: 'Rajdhani', sans-serif;
  font-size: 0.9rem;
  outline: none;
  width: 100%;
  transition: border-color 0.2s;
}

.input-field:focus { border-color: var(--blue-400); }
.input-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.15em;
  margin-bottom: 6px;
  display: block;
}
</style>
</head>
<body>

<div class="scan-line"></div>

<div class="app">
  <div class="header">
    <div class="logo">CIPHER</div>
    <div class="tagline">⬡ Advanced 20 Questions · Cybersecurity Edition ⬡</div>
  </div>

  <div class="nav-tabs">
    <button class="nav-tab active" onclick="showView('game')">PLAY</button>
    <button class="nav-tab" onclick="showView('leaderboard')">LEADERBOARD</button>
    <button class="nav-tab" onclick="showView('howto')">HOW TO PLAY</button>
  </div>

  <!-- ═══ GAME VIEW ═══ -->
  <div id="view-game" class="view active">

    <!-- START SCREEN -->
    <div id="screen-start">
      <div class="card">
        <div class="section-title">SELECT DIFFICULTY</div>
        <div class="difficulty-grid">
          <div class="diff-card selected" id="diff-medium" onclick="selectDiff('medium')">
            <div class="diff-icon">🛡️</div>
            <div class="diff-name">Medium</div>
            <div class="diff-desc">Common attacks & security concepts</div>
            <div class="diff-xp">+70 XP avg</div>
          </div>
          <div class="diff-card" id="diff-hard" onclick="selectDiff('hard')">
            <div class="diff-icon">⚔️</div>
            <div class="diff-name">Hard</div>
            <div class="diff-desc">Enterprise threats & historic incidents</div>
            <div class="diff-xp">+85 XP avg</div>
          </div>
          <div class="diff-card" id="diff-expert" onclick="selectDiff('expert')">
            <div class="diff-icon">☠️</div>
            <div class="diff-name">Expert</div>
            <div class="diff-desc">AI/ML attacks, zero-days, obscure concepts</div>
            <div class="diff-xp">+100 XP avg</div>
          </div>
        </div>

        <div style="margin-bottom:16px">
          <label class="input-label">CODENAME (for leaderboard)</label>
          <input class="input-field" id="player-name" placeholder="Enter your alias..." maxlength="20" value="Agent_X" />
        </div>

        <div class="rules-grid">
          <div class="rule-item">
            <span class="rule-icon">❓</span>
            <div class="rule-text"><strong>20 Questions</strong> — Ask yes/no questions about the hidden concept</div>
          </div>
          <div class="rule-item">
            <span class="rule-icon">❤️</span>
            <div class="rule-text"><strong>3 Lives</strong> — Each wrong final guess costs 1 heart</div>
          </div>
          <div class="rule-item">
            <span class="rule-icon">🏆</span>
            <div class="rule-text"><strong>XP Scoring</strong> — 100 XP no hints · 70 after 1 · 40 after 2</div>
          </div>
          <div class="rule-item">
            <span class="rule-icon">💡</span>
            <div class="rule-text"><strong>Hints</strong> — Use up to 3 hints but each reduces your score</div>
          </div>
        </div>

        <div class="text-center mt-4">
          <button class="btn btn-primary btn-lg" onclick="startGame()">
            INITIALIZE GAME
          </button>
        </div>
      </div>
    </div>

    <!-- GAME SCREEN -->
    <div id="screen-game" style="display:none">

      <!-- HUD -->
      <div class="game-hud">
        <div class="hud-item">
          <div class="hud-label">Questions Left</div>
          <div class="hud-value" id="hud-questions">20</div>
          <div class="progress-bar-outer">
            <div class="progress-bar-inner" id="q-progress" style="width:100%"></div>
          </div>
        </div>
        <div class="hud-item">
          <div class="hud-label">Lives</div>
          <div class="hearts" id="hud-hearts">❤️❤️❤️</div>
        </div>
        <div class="hud-item">
          <div class="hud-label">Difficulty</div>
          <div class="hud-value" id="hud-diff" style="font-size:0.75rem;letter-spacing:0.1em">—</div>
        </div>
      </div>

      <div id="category-badge" class="category-badge">
        <span class="pulse-dot"></span>
        <span id="badge-text">Loading category...</span>
      </div>

      <!-- QUESTION INPUT -->
      <div class="questions-section card" style="margin-bottom:16px">
        <div class="section-title">ASK A QUESTION</div>
        <div style="padding: 12px;">
          <p style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 12px;">
            Type your own yes/no question to learn about the concept:
          </p>
          <div class="guess-row">
            <input 
              class="guess-input" 
              id="question-input" 
              placeholder="e.g., Is it used for defense? Does it involve encryption?" 
              maxlength="200"
            />
            <button class="btn btn-primary" onclick="submitQuestion()">ASK</button>
          </div>
          <p style="color: var(--text-muted); font-size: 0.75rem; margin-top: 8px;">
            Questions remaining: <span id="questions-remaining">20</span>/20
          </p>
        </div>
      </div>

      <!-- Q&A LOG -->
      <div class="card" style="margin-bottom:16px" id="log-section" style="display:none">
        <div class="section-title">INTERROGATION LOG</div>
        <div class="answer-log" id="answer-log">
          <div class="terminal-text" style="padding:8px">// No questions asked yet — start your investigation</div>
        </div>
      </div>

      <!-- GUESS SECTION -->
      <div class="card guess-section">
        <div class="section-title">FINAL ANSWER</div>
        <div class="guess-row">
          <input class="guess-input" id="guess-input" placeholder="Type your answer..." />
          <button class="btn btn-success" onclick="submitGuess()">SUBMIT</button>
          <button class="btn btn-outline btn-sm" onclick="getHint()">💡 HINT</button>
        </div>
        <div id="hint-display" style="margin-top:10px;display:none" class="terminal-text"></div>
      </div>

      <div class="text-center mt-4">
        <button class="btn btn-outline btn-sm" onclick="startNew()">↺ New Game</button>
      </div>
    </div>

    <!-- RESULT SCREEN -->
    <div id="screen-result" style="display:none">
      <div class="card">
        <div class="result-hero">
          <div class="result-emoji" id="result-emoji">🎯</div>
          <div class="result-title" id="result-title">IDENTIFIED</div>
          <div class="xp-badge" id="xp-badge" style="display:none"></div>
        </div>

        <div class="result-answer">
          <div class="result-answer-name" id="result-name"></div>
          <div class="result-answer-desc" id="result-desc"></div>
        </div>

        <div class="optimal-path" id="optimal-path">
          <div class="path-title">⚡ OPTIMAL QUESTION PATH</div>
          <div id="path-steps"></div>
        </div>

        <div class="flex gap-3 justify-center flex-wrap mt-4">
          <button class="btn btn-primary" onclick="startNew()">PLAY AGAIN</button>
          <button class="btn btn-outline" onclick="showView('leaderboard')">LEADERBOARD</button>
        </div>
      </div>
    </div>
  </div>

  <!-- ═══ LEADERBOARD VIEW ═══ -->
  <div id="view-leaderboard" class="view">
    <div class="card">
      <div class="section-title">GLOBAL LEADERBOARD</div>
      <div id="lb-container">
        <div class="spinner" style="margin:20px auto;display:block;width:32px;height:32px;border-width:3px"></div>
      </div>
    </div>
  </div>

  <!-- ═══ HOW TO PLAY VIEW ═══ -->
  <div id="view-howto" class="view">
    <div class="card">
      <div class="section-title">GAME MANUAL</div>
      <div style="display:grid;gap:16px">
        <div class="rule-item">
          <span class="rule-icon">🎯</span>
          <div class="rule-text">
            <strong>Objective:</strong> The AI secretly selects a cybersecurity concept, AI technique, historical cyber event, or rare tech object. You must identify it using up to 20 yes/no questions and up to 3 final guesses.
          </div>
        </div>
        <div class="rule-item">
          <span class="rule-icon">❓</span>
          <div class="rule-text">
            <strong>Questions:</strong> Click question buttons to ask. Answers are strictly <span style="color:var(--green-300)">Yes</span>, <span style="color:#ff7a92">No</span>, or <span style="color:#ffcc7a">Irrelevant</span>. Use the color-coded log to track responses.
          </div>
        </div>
        <div class="rule-item">
          <span class="rule-icon">❤️</span>
          <div class="rule-text">
            <strong>Lives:</strong> You start with 3 hearts. Each wrong final answer costs 1 heart. Lose all 3 → Game Over. Hearts do not affect questions, only final guesses.
          </div>
        </div>
        <div class="rule-item">
          <span class="rule-icon">💡</span>
          <div class="rule-text">
            <strong>Hints:</strong> Up to 3 hints reveal category → character count → first letter. Using hints reduces XP: 100 (no hints) → 70 (1 hint) → 40 (2+ hints).
          </div>
        </div>
        <div class="rule-item">
          <span class="rule-icon">⚙️</span>
          <div class="rule-text">
            <strong>Difficulty:</strong> <span style="color:var(--cyan)">Medium</span> — common attacks. <span style="color:var(--cyan)">Hard</span> — enterprise threats & APTs. <span style="color:var(--cyan)">Expert</span> — AI attacks, zero-days, obscure concepts. Higher difficulty = rarer items.
          </div>
        </div>
        <div class="rule-item">
          <span class="rule-icon">🏆</span>
          <div class="rule-text">
            <strong>Scoring:</strong> Correct guess earns XP based on hints used, questions asked, and hearts remaining. Compete on the leaderboard!
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
// ─────────────────────────────────────────────
// GAME STATE
// ─────────────────────────────────────────────
let state = {
  difficulty: 'medium',
  questionsLeft: 20,
  hearts: 3,
  hintsUsed: 0,
  askedQuestions: new Set(),
  gameActive: false,
  playerName: 'Agent_X'
};

// Questions with keys matching backend
const QUESTIONS = [
  { key: 'is_a_concept', label: 'Is it an abstract concept?' },
  { key: 'is_physical', label: 'Does it have a physical form?' },
  { key: 'involves_computers', label: 'Involves computers/digital systems?' },
  { key: 'is_malicious', label: 'Is it harmful or malicious?' },
  { key: 'is_defensive', label: 'Is it used for defense?' },
  { key: 'requires_internet', label: 'Requires internet connection?' },
  { key: 'involves_human_error', label: 'Exploits human error/psychology?' },
  { key: 'is_automated', label: 'Is it automated/self-executing?' },
  { key: 'predates_2000', label: 'Did it exist before year 2000?' },
  { key: 'is_illegal', label: 'Is it typically illegal?' },
  { key: 'is_widely_known', label: 'Known to the general public?' },
  { key: 'is_a_protocol', label: 'Is it a protocol or standard?' },
  { key: 'is_a_tool', label: 'Is it a specific tool or framework?' },
  { key: 'involves_deception', label: 'Involves deception/impersonation?' },
  { key: 'targets_individuals', label: 'Primarily targets individuals?' },
  { key: 'targets_organizations', label: 'Primarily targets organizations?' },
  { key: 'is_an_attack', label: 'Is it an attack/attack technique?' },
  { key: 'is_network_based', label: 'Operates over a network?' },
  { key: 'involves_ai', label: 'Involves Artificial Intelligence?' },
  { key: 'is_state_sponsored', label: 'Is it state-sponsored?' },
];

// Optimal question paths per category
const OPTIMAL_PATHS = {
  default: [
    { q: 'Is it harmful or malicious?', hint: 'Separates attacks from defenses' },
    { q: 'Is it an attack technique?', hint: 'Narrows to specific categories' },
    { q: 'Operates over a network?', hint: 'Network vs. local threats' },
    { q: 'Exploits human error?', hint: 'Social engineering vs. technical' },
    { q: 'Is it automated?', hint: 'Manual vs. automated attacks' },
    { q: 'Did it exist before 2000?', hint: 'Narrows era' },
    { q: 'Involves deception?', hint: 'Phishing vs. exploitation' },
    { q: 'Involves AI/ML?', hint: 'Identifies AI-specific threats' }
  ]
};

// ─────────────────────────────────────────────
// VIEW MANAGEMENT
// ─────────────────────────────────────────────
function showView(name) {
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
  document.getElementById('view-' + name).classList.add('active');
  const tabs = document.querySelectorAll('.nav-tab');
  const idx = ['game','leaderboard','howto'].indexOf(name);
  if (idx >= 0) tabs[idx].classList.add('active');
  
  if (name === 'leaderboard') loadLeaderboard();
}

// ─────────────────────────────────────────────
// DIFFICULTY SELECTION
// ─────────────────────────────────────────────
function selectDiff(diff) {
  state.difficulty = diff;
  document.querySelectorAll('.diff-card').forEach(c => c.classList.remove('selected'));
  document.getElementById('diff-' + diff).classList.add('selected');
}

// ─────────────────────────────────────────────
// GAME START
// ─────────────────────────────────────────────
async function startGame() {
  state.playerName = document.getElementById('player-name').value.trim() || 'Agent_X';
  
  const resp = await fetch('/api/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ difficulty: state.difficulty })
  });
  
  const data = await resp.json();
  
  state.questionsLeft = 20;
  state.hearts = 3;
  state.hintsUsed = 0;
  state.askedQuestions = new Set();
  state.gameActive = true;
  
  // Update HUD
  updateHUD();
  document.getElementById('hud-diff').textContent = state.difficulty.toUpperCase();
  document.getElementById('badge-text').textContent = `CATEGORY: ${data.category_hint}`;
  
  // Update questions remaining display
  document.getElementById('questions-remaining').textContent = state.questionsLeft;
  
  // Clear log
  document.getElementById('answer-log').innerHTML = '<div class="terminal-text" style="padding:8px">// Begin interrogation — type your questions to investigate</div>';
  
  // Reset hint and inputs
  document.getElementById('hint-display').style.display = 'none';
  document.getElementById('guess-input').value = '';
  document.getElementById('question-input').value = '';
  
  // Show game screen
  document.getElementById('screen-start').style.display = 'none';
  document.getElementById('screen-result').style.display = 'none';
  document.getElementById('screen-game').style.display = 'block';
}

// ─────────────────────────────────────────────
// SUBMIT QUESTION (User types their own)
// ─────────────────────────────────────────────
async function submitQuestion() {
  const input = document.getElementById('question-input');
  const questionText = input.value.trim();
  
  // Validate
  if (!questionText) {
    showFeedback('Please type a question', 'irr');
    return;
  }
  
  if (questionText.length < 5) {
    showFeedback('Question must be at least 5 characters', 'irr');
    return;
  }
  
  if (state.questionsLeft <= 0) {
    showFeedback('No questions remaining!', 'irr');
    return;
  }
  
  // Check if already asked (case-insensitive)
  const questionLower = questionText.toLowerCase();
  if (state.askedQuestions.has(questionLower)) {
    showFeedback('You already asked this question', 'irr');
    return;
  }
  
  // Disable input temporarily
  input.disabled = true;
  
  try {
    const resp = await fetch('/api/question', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question_text: questionText })
    });
    
    const data = await resp.json();
    
    if (data.error) {
      showFeedback(data.error, 'irr');
      input.disabled = false;
      return;
    }
    
    const answer = data.answer;
    
    state.askedQuestions.add(questionLower);
    state.questionsLeft = data.questions_remaining;
    
    // Show feedback
    showFeedback(answer);
    
    // Add to log
    addToLog(questionText, answer);
    
    // Update HUD and questions remaining
    updateHUD();
    document.getElementById('questions-remaining').textContent = state.questionsLeft;
    
    // Clear input
    input.value = '';
    input.disabled = false;
    input.focus();
    
    if (state.questionsLeft === 0) {
      showFeedback('No more questions! Make your final guess.', 'irr');
    }
  } catch (error) {
    showFeedback('Error asking question', 'irr');
    input.disabled = false;
  }
}

// Allow Enter key to submit question
document.addEventListener('DOMContentLoaded', function() {
  const questionInput = document.getElementById('question-input');
  if (questionInput) {
    questionInput.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        submitQuestion();
      }
    });
  }
});

function showFeedback(text, type) {
  let t = type;
  if (!t) {
    if (text === 'Yes') t = 'yes';
    else if (text === 'No') t = 'no';
    else t = 'irr';
  }
  
  const fb = document.createElement('div');
  fb.className = `feedback ${t}`;
  const icons = { yes: '✓ YES', no: '✗ NO', irr: '~ IRRELEVANT' };
  fb.textContent = (t === 'yes' || t === 'no' || t === 'irr') 
    ? icons[t] || text 
    : text;
  document.body.appendChild(fb);
  
  setTimeout(() => {
    fb.style.opacity = '0';
    fb.style.transition = 'opacity 0.5s';
    setTimeout(() => fb.remove(), 500);
  }, 2000);
}

function addToLog(question, answer) {
  const log = document.getElementById('answer-log');
  
  // Remove placeholder
  const placeholder = log.querySelector('.terminal-text');
  if (placeholder) placeholder.remove();
  
  const item = document.createElement('div');
  const cls = answer === 'Yes' ? 'yes' : answer === 'No' ? 'no' : 'irr';
  item.className = `log-item ${cls}`;
  item.innerHTML = `
    <span class="log-q">${question}</span>
    <span class="log-a ${cls}">${answer.toUpperCase()}</span>
  `;
  log.appendChild(item);
  log.scrollTop = log.scrollHeight;
}

// ─────────────────────────────────────────────
// HUD UPDATE
// ─────────────────────────────────────────────
function updateHUD() {
  document.getElementById('hud-questions').textContent = state.questionsLeft;
  document.getElementById('q-progress').style.width = (state.questionsLeft / 20 * 100) + '%';
  
  const hearts = ['', '❤️', '❤️❤️', '❤️❤️❤️'][state.hearts] || '💔💔💔';
  document.getElementById('hud-hearts').textContent = state.hearts > 0 
    ? '❤️'.repeat(state.hearts) + '🖤'.repeat(3 - state.hearts)
    : '💔💔💔';
}

// ─────────────────────────────────────────────
// SUBMIT GUESS
// ─────────────────────────────────────────────
async function submitGuess() {
  const guess = document.getElementById('guess-input').value.trim();
  if (!guess) return;
  
  const resp = await fetch('/api/guess', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      guess: guess, 
      player_name: state.playerName 
    })
  });
  
  const data = await resp.json();
  
  if (data.correct) {
    showResult(true, data);
  } else {
    state.hearts = data.hearts_remaining;
    updateHUD();
    
    if (data.game_over) {
      showResult(false, data);
    } else {
      showFeedback(`Wrong! ${state.hearts} ${state.hearts === 1 ? 'heart' : 'hearts'} remaining`, 'no');
      document.getElementById('guess-input').value = '';
      
      // Shake animation
      const input = document.getElementById('guess-input');
      input.style.borderColor = 'var(--danger)';
      setTimeout(() => { input.style.borderColor = ''; }, 1000);
    }
  }
}

// ─────────────────────────────────────────────
// HINT
// ─────────────────────────────────────────────
async function getHint() {
  if (state.hintsUsed >= 3) return;
  
  const resp = await fetch('/api/hint', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  });
  
  const data = await resp.json();
  state.hintsUsed = data.hints_used;
  
  const hintBox = document.getElementById('hint-display');
  hintBox.style.display = 'block';
  hintBox.innerHTML = `💡 <span style="color:var(--warning)">${data.hint}</span> <span style="color:var(--text-muted)">(Hint ${state.hintsUsed}/3 — XP reduced)</span>`;
  
  if (state.hintsUsed >= 3) {
    document.querySelector('[onclick="getHint()"]').disabled = true;
  }
}

// ─────────────────────────────────────────────
// SHOW RESULT
// ─────────────────────────────────────────────
function showResult(won, data) {
  document.getElementById('screen-game').style.display = 'none';
  document.getElementById('screen-result').style.display = 'block';
  
  document.getElementById('result-emoji').textContent = won ? '🎯' : '💀';
  const titleEl = document.getElementById('result-title');
  titleEl.textContent = won ? 'TARGET IDENTIFIED' : 'MISSION FAILED';
  titleEl.className = 'result-title ' + (won ? 'win' : 'lose');
  
  document.getElementById('result-name').textContent = data.item.name;
  document.getElementById('result-desc').textContent = data.item.description;
  
  if (won && data.xp_earned) {
    const xpBadge = document.getElementById('xp-badge');
    xpBadge.style.display = 'inline-block';
    xpBadge.textContent = `+${data.xp_earned} XP EARNED`;
  }
  
  // Optimal path
  buildOptimalPath(data.item);
}

function buildOptimalPath(item) {
  const container = document.getElementById('path-steps');
  container.innerHTML = '';
  
  const paths = OPTIMAL_PATHS.default;
  paths.forEach((step, i) => {
    const div = document.createElement('div');
    div.className = 'path-step';
    const isYes = Math.random() > 0.4; // Simulate optimal answers
    div.innerHTML = `
      <span class="step-num">${i+1}</span>
      <span class="step-q">${step.q} <span style="color:var(--text-muted);font-size:0.75rem">— ${step.hint}</span></span>
    `;
    container.appendChild(div);
  });
}

// ─────────────────────────────────────────────
// LEADERBOARD
// ─────────────────────────────────────────────
async function loadLeaderboard() {
  const resp = await fetch('/api/leaderboard');
  const data = await resp.json();
  
  const container = document.getElementById('lb-container');
  container.innerHTML = '';
  
  data.leaderboard.forEach((entry, i) => {
    const rankColors = ['gold', 'silver', 'bronze'];
    const rankClass = rankColors[i] || 'other';
    const rankEmoji = ['🥇','🥈','🥉'][i] || '#' + entry.rank;
    
    const row = document.createElement('div');
    row.className = 'lb-row';
    row.innerHTML = `
      <div class="lb-rank ${rankClass}">${rankEmoji}</div>
      <div class="lb-name">${entry.name}</div>
      <div class="lb-score">${entry.score.toLocaleString()}</div>
      <div class="lb-games">${entry.games}g</div>
    `;
    container.appendChild(row);
  });
}

// ─────────────────────────────────────────────
// NEW GAME
// ─────────────────────────────────────────────
function startNew() {
  state.gameActive = false;
  document.getElementById('screen-game').style.display = 'none';
  document.getElementById('screen-result').style.display = 'none';
  document.getElementById('screen-start').style.display = 'block';
}

// ─────────────────────────────────────────────
// KEYBOARD
// ─────────────────────────────────────────────
document.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && state.gameActive) {
    const input = document.getElementById('guess-input');
    if (document.activeElement === input) submitGuess();
  }
});

// INIT
updateHUD();
</script>
</body>
</html>'''

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
