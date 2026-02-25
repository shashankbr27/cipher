# 🔐 CIPHER - AI-Powered Cybersecurity Guessing Game

An advanced 20-questions game powered by Google's Gemini 2.5 Flash AI, where players guess cybersecurity concepts through intelligent yes/no questions.

## 🎮 Features

- **AI-Powered Question Evaluation**: Ask any question in natural language, AI intelligently answers
- **Smart Guess Validation**: AI understands synonyms, abbreviations, and variations
- **No Repetition**: Tracks recently used concepts to ensure variety
- **Dynamic Difficulty**: Three levels (Medium, Hard, Expert)
- **Real-time Leaderboard**: Compete with other players
- **Cyberpunk UI**: Sleek, modern interface with neon aesthetics

## 🚀 Quick Deploy (5 Minutes)

### Option 1: Render (Recommended - Free)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Deploy Cipher Game"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Render:**
   - Go to https://render.com
   - Sign up with GitHub (free)
   - Click "New +" → "Web Service"
   - Connect your repository
   - Configure:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `python cipher_game.py`
   - Add Environment Variable:
     - **Key:** `GEMINI_API_KEY`
     - **Value:** Your Gemini API key
   - Click "Create Web Service"

3. **Get Your Link:** `https://cipher-game.onrender.com`

### Option 2: Railway (Fast)

1. Push to GitHub (same as above)
2. Go to https://railway.app
3. Sign up with GitHub
4. Click "New Project" → "Deploy from GitHub repo"
5. Select your repository
6. Add environment variable: `GEMINI_API_KEY`
7. Deploy!

Your link: `https://cipher-game.up.railway.app`

### Option 3: PythonAnywhere (No Git Required)

1. Go to https://www.pythonanywhere.com
2. Sign up (free)
3. Upload `cipher_game.py` and `requirements.txt`
4. Install dependencies: `pip install --user -r requirements.txt`
5. Configure web app in Web tab
6. Your link: `https://yourusername.pythonanywhere.com`

## 🔑 Environment Variables

All hosting platforms need:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your API key from: https://aistudio.google.com/apikey

## 💻 Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable (or hardcode in cipher_game.py)
export GEMINI_API_KEY=your_api_key_here

# Run the game
python cipher_game.py

# Open browser
http://localhost:5000
```

## 🎯 How to Play

1. **Start Game**: Choose difficulty level (Medium, Hard, Expert)
2. **Ask Questions**: Type any yes/no question about the concept
3. **Get AI Answers**: Receive Yes/No/Irrelevant responses
4. **Make Guesses**: Try to identify the concept
5. **Win**: Guess correctly before running out of questions or hearts!

## 📊 Scoring System

- **Base XP**: 100 (no hints), 70 (1 hint), 40 (2+ hints)
- **Question Penalty**: -2 XP per question asked
- **Hearts Bonus**: +10 XP per heart remaining
- **Difficulty Multiplier**: 1.0x (Medium), 1.5x (Hard), 2.0x (Expert)

## 🤖 AI Technology

- **Model**: Google Gemini 2.5 Flash
- **Capabilities**:
  - Natural language understanding
  - Context-aware question evaluation
  - Intelligent guess validation
  - Common sense reasoning
  - Domain-specific cybersecurity knowledge

### AI Features

**Question Evaluation:**
- Understands nuanced questions
- Distinguishes between attacks, tools, and defenses
- Handles synonyms and variations
- Context-aware responses

**Guess Validation:**
- Accepts abbreviations (e.g., "DDoS" = "Distributed Denial of Service")
- Recognizes synonyms (e.g., "Firewall" = "Network Firewall")
- Handles spelling variations
- Domain-specific matching

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **AI**: Google Gemini 2.5 Flash
- **Frontend**: HTML/CSS/JavaScript (embedded)
- **Styling**: Cyberpunk theme with custom CSS
- **Fonts**: Orbitron, Rajdhani, JetBrains Mono

## 📦 Files Structure

```
cipher-game/
├── cipher_game.py          # Main Flask application (self-contained)
├── requirements.txt        # Python dependencies
├── Procfile               # Deployment configuration
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🎨 Game Features

### Variety System
- Tracks last 5 concepts per session
- Avoids immediate repetition
- Automatic reset after all concepts used
- Fresh experience every time

### Leaderboard
- Real-time score tracking
- Top 10 players displayed
- Persistent across sessions
- Clean, no fake data

### Responsive Design
- Works on desktop, tablet, and mobile
- Adaptive layout
- Touch-friendly controls
- Optimized for all screen sizes

## 🔒 Security

- API key stored in environment variables (not in code)
- Input validation
- HTTPS support (automatic on hosting platforms)
- No sensitive data in repository

## 📱 Hosting Comparison

| Platform | Free Tier | Setup Time | Best For |
|----------|-----------|------------|----------|
| **Render** | ✅ Forever | 5 min | Most users |
| **Railway** | $5/month credit | 3 min | Fast deploy |
| **PythonAnywhere** | ✅ Limited | 10 min | No Git needed |
| **Heroku** | ❌ $5/month | 5 min | Enterprise |
| **Vercel** | ✅ Generous | 5 min | Global CDN |

## 🐛 Troubleshooting

**App won't start:**
- Verify `GEMINI_API_KEY` environment variable is set
- Check requirements.txt exists
- Review platform logs

**Slow loading:**
- Free tiers may sleep after 15 min inactivity
- First request takes 30s to wake up
- Subsequent requests are fast

**API errors:**
- Verify API key is correct
- Check Gemini API quota
- Review error logs

## 🎮 Game Modes

- **Static Mode**: Curated cybersecurity concepts (5 per difficulty)
- **AI Mode**: Dynamically generated concepts (unlimited variety)

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📄 License

MIT License - feel free to use and modify!

## 🙏 Credits

- **AI**: Google Gemini 2.5 Flash
- **Fonts**: Orbitron, Rajdhani, JetBrains Mono (Google Fonts)
- **Inspiration**: Classic 20 Questions game

## 📞 Support

Having issues?
1. Check troubleshooting section above
2. Review hosting platform documentation
3. Open a GitHub issue

## 🎉 Have Fun!

Enjoy testing your cybersecurity knowledge with AI-powered intelligence!

---

**Made with ❤️ and 🤖 AI**

**Star ⭐ this repo if you found it useful!**
