"""
╔══════════════════════════════════════════════════╗
║   CIPHER — Advanced 20 Questions Game            ║
║   Powered by Google Gemini AI (fully dynamic)    ║
║   Run: streamlit run app.py                      ║
╚══════════════════════════════════════════════════╝
"""

import streamlit as st
import json
import time
import random
import requests
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CIPHER — 20 Questions",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
#  CUSTOM CSS — Cyberpunk Blue/Green Aesthetic
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Rajdhani:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;600&display=swap');

/* ── Root variables ── */
:root {
  --bg-deep:    #020b18;
  --bg-dark:    #041224;
  --bg-card:    #061a2e;
  --blue-700:   #0f3460;
  --blue-600:   #155fa0;
  --blue-500:   #1e7fcb;
  --blue-400:   #38a3e8;
  --blue-300:   #6ec0f5;
  --green-500:  #0d9f53;
  --green-400:  #17c96a;
  --green-300:  #4de890;
  --cyan:       #00e5ff;
  --teal:       #00bcd4;
  --accent:     #00ff88;
  --warning:    #ff9f1c;
  --danger:     #ff3a5c;
  --text-pri:   #e8f4ff;
  --text-sec:   #7ab5d8;
  --text-muted: #3d6e8a;
  --border:     #0d3a5c;
}

/* ── Global reset ── */
html, body, [class*="css"] {
  font-family: 'Rajdhani', sans-serif !important;
  background-color: var(--bg-deep) !important;
  color: var(--text-pri) !important;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem !important; max-width: 1100px !important; }

/* ── Animated background grid ── */
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(30,127,203,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(30,127,203,0.04) 1px, transparent 1px);
  background-size: 42px 42px;
  pointer-events: none;
  z-index: 0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: var(--bg-card) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text-sec) !important; }

/* ── Buttons ── */
.stButton > button {
  font-family: 'Orbitron', monospace !important;
  font-size: 0.68rem !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  border-radius: 10px !important;
  transition: all 0.25s ease !important;
  border: 1px solid var(--blue-600) !important;
  background: linear-gradient(135deg, var(--blue-700), var(--blue-600)) !important;
  color: var(--text-pri) !important;
  padding: 0.5rem 1.2rem !important;
}
.stButton > button:hover {
  border-color: var(--cyan) !important;
  color: var(--cyan) !important;
  box-shadow: 0 0 18px rgba(0,229,255,0.3) !important;
  transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }
.stButton > button:disabled {
  opacity: 0.3 !important;
  cursor: not-allowed !important;
  transform: none !important;
}

/* ── Text input ── */
.stTextInput > div > div > input, .stTextArea textarea {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  color: var(--text-pri) !important;
  border-radius: 10px !important;
  font-family: 'Rajdhani', sans-serif !important;
  font-size: 1rem !important;
}
.stTextInput > div > div > input:focus, .stTextArea textarea:focus {
  border-color: var(--blue-400) !important;
  box-shadow: 0 0 12px rgba(30,127,203,0.35) !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  color: var(--text-pri) !important;
}

/* ── Metric widgets ── */
[data-testid="stMetric"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  padding: 14px !important;
}
[data-testid="stMetricValue"] {
  font-family: 'Orbitron', monospace !important;
  color: var(--cyan) !important;
}
[data-testid="stMetricLabel"] {
  font-family: 'JetBrains Mono', monospace !important;
  color: var(--text-muted) !important;
  font-size: 0.65rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.15em !important;
}

/* ── Progress bar ── */
.stProgress > div > div > div {
  background: linear-gradient(90deg, var(--blue-500), var(--cyan)) !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  font-family: 'Orbitron', monospace !important;
  font-size: 0.7rem !important;
  letter-spacing: 0.1em !important;
  color: var(--blue-300) !important;
}

/* ── Divider ── */
hr {
  border-color: var(--border) !important;
  margin: 1.2rem 0 !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--bg-card) !important;
  border-radius: 12px !important;
  padding: 6px !important;
  gap: 4px !important;
  border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
  font-family: 'Orbitron', monospace !important;
  font-size: 0.65rem !important;
  letter-spacing: 0.1em !important;
  background: transparent !important;
  color: var(--text-muted) !important;
  border-radius: 8px !important;
  padding: 8px 18px !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, var(--blue-700), var(--blue-600)) !important;
  color: var(--cyan) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-dark); }
::-webkit-scrollbar-thumb { background: var(--blue-700); border-radius: 3px; }

