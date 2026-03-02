# 🔐 CIPHER — Advanced 20 Questions (Gemini Edition)

> A fully dynamic, AI-powered 20 Questions game where **Google Gemini** picks the secret, answers your questions, generates strategic hints, and reveals the optimal path to victory.

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install streamlit requests
```

### 2. Get a Gemini API Key
- Visit **https://aistudio.google.com**
- Sign in → Get API key → Copy it

### 3. Run the game
```bash
streamlit run app.py
```

### 4. Enter your API key in the sidebar and play!

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 **Fully Dynamic** | Gemini picks ANY subject from ANY category — no static list |
| 🔄 **AI Question Suggestions** | Context-aware questions generated live based on your progress |
| ✏️ **Custom Questions** | Ask anything in your own words |
| 💡 **Smart Hints** | 3-tier AI hints that grow more specific without spoiling |
| ⚡ **Optimal Path Analysis** | Post-game strategic breakdown of the best question sequence |
| 🌐 **Any Category** | From Cybersecurity to Jazz Musicians to Ancient Roman weapons |
| 🏆 **Leaderboard** | Score based on efficiency, hints used, hearts remaining |
| ⚙️ **Feature Toggles** | Enable/disable each feature independently |
| 🤖 **Multi-model** | Works with Gemini 1.5 Flash, 1.5 Pro, 2.0 Flash |

---

## 🎮 How to Play

1. **Set difficulty**: Medium / Hard / Expert
2. **Choose category**: 12 preset options or type any custom category
3. **Gemini picks a secret** subject in that category
4. **Ask yes/no questions** using AI suggestions or your own
5. **Use hints** if stuck (costs XP)
6. **Submit your guess** — 3 wrong guesses = Game Over
7. **View results**: See the answer, fun fact, and optimal question path

---

## 🧮 Scoring

```
XP = base_score
   - (hints_used × 15)
   + (questions_remaining × 2)
   + (hearts_remaining × 8)
```

| Difficulty | Base XP |
|---|---|
| Medium | 80 |
| Hard | 120 |
| Expert | 200 |

---

## 🏗️ Architecture

```
app.py                   # Single-file Streamlit app
│
├── Gemini REST calls     # Direct API via requests (no SDK needed)
│   ├── pick_secret()     # Gemini picks the hidden subject
│   ├── answer_question() # Gemini answers yes/no strictly
│   ├── generate_question_suggestions()  # Strategic Qs
│   ├── validate_guess()  # Flexible answer matching
│   ├── generate_hint()   # Contextual progressive hints
│   └── generate_optimal_path()  # Post-game analysis
│
├── Session State         # Full game state in st.session_state
├── Custom CSS            # Cyberpunk blue/green aesthetic
└── Feature Toggles       # Sidebar controls for all features
```

---

## ⚙️ Supported Gemini Models

- `gemini-1.5-flash` — Fast, free tier, great for casual play
- `gemini-1.5-pro` — More accurate, better for Expert difficulty
- `gemini-2.0-flash` — Latest fast model
- `gemini-2.0-flash-exp` — Experimental, cutting edge

---

## 💡 Tips

- On **Expert** difficulty, start with broad domain questions (physical? digital? human-created?)
- Use **custom questions** when you have a specific hypothesis to test
- **Refresh suggestions** after asking 4-5 questions — new context = better questions
- The **optimal path** after the game is the best teacher for next time