/* ── Toggle ── */
.stToggle { }
[data-testid="stToggleSwitch"] > div {
  background: var(--blue-700) !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  HTML COMPONENT HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def logo_html():
    return """
    <div style="text-align:center;padding:24px 0 8px">
      <div style="font-family:'Orbitron',monospace;font-size:clamp(1.8rem,5vw,3.2rem);
                  font-weight:900;letter-spacing:0.3em;
                  background:linear-gradient(135deg,#00e5ff,#38a3e8,#00ff88);
                  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                  filter:drop-shadow(0 0 24px rgba(0,229,255,0.5));">
        CIPHER
      </div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;
                  color:#3d6e8a;letter-spacing:0.35em;margin-top:6px;text-transform:uppercase;">
        ⬡ Advanced 20 Questions · Powered by Gemini AI ⬡
      </div>
    </div>
    """

def card_html(content, glow_color="blue"):
    glow = "rgba(30,127,203,0.2)" if glow_color == "blue" else "rgba(0,255,136,0.2)"
    return f"""
    <div style="background:#061a2e;border:1px solid #0d3a5c;border-radius:16px;
                padding:20px;margin:8px 0;
                box-shadow:0 0 20px {glow};">
      {content}
    </div>
    """

def badge_html(text, color="cyan"):
    colors = {
        "cyan":   ("#00e5ff", "rgba(0,229,255,0.07)", "rgba(0,229,255,0.2)"),
        "green":  ("#4de890", "rgba(13,159,83,0.1)",  "rgba(77,232,144,0.3)"),
        "red":    ("#ff7a92", "rgba(255,58,92,0.08)", "rgba(255,58,92,0.35)"),
        "orange": ("#ffcc7a", "rgba(255,159,28,0.08)","rgba(255,159,28,0.3)"),
        "blue":   ("#6ec0f5", "rgba(30,127,203,0.1)", "rgba(110,192,245,0.3)"),
    }
    fg, bg, border_c = colors.get(color, colors["cyan"])
    return f"""
    <span style="display:inline-flex;align-items:center;gap:6px;
                 background:{bg};border:1px solid {border_c};
                 border-radius:8px;padding:6px 14px;
                 font-family:'JetBrains Mono',monospace;
                 font-size:0.72rem;color:{fg};letter-spacing:0.1em;">
      {text}
    </span>
    """

def section_title_html(text):
    return f"""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px">
      <span style="font-family:'Orbitron',monospace;font-size:0.62rem;
                   color:#3d6e8a;text-transform:uppercase;letter-spacing:0.2em;">
        {text}
      </span>
      <div style="flex:1;height:1px;background:#0d3a5c;"></div>
    </div>
    """

def answer_tag(answer):
    if answer == "Yes":
        return badge_html("✓ YES", "green")
    elif answer == "No":
        return badge_html("✗ NO", "red")
    else:
        return badge_html("~ IRRELEVANT", "orange")

def hearts_html(count):
    filled = "❤️" * count
    empty  = "🖤" * (3 - count)
    return f"<span style='font-size:1.4rem;letter-spacing:3px'>{filled}{empty}</span>"

def xp_badge_html(xp):
    return f"""
    <div style="text-align:center;margin:16px 0">
      <span style="display:inline-block;
                   background:linear-gradient(135deg,#1a3a20,#0d9f53);
                   border:1px solid #17c96a;border-radius:50px;
                   padding:12px 36px;font-family:'Orbitron',monospace;
                   font-size:1.1rem;color:#00ff88;
                   box-shadow:0 0 24px rgba(13,159,83,0.4);">
        +{xp} XP EARNED
      </span>
    </div>
    """

def answer_log_html(log):
    if not log:
        return """<div style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;
                              color:#3d6e8a;padding:10px">
                    // No questions asked yet — begin your investigation
                  </div>"""
    items = []
    for entry in log:
        ans = entry["answer"]
        border = "#17c96a" if ans=="Yes" else ("#ff3a5c" if ans=="No" else "#ff9f1c")
        fg     = "#4de890" if ans=="Yes" else ("#ff7a92" if ans=="No" else "#ffcc7a")
        items.append(f"""
          <div style="display:flex;align-items:flex-start;gap:10px;
                      padding:8px 12px;background:#082040;border-radius:8px;
                      border-left:3px solid {border};margin-bottom:6px">
            <span style="flex:1;color:#7ab5d8;font-size:0.82rem;line-height:1.4">
              {entry['question']}
            </span>
            <span style="font-family:'Orbitron',monospace;font-size:0.62rem;
                         font-weight:700;color:{fg};white-space:nowrap">
              {ans.upper()}
            </span>
          </div>
        """)
    return "\n".join(items)

def leaderboard_row_html(rank, name, score, games, is_new=False):
    icons  = {1:"🥇",2:"🥈",3:"🥉"}
    colors = {1:"#ffd700",2:"#c0c0c0",3:"#cd7f32"}
    icon   = icons.get(rank, f"#{rank}")
    color  = colors.get(rank, "#3d6e8a")
    highlight = "border-color:#00ff88;box-shadow:0 0 12px rgba(0,255,136,0.2);" if is_new else ""
    return f"""
    <div style="display:grid;grid-template-columns:44px 1fr auto auto;
                gap:12px;align-items:center;
                padding:12px 16px;background:#082040;
                border:1px solid #0d3a5c;border-radius:10px;
                margin-bottom:7px;{highlight}">
      <span style="font-family:'Orbitron',monospace;font-size:0.9rem;
                   font-weight:700;color:{color};text-align:center">{icon}</span>
      <span style="font-family:'Rajdhani',sans-serif;font-weight:600;
                   font-size:0.95rem;color:#e8f4ff">{name}</span>
      <span style="font-family:'Orbitron',monospace;font-size:0.85rem;
                   color:#00ff88;font-weight:700">{score:,}</span>
      <span style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;
                   color:#3d6e8a;text-align:right">{games}g</span>
    </div>
    """


# ─────────────────────────────────────────────────────────────────────────────
#  GEMINI API  (direct REST, no SDK needed)
# ─────────────────────────────────────────────────────────────────────────────

GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

def gemini_chat(api_key: str, model: str, messages: list, system: str = "",
                temperature: float = 0.7, max_tokens: int = 512) -> str:
    """
    Call Gemini via raw REST with optimized token usage.
    messages: [{"role": "user"|"model", "parts": [{"text": "..."}]}]
    """
    url = f"{GEMINI_BASE}/{model}:generateContent?key={api_key}"

    payload = {
        "contents": messages,
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens,
            "candidateCount": 1,  # Only generate one response
        }
    }
    if system:
        payload["system_instruction"] = {"parts": [{"text": system}]}

    try:
        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except requests.exceptions.HTTPError as e:
        code = e.response.status_code if e.response else "?"
        body = e.response.text[:300] if e.response else ""
        return f"__ERROR__:HTTP {code}: {body}"
    except Exception as e:
        return f"__ERROR__:{str(e)}"


def gemini_json(api_key, model, prompt, system="", temperature=0.7, max_tokens=600):
    """Gemini call expecting a clean JSON response with optimized token usage."""
    messages = [{"role": "user", "parts": [{"text": prompt}]}]
    raw = gemini_chat(api_key, model, messages, system=system,
                      temperature=temperature, max_tokens=max_tokens)
    if raw.startswith("__ERROR__"):
        return None, raw
    # Strip markdown fences
    clean = raw.strip()
    for fence in ["```json", "```JSON", "```"]:
        if fence in clean:
            clean = clean.split(fence, 1)[-1].rsplit("```", 1)[0].strip()
    try:
        return json.loads(clean), None
    except json.JSONDecodeError:
        return None, f"JSON parse failed: {clean[:200]}"


# ─────────────────────────────────────────────────────────────────────────────
#  GAME LOGIC — ALL AI-DRIVEN
# ─────────────────────────────────────────────────────────────────────────────

CATEGORIES = [
    "Cybersecurity Concept",
    "AI / Machine Learning Technique",
    "Global Landmark",
    "Country",
    "Historical Cyber Incident",
    "Rare / Obscure Technology",
    "Programming Language or Framework",
    "Scientific Phenomenon",
    "Mathematical Concept",
    "Famous Algorithm",
    "Space / Astronomy Object",
    "Cryptographic Primitive",
]

DIFFICULTY_CONFIGS = {
    "Medium": {
        "desc": "Common, well-known subjects. Good for beginners.",
        "prompt_note": "Choose something moderately well-known but not trivially obvious.",
        "xp_base": 80,
        "icon": "🛡️",
    },
    "Hard": {
        "desc": "Technical, obscure, or niche subjects.",
        "prompt_note": "Choose something technical, niche, or requiring domain expertise.",
        "xp_base": 120,
        "icon": "⚔️",
    },
    "Expert": {
        "desc": "Highly obscure, multi-domain, edge-case subjects.",
        "prompt_note": "Choose something very obscure, highly technical, or that spans multiple domains. It should be genuinely hard to identify in 20 questions.",
        "xp_base": 200,
        "icon": "☠️",
    },
}

def pick_secret(api_key, model, difficulty, category, player_name="Player"):
    """Ask Gemini to secretly pick a subject and return its metadata."""
    diff_note = DIFFICULTY_CONFIGS[difficulty]["prompt_note"]
    
    system = """You are a game master selecting subjects for a 20-questions game. Pick specific, well-defined subjects that are fair and guessable."""
    
    prompt = f"""Select ONE specific subject from category: "{category}"
Difficulty: {difficulty}. {diff_note}

Requirements:
- Real, specific, verifiable subject
- Guessable within 20 yes/no questions
- Not too obscure

Respond ONLY with valid JSON:
{{
  "name": "<exact name>",
  "category": "{category}",
  "difficulty": "{difficulty}",
  "description": "<one sentence>",
  "fun_fact": "<one interesting fact>",
  "optimal_first_questions": ["<Q1>","<Q2>","<Q3>","<Q4>","<Q5>"]
}}"""
    data, err = gemini_json(api_key, model, prompt, system=system, temperature=0.95, max_tokens=500)
    return data, err


def answer_question(api_key, model, secret_name, secret_desc, question_text):
    """Ask Gemini to answer a yes/no question about the secret."""
    system = """You are a precise game master for a 20-questions game. Answer questions accurately based ONLY on the secret subject provided. Be consistent and logical."""
    
    prompt = f"""Secret subject: "{secret_name}"
Description: {secret_desc}

Player's question: "{question_text}"

Rules:
1. Answer "Yes" if the question is TRUE about this subject
2. Answer "No" if the question is FALSE about this subject  
3. Answer "Irrelevant" ONLY if the question cannot be answered yes/no (e.g., "What color is it?" or nonsensical questions)
4. Be consistent - if you answer "Yes" to a general category, don't contradict it later
5. Consider the question carefully - "Is it an attack?" and "Is it a phishing attack?" are different questions

Respond ONLY with valid JSON:
{{"answer": "Yes"|"No"|"Irrelevant", "brief_reason": "<5 words max>"}}"""

    data, err = gemini_json(api_key, model, prompt, system=system, temperature=0.1)
    if data and "answer" in data:
        ans = data["answer"].strip()
        if ans not in ("Yes", "No", "Irrelevant"):
            ans = "Irrelevant"
        return ans, data.get("brief_reason", "")
    return "Irrelevant", f"Error: {err}"


def generate_question_suggestions(api_key, model, secret_name, secret_desc,
                                   already_asked, difficulty, category):
    """Ask Gemini to suggest 12 dynamic questions tailored to current game state."""
    asked_str = "\n".join(f"- {q}" for q in already_asked[-10:]) if already_asked else "None yet"  # Only last 10 to reduce tokens
    
    system = """You are a strategic 20-questions expert. Generate diverse, specific questions that efficiently narrow down possibilities. Avoid generic questions."""
    
    prompt = f"""Secret: "{secret_name}" (Category: {category})
Description: {secret_desc}

Recent questions asked:
{asked_str}

Generate 12 NEW strategic yes/no questions that:
1. Are NOT similar to already asked questions
2. Are SPECIFIC to {category} domain (avoid generic questions like "Is it related to cybersecurity?")
3. Narrow down possibilities efficiently
4. Cover different aspects: technical details, time period, scope, purpose, implementation, impact
5. Are clear and unambiguous

Respond ONLY with valid JSON:
{{"questions": ["Q1","Q2","Q3","Q4","Q5","Q6","Q7","Q8","Q9","Q10","Q11","Q12"]}}"""

    data, err = gemini_json(api_key, model, prompt, system=system, temperature=0.6)
    if data and "questions" in data:
        return data["questions"], None
    return [], err


def validate_guess(api_key, model, secret_name, guess):
    """Flexible guess validation via Gemini."""
    system = """You are a fair judge for a guessing game. Validate answers considering exact matches, abbreviations, and alternate names."""
    
    prompt = f"""Secret: "{secret_name}"
Player's guess: "{guess}"

Is this correct? Consider exact matches, abbreviations, alternate names, and partial matches.

Respond ONLY with valid JSON:
{{"correct": true|false, "reason": "<brief reason>"}}"""

    data, err = gemini_json(api_key, model, prompt, system=system, temperature=0.1, max_tokens=150)
    if data is not None:
        return bool(data.get("correct", False)), data.get("reason", "")
    return False, f"Validation error: {err}"


def generate_hint(api_key, model, secret_name, secret_desc, hints_used, question_log, category):
    """Generate a contextual hint that doesn't give away the answer."""
    recent_questions = "\n".join([f"- {q['question']} → {q['answer']}" for q in question_log[-5:]]) if question_log else "None yet"
    
    system = """You are a helpful hint generator. Provide progressive hints that guide without revealing the answer directly."""
    
    prompt = f"""Secret: "{secret_name}" (Category: {category})
Description: {secret_desc}

Recent Q&A:
{recent_questions}

Generate hint #{hints_used + 1}. Make it contextual and progressive:
- Hint 1: Narrow down the sub-category or time period (e.g., "It's a type of malware from the 2010s")
- Hint 2: Provide a specific characteristic or notable feature (e.g., "It spreads through a specific vulnerability")
- Hint 3: Give a strong clue like word length, first letter, or famous incident (e.g., "It has 8 letters and starts with 'W'")

DO NOT use generic hints like "It's related to cybersecurity" - be SPECIFIC to this particular subject.

Respond ONLY with valid JSON:
{{"hint": "<the hint text>", "hint_level": {hints_used + 1}}}"""

    data, err = gemini_json(api_key, model, prompt, system=system, temperature=0.4)
    if data and "hint" in data:
        return data["hint"], None
    return "Hint unavailable.", err


def generate_optimal_path(api_key, model, secret_name, secret_desc, question_log):
    """Post-game: generate the truly optimal question path."""
    # Only include last 10 questions to reduce token usage
    recent_log = question_log[-10:] if len(question_log) > 10 else question_log
    
    system = """You are a strategic game analyst. Provide concise, actionable optimal strategies."""
    
    prompt = f"""Secret: "{secret_name}"
Description: {secret_desc}

Player's recent questions (last 10):
{json.dumps(recent_log, indent=2)}

Generate 8 OPTIMAL questions that would efficiently identify this subject.

Respond ONLY with valid JSON:
{{
  "optimal_path": [
    {{"step": 1, "question": "...", "expected_answer": "Yes|No", "why": "..."}},
    ...
  ],
  "strategy_tip": "<one sentence tip>"
}}"""

    data, err = gemini_json(api_key, model, prompt, system=system, temperature=0.3, max_tokens=700)
    return data, err


# ─────────────────────────────────────────────────────────────────────────────
#  SESSION STATE DEFAULTS
# ─────────────────────────────────────────────────────────────────────────────

def init_state():
    defaults = {
        # Config
        "api_key": "",
        "gemini_model": "gemini-1.5-flash",
        "player_name": "Agent_X",

        # Feature toggles
        "feature_dynamic_questions": True,
        "feature_hints": True,
        "feature_optimal_path": True,
        "feature_fun_facts": True,
        "feature_custom_category": False,

        # Game state
        "game_phase": "setup",   # setup | playing | result
        "difficulty": "Hard",
        "category": "Cybersecurity Concept",
        "custom_category": "",

        "secret": None,          # full secret dict from Gemini
        "questions_left": 20,
        "hearts": 3,
        "hints_used": 0,
        "question_log": [],      # [{"question":..., "answer":..., "reason":...}]
        "asked_set": set(),
        "suggested_questions": [],
        "current_hint": None,
        "wrong_guesses": 0,
        "xp_earned": 0,

        # UI state
        "loading_msg": "",
        "error_msg": "",
        "result_data": None,

        # Leaderboard
        "leaderboard": [
            {"name": "ShadowHexer",   "score": 2850, "games": 31, "rank": 1},
            {"name": "NullByte_X",    "score": 2340, "games": 27, "rank": 2},
            {"name": "CipherWolf",    "score": 1980, "games": 22, "rank": 3},
            {"name": "ByteKnight",    "score": 1650, "games": 19, "rank": 4},
            {"name": "GhostProtocol", "score": 1200, "games": 15, "rank": 5},
        ],
        "player_rank": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()
S = st.session_state   # convenience alias


# ─────────────────────────────────────────────────────────────────────────────
#  SIDEBAR — Config & Toggles
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="font-family:'Orbitron',monospace;font-size:0.85rem;
                color:#00e5ff;letter-spacing:0.15em;padding:10px 0 16px;
                text-align:center;border-bottom:1px solid #0d3a5c;margin-bottom:16px">
      ⚙ CONTROL PANEL
    </div>
    """, unsafe_allow_html=True)

    # API Key
    st.markdown("**🔑 Gemini API Key**")
    api_input = st.text_input("", value=S.api_key,
                               type="password", placeholder="AIza...",
                               key="_api_key_input", label_visibility="collapsed")
    if api_input != S.api_key:
        S.api_key = api_input

    # Model
    model_choice = st.selectbox(
        "🤖 Model",
        ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash", "gemini-2.0-flash-exp"],
        index=["gemini-1.5-flash","gemini-1.5-pro","gemini-2.0-flash","gemini-2.0-flash-exp"]
              .index(S.gemini_model) if S.gemini_model in
              ["gemini-1.5-flash","gemini-1.5-pro","gemini-2.0-flash","gemini-2.0-flash-exp"] else 0,
    )
    S.gemini_model = model_choice

    st.divider()

    # Player name
    pname = st.text_input("🕹️ Your Codename", value=S.player_name, max_chars=20)
    S.player_name = pname or "Agent_X"

    st.divider()

    st.markdown("""<div style="font-family:'Orbitron',monospace;font-size:0.65rem;
                               color:#3d6e8a;letter-spacing:0.2em;margin-bottom:10px">
                    ⬡ FEATURE TOGGLES
                   </div>""", unsafe_allow_html=True)

    S.feature_dynamic_questions = st.toggle(
        "Dynamic AI Questions", value=S.feature_dynamic_questions,
        help="Gemini generates context-aware question suggestions each round"
    )
    S.feature_hints = st.toggle(
        "Hint System", value=S.feature_hints,
        help="Allow up to 3 AI-generated contextual hints (reduces XP)"
    )
    S.feature_optimal_path = st.toggle(
        "Optimal Path Reveal", value=S.feature_optimal_path,
        help="Post-game analysis showing the ideal question strategy"
    )
    S.feature_fun_facts = st.toggle(
        "Fun Facts on Reveal", value=S.feature_fun_facts,
        help="Show an interesting fact about the answer after the game"
    )
    S.feature_custom_category = st.toggle(
        "Custom Category Input", value=S.feature_custom_category,
        help="Type any category you want Gemini to pick from"
    )

    st.divider()

    if st.button("🔄 Reset Game", use_container_width=True):
        keys_to_reset = ["game_phase","secret","questions_left","hearts","hints_used",
                         "question_log","asked_set","suggested_questions","current_hint",
                         "wrong_guesses","xp_earned","loading_msg","error_msg",
                         "result_data","player_rank"]
        for k in keys_to_reset:
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()

    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.62rem;
                color:#1a3d5c;text-align:center;padding-top:16px">
      CIPHER v2.0 · Gemini-Powered
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN CONTENT — TABS
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(logo_html(), unsafe_allow_html=True)

tab_game, tab_leaderboard, tab_howto = st.tabs(["🎮 PLAY", "🏆 LEADERBOARD", "📖 HOW TO PLAY"])


# ═══════════════════════════════════════════════════════════════════════════
#  TAB: GAME
# ═══════════════════════════════════════════════════════════════════════════
with tab_game:

    # ── API Key guard ──
    if not S.api_key:
        st.markdown(card_html(f"""
          <div style='text-align:center;padding:20px 0'>
            {section_title_html("AUTHENTICATION REQUIRED")}
            <div style='font-size:2.5rem;margin-bottom:12px'>🔑</div>
            <div style='color:#7ab5d8;font-size:0.9rem;line-height:1.6;max-width:400px;margin:0 auto'>
              Enter your <strong style='color:#00e5ff'>Google Gemini API key</strong> 
              in the sidebar to begin.<br><br>
              Get a free key at 
              <span style='color:#00ff88'>aistudio.google.com</span>
            </div>
          </div>
        """), unsafe_allow_html=True)
        st.stop()

    # ══════════════════════════════════════════
    #  PHASE: SETUP
    # ══════════════════════════════════════════
    if S.game_phase == "setup":

        st.markdown(section_title_html("GAME CONFIGURATION"), unsafe_allow_html=True)

        col_diff, col_cat = st.columns([1, 1], gap="large")

        with col_diff:
            st.markdown("**Difficulty**")
            diff_cols = st.columns(3)
            for i, (diff_name, cfg) in enumerate(DIFFICULTY_CONFIGS.items()):
                with diff_cols[i]:
                    selected = S.difficulty == diff_name
                    border = "border:2px solid #00e5ff;" if selected else "border:1px solid #0d3a5c;"
                    glow = "box-shadow:0 0 16px rgba(0,229,255,0.3);" if selected else ""
                    st.markdown(f"""
                    <div style="background:#061a2e;{border}border-radius:14px;
                                padding:16px 10px;text-align:center;{glow}cursor:pointer">
                      <div style='font-size:1.8rem'>{cfg['icon']}</div>
                      <div style='font-family:"Orbitron",monospace;font-size:0.65rem;
                                  color:#00e5ff;letter-spacing:0.1em;margin:6px 0'>
                        {diff_name.upper()}
                      </div>
                      <div style='font-size:0.75rem;color:#3d6e8a;line-height:1.3'>
                        {cfg['desc']}
                      </div>
                      <div style='font-family:"JetBrains Mono",monospace;font-size:0.65rem;
                                  color:#00ff88;margin-top:8px'>
                        +{cfg['xp_base']} XP base
                      </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(diff_name, key=f"diff_{diff_name}",
                                 use_container_width=True):
                        S.difficulty = diff_name
                        st.rerun()

        with col_cat:
            st.markdown("**Category**")
            if S.feature_custom_category:
                custom_cat = st.text_input("Custom Category", value=S.custom_category,
                                           placeholder="e.g. Ancient Roman technology")
                S.custom_category = custom_cat
                if custom_cat:
                    S.category = custom_cat
            else:
                cat = st.selectbox("", CATEGORIES,
                                   index=CATEGORIES.index(S.category) if S.category in CATEGORIES else 0,
                                   label_visibility="collapsed")
                S.category = cat

        st.markdown("<br>", unsafe_allow_html=True)

        # Active features preview
        active_feats = []
        if S.feature_dynamic_questions: active_feats.append("🧠 Dynamic Questions")
        if S.feature_hints:             active_feats.append("💡 Hints")
        if S.feature_optimal_path:      active_feats.append("⚡ Optimal Path")
        if S.feature_fun_facts:         active_feats.append("✨ Fun Facts")

        if active_feats:
            st.markdown(f"""
            <div style='display:flex;flex-wrap:wrap;gap:8px;margin-bottom:20px'>
              {''.join(badge_html(f, "blue") for f in active_feats)}
            </div>
            """, unsafe_allow_html=True)

        col_btn, col_info = st.columns([1, 2])
        with col_btn:
            start_clicked = st.button("🚀 INITIALIZE GAME", type="primary",
                                      use_container_width=True)

        if start_clicked:
            if not S.api_key:
                st.error("Enter your Gemini API key in the sidebar.")
            else:
                category = S.custom_category if (S.feature_custom_category and S.custom_category) else S.category
                with st.spinner(f"🤖 Gemini is picking a secret {category}..."):
                    secret, err = pick_secret(S.api_key, S.gemini_model,
                                              S.difficulty, category, S.player_name)
                if err and not secret:
                    st.error(f"Gemini error: {err}")
                else:
                    # Reset ALL game state for new game
                    S.secret            = secret
                    S.questions_left    = 20
                    S.hearts            = 3
                    S.hints_used        = 0
                    S.question_log      = []
                    S.asked_set         = set()
                    S.suggested_questions = []  # Clear old suggestions
                    S.current_hint      = None  # Clear old hint
                    S.wrong_guesses     = 0
                    S.xp_earned         = 0
                    S.error_msg         = ""
                    S.result_data       = None
                    S.player_rank       = None
                    S.game_phase        = "playing"

                    # Pre-fetch first batch of suggested questions
                    if S.feature_dynamic_questions:
                        qs, _ = generate_question_suggestions(
                            S.api_key, S.gemini_model,
                            S.secret["name"], S.secret["description"],
                            [], S.difficulty, S.secret["category"]
                        )
                        S.suggested_questions = qs

                    st.rerun()

    # ══════════════════════════════════════════
    #  PHASE: PLAYING
    # ══════════════════════════════════════════
    elif S.game_phase == "playing" and S.secret:

        secret = S.secret

        # ── HUD ──
        hud_cols = st.columns(4)
        with hud_cols[0]:
            st.metric("Questions Left", S.questions_left)
        with hud_cols[1]:
            st.markdown(f"""
            <div style="background:#061a2e;border:1px solid #0d3a5c;border-radius:12px;
                        padding:14px 12px;text-align:center">
              <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
                          color:#3d6e8a;text-transform:uppercase;letter-spacing:0.15em;mb:6px">
                Lives
              </div>
              {hearts_html(S.hearts)}
            </div>
            """, unsafe_allow_html=True)
        with hud_cols[2]:
            st.metric("Difficulty", S.difficulty)
        with hud_cols[3]:
            st.metric("Category", secret.get("category", "—")[:18])

        # Progress bar
        st.progress(S.questions_left / 20, text=None)

        # Category badge
        st.markdown(f"""
        <div style='margin:8px 0 16px'>
          {badge_html(f"🔍 CATEGORY: {secret.get('category','Unknown').upper()}", "cyan")}
        </div>
        """, unsafe_allow_html=True)

        # ── Error message ──
        if S.error_msg:
            st.warning(S.error_msg)
            S.error_msg = ""

        # ── Two-column layout: Questions | Log ──
        col_left, col_right = st.columns([3, 2], gap="large")

        with col_left:
            st.markdown(section_title_html("ASK A QUESTION"), unsafe_allow_html=True)

            # Tab: Suggested vs Custom
            q_tab_suggest, q_tab_custom = st.tabs(["💡 Suggested", "✏️ Custom"])

            with q_tab_suggest:
                if S.feature_dynamic_questions:
                    if not S.suggested_questions:
                        if st.button("🔄 Generate Questions", use_container_width=True):
                            with st.spinner("🤖 Thinking up strategic questions..."):
                                qs, err = generate_question_suggestions(
                                    S.api_key, S.gemini_model,
                                    secret["name"], secret["description"],
                                    list(S.asked_set), S.difficulty, secret["category"]
                                )
                            if qs:
                                S.suggested_questions = qs
                                st.rerun()
                            else:
                                st.error(f"Could not generate questions: {err}")
                    else:
                        # Display in 2 columns of buttons
                        available = [q for q in S.suggested_questions if q not in S.asked_set]
                        if not available:
                            st.markdown("""<div style='color:#3d6e8a;font-size:0.82rem;
                                           font-family:"JetBrains Mono",monospace;padding:10px'>
                                           All suggestions used. Refresh for more.
                                           </div>""", unsafe_allow_html=True)
                        else:
                            btn_cols = st.columns(2)
                            for idx, q in enumerate(available[:12]):
                                with btn_cols[idx % 2]:
                                    if st.button(q, key=f"sq_{idx}_{hash(q)}",
                                                 use_container_width=True,
                                                 disabled=S.questions_left <= 0):
                                        with st.spinner("🤖 Consulting the oracle..."):
                                            ans, reason = answer_question(
                                                S.api_key, S.gemini_model,
                                                secret["name"], secret["description"], q
                                            )
                                        S.question_log.append({"question": q, "answer": ans, "reason": reason})
                                        S.asked_set.add(q)
                                        S.questions_left -= 1

                                        # Refresh suggestions
                                        if S.feature_dynamic_questions and len(available) <= 4:
                                            with st.spinner("🔄 Refreshing questions..."):
                                                new_qs, _ = generate_question_suggestions(
                                                    S.api_key, S.gemini_model,
                                                    secret["name"], secret["description"],
                                                    list(S.asked_set), S.difficulty, secret["category"]
                                                )
                                            if new_qs:
                                                S.suggested_questions = new_qs

                                        st.rerun()

                        if st.button("🔄 Refresh Suggestions", use_container_width=True):
                            with st.spinner("🤖 Generating new questions..."):
                                qs, err = generate_question_suggestions(
                                    S.api_key, S.gemini_model,
                                    secret["name"], secret["description"],
                                    list(S.asked_set), S.difficulty, secret["category"]
                                )
                            if qs:
                                S.suggested_questions = qs
                                st.rerun()
                else:
                    st.info("Dynamic questions are disabled. Enable in sidebar or use Custom tab.")

            with q_tab_custom:
                custom_q = st.text_input("Type any yes/no question",
                                         placeholder="e.g. Is it older than 50 years?",
                                         key="custom_q_input")
                if st.button("Ask This Question", use_container_width=True,
                             disabled=not custom_q or S.questions_left <= 0):
                    if custom_q not in S.asked_set:
                        with st.spinner("🤖 Answering..."):
                            ans, reason = answer_question(
                                S.api_key, S.gemini_model,
                                secret["name"], secret["description"], custom_q
                            )
                        S.question_log.append({"question": custom_q, "answer": ans, "reason": reason})
                        S.asked_set.add(custom_q)
                        S.questions_left -= 1
                        st.rerun()
                    else:
                        S.error_msg = "You already asked that question!"
                        st.rerun()

        with col_right:
            st.markdown(section_title_html("INTERROGATION LOG"), unsafe_allow_html=True)
            log_html = answer_log_html(S.question_log)
            st.markdown(f"""
            <div style="max-height:320px;overflow-y:auto;padding-right:4px">
              {log_html}
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # ── GUESS + HINTS ──
        st.markdown(section_title_html("SUBMIT FINAL ANSWER"), unsafe_allow_html=True)

        guess_col, btn_col, hint_col = st.columns([3, 1, 1])

        with guess_col:
            guess_text = st.text_input("", placeholder="Type your answer here...",
                                       key="guess_input", label_visibility="collapsed")

        with btn_col:
            submit_guess = st.button("⚡ SUBMIT", use_container_width=True,
                                     type="primary", disabled=not guess_text)

        with hint_col:
            hints_btn_disabled = (not S.feature_hints) or (S.hints_used >= 3)
            get_hint_btn = st.button(
                f"💡 HINT {'(' + str(S.hints_used) + '/3)' if S.feature_hints else '(OFF)'}",
                use_container_width=True,
                disabled=hints_btn_disabled
            )

        # Display current hint
        if S.current_hint:
            st.markdown(f"""
            <div style="background:rgba(255,159,28,0.07);border:1px solid rgba(255,159,28,0.3);
                        border-radius:10px;padding:12px 16px;margin:8px 0">
              <span style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;
                           color:#ffcc7a">💡 HINT {S.hints_used}:</span>
              <span style="color:#e8f4ff;font-size:0.88rem;margin-left:8px">{S.current_hint}</span>
              <span style="color:#3d6e8a;font-size:0.72rem;margin-left:8px">(XP reduced)</span>
            </div>
            """, unsafe_allow_html=True)

        # ── Handle hint button ──
        if get_hint_btn:
            with st.spinner("🤖 Crafting a hint..."):
                hint_text, hint_err = generate_hint(
                    S.api_key, S.gemini_model,
                    secret["name"], secret["description"],
                    S.hints_used, S.question_log, secret["category"]
                )
            S.current_hint = hint_text
            S.hints_used += 1
            st.rerun()

        # ── Handle guess submission ──
        if submit_guess and guess_text:
            with st.spinner("🤖 Checking your answer..."):
                correct, reason = validate_guess(
                    S.api_key, S.gemini_model, secret["name"], guess_text
                )

            if correct:
                # Calculate XP
                xp_base = DIFFICULTY_CONFIGS[S.difficulty]["xp_base"]
                hint_penalty = S.hints_used * 15
                q_bonus = max(0, (S.questions_left) * 2)
                heart_bonus = S.hearts * 8
                S.xp_earned = max(10, xp_base - hint_penalty + q_bonus + heart_bonus)

                # Update leaderboard
                new_score = S.xp_earned
                S.leaderboard.append({
                    "name": S.player_name,
                    "score": new_score,
                    "games": 1,
                    "rank": 0
                })
                S.leaderboard.sort(key=lambda x: x["score"], reverse=True)
                for i, e in enumerate(S.leaderboard):
                    e["rank"] = i + 1
                S.leaderboard = S.leaderboard[:10]
                for i, e in enumerate(S.leaderboard):
                    if e["name"] == S.player_name and e["score"] == new_score:
                        S.player_rank = i + 1
                        break

                # Generate optimal path if feature on
                opt_data = None
                if S.feature_optimal_path:
                    with st.spinner("⚡ Analyzing optimal strategy..."):
                        opt_data, _ = generate_optimal_path(
                            S.api_key, S.gemini_model,
                            secret["name"], secret["description"],
                            S.question_log
                        )

                S.result_data = {"won": True, "opt_data": opt_data}
                S.game_phase = "result"
                st.rerun()

            else:
                S.hearts -= 1
                S.wrong_guesses += 1

                if S.hearts <= 0:
                    opt_data = None
                    if S.feature_optimal_path:
                        with st.spinner("⚡ Analyzing optimal strategy..."):
                            opt_data, _ = generate_optimal_path(
                                S.api_key, S.gemini_model,
                                secret["name"], secret["description"],
                                S.question_log
                            )
                    S.result_data = {"won": False, "opt_data": opt_data}
                    S.game_phase = "result"
                    st.rerun()
                else:
                    S.error_msg = f"❌ Wrong! '{guess_text}' is not the answer. {S.hearts} {'heart' if S.hearts==1 else 'hearts'} remaining."
                    st.rerun()

        # ── Out of questions check ──
        if S.questions_left <= 0:
            st.warning("⚠️ No questions remaining — make your final guess above!")

    # ══════════════════════════════════════════
    #  PHASE: RESULT
    # ══════════════════════════════════════════
    elif S.game_phase == "result" and S.secret:
        secret = S.secret
        result = S.result_data or {}
        won = result.get("won", False)
        opt_data = result.get("opt_data")

        # Hero
        st.markdown(f"""
        <div style='text-align:center;padding:24px 0 16px'>
          <div style='font-size:4rem;margin-bottom:12px'>{"🎯" if won else "💀"}</div>
          <div style='font-family:"Orbitron",monospace;
                      font-size:clamp(1.2rem,4vw,2rem);font-weight:900;
                      color:{"#00ff88" if won else "#ff3a5c"};
                      text-shadow:0 0 30px {"rgba(0,255,136,0.5)" if won else "rgba(255,58,92,0.5)"};
                      margin-bottom:8px'>
            {"TARGET IDENTIFIED" if won else "MISSION FAILED"}
          </div>
          {"" if not won else f'<div style="color:#7ab5d8;font-size:0.88rem">Solved in {20 - S.questions_left} questions · {S.wrong_guesses} wrong guesses</div>'}
        </div>
        """, unsafe_allow_html=True)

        if won:
            st.markdown(xp_badge_html(S.xp_earned), unsafe_allow_html=True)
            if S.player_rank:
                st.markdown(f"""<div style='text-align:center;margin-bottom:16px'>
                  {badge_html(f"🏆 LEADERBOARD RANK #{S.player_rank}", "green")}
                </div>""", unsafe_allow_html=True)

        # Answer reveal
        st.markdown(f"""
        <div style='background:#061a2e;border:1px solid #00e5ff;border-radius:16px;
                    padding:20px;margin:16px 0;box-shadow:0 0 24px rgba(0,229,255,0.2)'>
          {section_title_html("THE ANSWER WAS")}
          <div style='font-family:"Orbitron",monospace;font-size:clamp(1rem,3vw,1.6rem);
                      color:#00e5ff;margin-bottom:10px'>{secret['name']}</div>
          <div style='color:#7ab5d8;font-size:0.88rem;line-height:1.5'>
            {secret.get('description','')}
          </div>
          {f"<div style='margin-top:12px;color:#4de890;font-size:0.82rem'><strong style='color:#00ff88'>Fun fact:</strong> {secret.get('fun_fact','')}</div>" if S.feature_fun_facts and secret.get('fun_fact') else ""}
        </div>
        """, unsafe_allow_html=True)

        # Optimal path
        if S.feature_optimal_path and opt_data and "optimal_path" in opt_data:
            with st.expander("⚡ OPTIMAL QUESTION PATH", expanded=True):
                st.markdown(f"""
                <div style='font-family:"JetBrains Mono",monospace;font-size:0.72rem;
                             color:#7ab5d8;margin-bottom:14px'>
                  💬 {opt_data.get('strategy_tip', '')}
                </div>
                """, unsafe_allow_html=True)
                for step in opt_data["optimal_path"]:
                    ans = step.get("expected_answer", "")
                    color = "#4de890" if ans == "Yes" else "#ff7a92"
                    st.markdown(f"""
                    <div style='display:flex;align-items:flex-start;gap:12px;
                                padding:10px 0;border-bottom:1px solid #0d3a5c'>
                      <span style='font-family:"Orbitron",monospace;font-size:0.65rem;
                                   background:#0f3460;color:#00e5ff;
                                   width:24px;height:24px;border-radius:50%;
                                   display:flex;align-items:center;justify-content:center;
                                   flex-shrink:0;font-weight:700'>{step['step']}</span>
                      <div style='flex:1'>
                        <div style='color:#e8f4ff;font-size:0.82rem'>{step['question']}</div>
                        <div style='color:#3d6e8a;font-size:0.73rem;margin-top:3px'>{step.get('why','')}</div>
                      </div>
                      <span style='font-family:"Orbitron",monospace;font-size:0.65rem;
                                   color:{color};white-space:nowrap'>{ans}</span>
                    </div>
                    """, unsafe_allow_html=True)

        # Player's question log summary
        with st.expander("📋 YOUR QUESTION LOG"):
            st.markdown(answer_log_html(S.question_log), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        btn_c1, btn_c2, btn_c3 = st.columns(3)
        with btn_c1:
            if st.button("🔄 PLAY AGAIN", use_container_width=True, type="primary"):
                for k in ["game_phase","secret","questions_left","hearts","hints_used",
                          "question_log","asked_set","suggested_questions","current_hint",
                          "wrong_guesses","xp_earned","result_data","player_rank","error_msg"]:
                    if k in st.session_state:
                        del st.session_state[k]
                st.rerun()
        with btn_c2:
            if st.button("⚙️ CHANGE SETTINGS", use_container_width=True):
                S.game_phase = "setup"
                for k in ["secret","questions_left","hearts","hints_used","question_log",
                          "asked_set","suggested_questions","current_hint","wrong_guesses",
                          "xp_earned","result_data","player_rank","error_msg"]:
                    if k in st.session_state:
                        del st.session_state[k]
                st.rerun()


# ═══════════════════════════════════════════════════════════════════════════
#  TAB: LEADERBOARD
# ═══════════════════════════════════════════════════════════════════════════
with tab_leaderboard:

    st.markdown(section_title_html("GLOBAL LEADERBOARD"), unsafe_allow_html=True)

    if not S.leaderboard:
        st.info("No scores yet — play a game to appear here!")
    else:
        lb_html = ""
        for entry in S.leaderboard[:10]:
            is_new = (entry["name"] == S.player_name and
                      S.game_phase == "result" and
                      S.player_rank == entry["rank"])
            lb_html += leaderboard_row_html(
                entry["rank"], entry["name"],
                entry["score"], entry["games"],
                is_new=is_new
            )
        st.markdown(lb_html, unsafe_allow_html=True)

    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(card_html(f"""
        <div style='text-align:center'>
          <div style='font-size:1.6rem'>🏆</div>
          <div style='font-family:"Orbitron",monospace;font-size:0.65rem;
                      color:#3d6e8a;letter-spacing:0.15em;margin:6px 0'>TOP SCORE</div>
          <div style='font-family:"Orbitron",monospace;font-size:1.2rem;color:#00ff88'>
            {S.leaderboard[0]['score']:,}
          </div>
          <div style='font-size:0.8rem;color:#7ab5d8'>{S.leaderboard[0]['name']}</div>
        </div>
        """), unsafe_allow_html=True)
    with col2:
        total_games = sum(e["games"] for e in S.leaderboard)
        st.markdown(card_html(f"""
        <div style='text-align:center'>
          <div style='font-size:1.6rem'>🎮</div>
          <div style='font-family:"Orbitron",monospace;font-size:0.65rem;
                      color:#3d6e8a;letter-spacing:0.15em;margin:6px 0'>TOTAL GAMES</div>
          <div style='font-family:"Orbitron",monospace;font-size:1.2rem;color:#00e5ff'>
            {total_games}
          </div>
        </div>
        """), unsafe_allow_html=True)
    with col3:
        avg_score = int(sum(e["score"] for e in S.leaderboard) / len(S.leaderboard))
        st.markdown(card_html(f"""
        <div style='text-align:center'>
          <div style='font-size:1.6rem'>📊</div>
          <div style='font-family:"Orbitron",monospace;font-size:0.65rem;
                      color:#3d6e8a;letter-spacing:0.15em;margin:6px 0'>AVG SCORE</div>
          <div style='font-family:"Orbitron",monospace;font-size:1.2rem;color:#38a3e8'>
            {avg_score:,}
          </div>
        </div>
        """), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
#  TAB: HOW TO PLAY
# ═══════════════════════════════════════════════════════════════════════════
with tab_howto:

    st.markdown(section_title_html("GAME MANUAL"), unsafe_allow_html=True)

    rules = [
        ("🎯", "Objective",
         "Gemini AI secretly picks a subject from your chosen category. "
         "You have <strong>20 yes/no questions</strong> and <strong>3 final guesses</strong> "
         "to identify it. The more efficiently you solve it, the higher your XP."),
        ("🧠", "Dynamic Questions",
         "When enabled, Gemini generates <strong>context-aware question suggestions</strong> "
         "tailored to what you've already asked and the current difficulty. "
         "You can also type any custom question."),
        ("❤️", "Lives System",
         "You start with <strong>3 hearts</strong>. Each <em>wrong final guess</em> costs "
         "1 heart. Questions never cost hearts. Lose all 3 → Game Over. "
         "Hearts are <em>not</em> spent on questions."),
        ("💡", "Hint System",
         "Up to <strong>3 AI-generated hints</strong> that grow progressively more revealing. "
         "Each hint reduces your XP gain. Hints are contextual — Gemini knows what you've "
         "already asked and gives useful, non-trivial clues."),
        ("⚡", "Optimal Path",
         "After each game, Gemini analyzes your questions and reveals the "
         "<strong>ideal question path</strong> — the most efficient route to the answer — "
         "with explanations for why each question is strategically valuable."),
        ("🏆", "Scoring",
         "XP = base (80/120/200 by difficulty) − hint penalty (15×hints) "
         "+ question efficiency bonus + heart bonus. "
         "Scores are added to the leaderboard after a correct guess."),
        ("⚙️", "Feature Toggles",
         "Use the <strong>sidebar toggles</strong> to enable/disable: "
         "Dynamic Questions, Hints, Optimal Path, Fun Facts, and Custom Category. "
         "Mix and match for your preferred experience."),
        ("🌐", "Any Category",
         "Enable <em>Custom Category</em> in the sidebar and type anything — "
         "<em>Ancient Roman technology, Jazz musicians, Deep sea creatures, "
         "Medieval siege weapons</em> — Gemini will pick something real and guessable."),
    ]

    for icon, title, body in rules:
        st.markdown(f"""
        <div style='display:flex;align-items:flex-start;gap:14px;
                    padding:16px;background:#061a2e;border:1px solid #0d3a5c;
                    border-radius:12px;margin-bottom:10px'>
          <span style='font-size:1.5rem;flex-shrink:0'>{icon}</span>
          <div>
            <div style='font-family:"Orbitron",monospace;font-size:0.72rem;
                        color:#00e5ff;letter-spacing:0.1em;margin-bottom:6px'>
              {title.upper()}
            </div>
            <div style='color:#7ab5d8;font-size:0.86rem;line-height:1.55'>{body}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.markdown(f"""
    <div style='text-align:center;padding:12px'>
      <div style='font-family:"JetBrains Mono",monospace;font-size:0.75rem;
                  color:#3d6e8a;line-height:2'>
        Get a free Gemini API key at
        <span style='color:#00e5ff'>aistudio.google.com</span><br>
        CIPHER v2.0 · Built with Streamlit + Google Gemini
      </div>
    </div>
    """, unsafe_allow_html=True)
