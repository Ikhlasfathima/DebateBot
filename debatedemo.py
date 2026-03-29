import streamlit as st
import google.generativeai as genai
import os

# ------------------ CONFIG ------------------
genai.configure(api_key=os.getenv("AIzaSyATfrKV2CGCazX4ag-sn2cshPBjqRSPMvc"))
model = genai.GenerativeModel('gemini-2.5-flash')

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="⚔️ Debate Bot",
    page_icon="⚔️",
    layout="centered"
)

# ------------------ SESSION STATE ------------------
defaults = {
    "chat": None,
    "messages": [],
    "personality": None,
    "round": 1,
    "scores": {"user": 0, "bot": 0},
    "game_over": False,
    "dark_mode": True,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if st.session_state.chat is None and st.session_state.personality:
    st.session_state.chat = model.start_chat(history=[])


# ------------------ PERSONALITY DATA ------------------
PERSONALITIES = {
    "Calm 🧘": {
        "label": "Calm",
        "emoji": "🧘",
        "bot_icon": "🌊",
        "user_icon": "🌿",
        "tagline": "Still waters run deep.",
        "description": "Serene, composed, and thoughtful.",
        "dark": {
            "bg": "#0d1b2a",
            "bg2": "#112233",
            "card": "#162840",
            "accent": "#7ecac3",
            "accent2": "#a8dbd6",
            "text": "#d6eef0",
            "subtext": "#89b5bb",
            "border": "#2a4a5a",
            "user_bubble": "#1a3a4a",
            "bot_bubble": "#0f2535",
            "gradient": "linear-gradient(135deg, #0d1b2a 0%, #0a2535 50%, #0d2040 100%)",
            "header_grad": "linear-gradient(90deg, #7ecac3, #4a9fa0)",
            "font_display": "'Playfair Display', serif",
            "font_body": "'Lato', sans-serif",
            "font_mono": "'Courier New', monospace",
            "orb_color": "rgba(126, 202, 195, 0.08)",
        },
        "light": {
            "bg": "#e8f4f3",
            "bg2": "#d5ecea",
            "card": "#ffffff",
            "accent": "#2a8a85",
            "accent2": "#1e6e6a",
            "text": "#1a3a3a",
            "subtext": "#4a7a7a",
            "border": "#b0d8d5",
            "user_bubble": "#c5e8e5",
            "bot_bubble": "#f0f9f8",
            "gradient": "linear-gradient(135deg, #e8f4f3 0%, #d5ecea 50%, #c8e8e5 100%)",
            "header_grad": "linear-gradient(90deg, #2a8a85, #1e6e6a)",
            "font_display": "'Playfair Display', serif",
            "font_body": "'Lato', sans-serif",
            "font_mono": "'Courier New', monospace",
            "orb_color": "rgba(42, 138, 133, 0.06)",
        },
        "effects": "waves",
    },
    "Aggressive 🔥": {
        "label": "Aggressive",
        "emoji": "🔥",
        "bot_icon": "🐉",
        "user_icon": "⚡",
        "tagline": "Crush. Dominate. Annihilate.",
        "description": "Intense, relentless, and fierce.",
        "dark": {
            "bg": "#0f0a0a",
            "bg2": "#1a0c0c",
            "card": "#220e0e",
            "accent": "#ff4444",
            "accent2": "#ff7700",
            "text": "#ffe0d0",
            "subtext": "#cc7755",
            "border": "#4a1515",
            "user_bubble": "#2a1010",
            "bot_bubble": "#1a0808",
            "gradient": "linear-gradient(135deg, #0f0a0a 0%, #1c0a08 50%, #220c08 100%)",
            "header_grad": "linear-gradient(90deg, #ff4444, #ff7700)",
            "font_display": "'Black Han Sans', 'Bebas Neue', sans-serif",
            "font_body": "'Rajdhani', sans-serif",
            "font_mono": "'Share Tech Mono', monospace",
            "orb_color": "rgba(255, 68, 68, 0.10)",
        },
        "light": {
            "bg": "#fff0ec",
            "bg2": "#ffe0d8",
            "card": "#ffffff",
            "accent": "#cc2200",
            "accent2": "#e05500",
            "text": "#2a0a00",
            "subtext": "#8a3322",
            "border": "#f0b0a0",
            "user_bubble": "#ffd5cc",
            "bot_bubble": "#fff5f2",
            "gradient": "linear-gradient(135deg, #fff0ec 0%, #ffe0d8 50%, #ffd5cc 100%)",
            "header_grad": "linear-gradient(90deg, #cc2200, #e05500)",
            "font_display": "'Black Han Sans', 'Bebas Neue', sans-serif",
            "font_body": "'Rajdhani', sans-serif",
            "font_mono": "'Share Tech Mono', monospace",
            "orb_color": "rgba(204, 34, 0, 0.06)",
        },
        "effects": "sparks",
    },
    "Sarcastic 😏": {
        "label": "Sarcastic",
        "emoji": "😏",
        "bot_icon": "🎭",
        "user_icon": "🃏",
        "tagline": "Oh sure, that's *brilliant*.",
        "description": "Witty, sharp, and deliciously smug.",
        "dark": {
            "bg": "#100d1a",
            "bg2": "#150f22",
            "card": "#1e1530",
            "accent": "#c084fc",
            "accent2": "#e879f9",
            "text": "#ecdff8",
            "subtext": "#9d7abf",
            "border": "#3a2460",
            "user_bubble": "#221840",
            "bot_bubble": "#160f30",
            "gradient": "linear-gradient(135deg, #100d1a 0%, #180f2a 50%, #1a0f28 100%)",
            "header_grad": "linear-gradient(90deg, #c084fc, #e879f9)",
            "font_display": "'Abril Fatface', cursive",
            "font_body": "'DM Sans', sans-serif",
            "font_mono": "'Fira Code', monospace",
            "orb_color": "rgba(192, 132, 252, 0.09)",
        },
        "light": {
            "bg": "#f5f0ff",
            "bg2": "#ede5ff",
            "card": "#ffffff",
            "accent": "#7c3aed",
            "accent2": "#9333ea",
            "text": "#1a0a2e",
            "subtext": "#6b3fa0",
            "border": "#d8c0f8",
            "user_bubble": "#e8d5ff",
            "bot_bubble": "#faf5ff",
            "gradient": "linear-gradient(135deg, #f5f0ff 0%, #ede5ff 50%, #e8d8ff 100%)",
            "header_grad": "linear-gradient(90deg, #7c3aed, #9333ea)",
            "font_display": "'Abril Fatface', cursive",
            "font_body": "'DM Sans', sans-serif",
            "font_mono": "'Fira Code', monospace",
            "orb_color": "rgba(124, 58, 237, 0.05)",
        },
        "effects": "stars",
    },
    "Logical 🧠": {
        "label": "Logical",
        "emoji": "🧠",
        "bot_icon": "🤖",
        "user_icon": "💡",
        "tagline": "Logic is the ultimate weapon.",
        "description": "Calculated, precise, and merciless.",
        "dark": {
            "bg": "#080e1a",
            "bg2": "#0a1220",
            "card": "#0e1a2e",
            "accent": "#38bdf8",
            "accent2": "#06b6d4",
            "text": "#cce8f8",
            "subtext": "#5a9abb",
            "border": "#1a3050",
            "user_bubble": "#0f1e35",
            "bot_bubble": "#080e1e",
            "gradient": "linear-gradient(135deg, #080e1a 0%, #0c1525 50%, #0a1830 100%)",
            "header_grad": "linear-gradient(90deg, #38bdf8, #06b6d4)",
            "font_display": "'Orbitron', sans-serif",
            "font_body": "'IBM Plex Mono', monospace",
            "font_mono": "'IBM Plex Mono', monospace",
            "orb_color": "rgba(56, 189, 248, 0.08)",
        },
        "light": {
            "bg": "#f0f7ff",
            "bg2": "#e0f0ff",
            "card": "#ffffff",
            "accent": "#0369a1",
            "accent2": "#0284c7",
            "text": "#0a1a2a",
            "subtext": "#2a6080",
            "border": "#a0cce8",
            "user_bubble": "#cce5f8",
            "bot_bubble": "#f0f8ff",
            "gradient": "linear-gradient(135deg, #f0f7ff 0%, #e0f0ff 50%, #d5ecff 100%)",
            "header_grad": "linear-gradient(90deg, #0369a1, #0284c7)",
            "font_display": "'Orbitron', sans-serif",
            "font_body": "'IBM Plex Mono', monospace",
            "font_mono": "'IBM Plex Mono', monospace",
            "orb_color": "rgba(3, 105, 161, 0.05)",
        },
        "effects": "grid",
    },
}

PERSONALITY_STYLE_PROMPTS = {
    "Calm 🧘": "Be calm, respectful, compassionate, and composed. Speak gently.",
    "Aggressive 🔥": "Be intense, dominating, confrontational, and critical. Show no mercy.",
    "Sarcastic 😏": "Be sarcastic, witty, condescending, and sharply ironic.",
    "Logical 🧠": "Be strictly logical, analytical, and fact-based. No emotion whatsoever.",
}


# ------------------ THEME RESOLVER ------------------
def get_theme():
    p = st.session_state.personality or "Calm 🧘"
    mode = "dark" if st.session_state.dark_mode else "light"
    return PERSONALITIES[p][mode], PERSONALITIES[p]


# ------------------ INJECT CSS ------------------
def inject_css(t, meta):
    google_fonts = "@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Abril+Fatface&family=Orbitron:wght@400;700;900&family=IBM+Plex+Mono:wght@400;500&family=Rajdhani:wght@400;600;700&family=DM+Sans:wght@300;400;600&family=Lato:wght@300;400;700&display=swap');"

    st.markdown(f"""
<style>
{google_fonts}

html, body, [class*="css"] {{
    font-family: {t['font_body']};
    background-color: {t['bg']} !important;
    color: {t['text']} !important;
}}

.stApp {{
    background: {t['gradient']} !important;
    min-height: 100vh;
}}

/* Orb background effects */
.stApp::before {{
    content: '';
    position: fixed;
    width: 600px;
    height: 600px;
    border-radius: 50%;
    background: {t['orb_color']};
    top: -150px;
    right: -150px;
    filter: blur(80px);
    pointer-events: none;
    z-index: 0;
}}

.stApp::after {{
    content: '';
    position: fixed;
    width: 400px;
    height: 400px;
    border-radius: 50%;
    background: {t['orb_color']};
    bottom: -100px;
    left: -100px;
    filter: blur(60px);
    pointer-events: none;
    z-index: 0;
}}

/* Main content */
.block-container {{
    padding: 1.5rem 2rem !important;
    max-width: 820px !important;
}}

/* Title */
h1 {{
    font-family: {t['font_display']} !important;
    background: {t['header_grad']};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2.8rem !important;
    letter-spacing: 2px;
    margin-bottom: 0 !important;
}}

h2, h3 {{
    font-family: {t['font_display']} !important;
    color: {t['accent']} !important;
}}

/* Toggle button */
.toggle-bar {{
    display: flex;
    justify-content: flex-end;
    margin-bottom: 0.5rem;
}}

/* Scoreboard card */
.score-card {{
    background: {t['card']};
    border: 1px solid {t['border']};
    border-radius: 16px;
    padding: 1rem 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 1rem 0;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 24px rgba(0,0,0,0.15);
}}

.score-item {{
    text-align: center;
    flex: 1;
}}

.score-number {{
    font-family: {t['font_display']};
    font-size: 2.2rem;
    color: {t['accent']};
    line-height: 1;
}}

.score-label {{
    font-size: 0.75rem;
    color: {t['subtext']};
    letter-spacing: 1px;
    text-transform: uppercase;
}}

.score-vs {{
    font-family: {t['font_display']};
    font-size: 1.4rem;
    color: {t['subtext']};
    padding: 0 1rem;
}}

/* Round badge */
.round-badge {{
    background: {t['accent']};
    color: {t['bg']};
    border-radius: 999px;
    padding: 0.2rem 1rem;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 1px;
    display: inline-block;
    margin: 0.3rem 0;
}}

/* Chat bubbles */
.chat-bubble-user {{
    background: {t['user_bubble']};
    border: 1px solid {t['border']};
    border-radius: 18px 18px 4px 18px;
    padding: 0.8rem 1.1rem;
    margin: 0.6rem 0 0.6rem 2rem;
    position: relative;
    box-shadow: 0 2px 12px rgba(0,0,0,0.12);
}}

.chat-bubble-bot {{
    background: {t['bot_bubble']};
    border: 1px solid {t['border']};
    border-radius: 18px 18px 18px 4px;
    padding: 0.8rem 1.1rem;
    margin: 0.6rem 2rem 0.6rem 0;
    position: relative;
    box-shadow: 0 2px 12px rgba(0,0,0,0.12);
}}

.bubble-header {{
    font-size: 0.72rem;
    color: {t['subtext']};
    letter-spacing: 0.5px;
    margin-bottom: 0.3rem;
    text-transform: uppercase;
    font-weight: 600;
}}

.bubble-icon {{
    font-size: 1.5rem;
    margin-right: 0.4rem;
}}

.bubble-text {{
    color: {t['text']};
    font-family: {t['font_body']};
    line-height: 1.6;
}}

/* Personality card on selection screen */
.personality-card {{
    background: {t['card']};
    border: 2px solid {t['border']};
    border-radius: 20px;
    padding: 1.5rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}}

.personality-card:hover {{
    border-color: {t['accent']};
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.2);
}}

.personality-card.selected {{
    border-color: {t['accent']};
    background: linear-gradient(135deg, {t['card']}, {t['bg2']});
}}

.char-emoji {{
    font-size: 3.5rem;
    display: block;
    margin-bottom: 0.5rem;
    filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
}}

.char-name {{
    font-family: {t['font_display']};
    font-size: 1.3rem;
    color: {t['accent']};
    margin-bottom: 0.2rem;
}}

.char-tagline {{
    font-size: 0.8rem;
    color: {t['subtext']};
    font-style: italic;
}}

.char-desc {{
    font-size: 0.75rem;
    color: {t['subtext']};
    margin-top: 0.5rem;
}}

/* Streamlit buttons */
.stButton > button {{
    background: {t['header_grad']} !important;
    color: {t['bg']} !important;
    border: none !important;
    border-radius: 999px !important;
    font-family: {t['font_display']} !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    padding: 0.6rem 2rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
}}

.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0,0,0,0.3) !important;
    opacity: 0.9 !important;
}}

/* Selectbox */
.stSelectbox > div > div {{
    background: {t['card']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 12px !important;
    color: {t['text']} !important;
}}

/* Chat input */
.stChatInput textarea, .stChatInput input {{
    background: {t['card']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 16px !important;
    color: {t['text']} !important;
    font-family: {t['font_body']} !important;
}}

.stChatInput {{
    border-radius: 16px !important;
}}

/* Success / error */
.stSuccess {{
    background: rgba(126, 202, 195, 0.15) !important;
    border-color: {t['accent']} !important;
    border-radius: 12px !important;
}}

/* Feedback section */
.feedback-card {{
    background: {t['card']};
    border: 1px solid {t['border']};
    border-radius: 16px;
    padding: 1.5rem;
    margin-top: 1rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}}

/* Divider */
hr {{
    border-color: {t['border']} !important;
    margin: 1rem 0 !important;
}}

/* Caption / subtext */
.stCaption, small, .element-container p small {{
    color: {t['subtext']} !important;
    font-family: {t['font_body']} !important;
}}

/* Expanders */
.streamlit-expanderHeader {{
    background: {t['card']} !important;
    border-radius: 12px !important;
    color: {t['text']} !important;
    font-family: {t['font_display']} !important;
}}

/* Intro hero section */
.hero-section {{
    text-align: center;
    padding: 2rem 0 1rem;
}}

.hero-tagline {{
    font-family: {t['font_display']};
    color: {t['subtext']};
    font-size: 1.1rem;
    font-style: italic;
    margin: 0.5rem 0 2rem;
}}

/* Personality badge in header */
.personality-badge {{
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: {t['card']};
    border: 1px solid {t['border']};
    border-radius: 999px;
    padding: 0.25rem 0.9rem;
    font-size: 0.8rem;
    color: {t['subtext']};
    margin-bottom: 0.5rem;
}}

/* Scrollable chat area */
.chat-container {{
    max-height: 480px;
    overflow-y: auto;
    padding: 0.5rem;
    scrollbar-width: thin;
    scrollbar-color: {t['border']} transparent;
}}

/* Hide Streamlit branding */
#MainMenu, footer, header {{
    visibility: hidden;
}}

/* Progress bar */
.stProgress > div > div {{
    background: {t['header_grad']} !important;
}}

</style>
""", unsafe_allow_html=True)


# ------------------ PERSONALITY SELECTION SCREEN ------------------
def show_personality_select(t, meta):
    st.markdown(f"""
    <div class="hero-section">
        <h1>⚔️ Debate Bot</h1>
        <p class="hero-tagline">Choose your opponent. Face the challenge. Win the argument.</p>
    </div>
    """, unsafe_allow_html=True)

    selected = st.session_state.get("selected_personality", None)

    cols = st.columns(2)
    personality_keys = list(PERSONALITIES.keys())

    for i, key in enumerate(personality_keys):
        p_meta = PERSONALITIES[key]
        mode = "dark" if st.session_state.dark_mode else "light"
        p_theme = p_meta[mode]
        selected_class = "selected" if selected == key else ""

        with cols[i % 2]:
            st.markdown(f"""
            <div class="personality-card {selected_class}" onclick="">
                <span class="char-emoji">{p_meta['bot_icon']}</span>
                <div class="char-name">{p_meta['label']}</div>
                <div class="char-tagline">"{p_meta['tagline']}"</div>
                <div class="char-desc">{p_meta['description']}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Choose {p_meta['label']}", key=f"btn_{key}"):
                st.session_state.selected_personality = key

    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.get("selected_personality"):
        chosen = st.session_state.selected_personality
        p_meta = PERSONALITIES[chosen]
        st.markdown(f"""
        <div style="text-align:center; padding:1rem; background:{t['card']}; border:1px solid {t['border']};
                    border-radius:16px; margin:0.5rem 0;">
            <span style="font-size:2rem;">{p_meta['bot_icon']}</span>
            <div style="font-family:{t['font_display']}; color:{t['accent']}; font-size:1.2rem; margin:0.3rem 0;">
                {p_meta['label']} selected
            </div>
            <div style="color:{t['subtext']}; font-size:0.85rem;">{p_meta['tagline']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("⚔️ Start Debate!", use_container_width=True):
                st.session_state.personality = chosen
                st.session_state.chat = model.start_chat(history=[])
                st.rerun()


# ------------------ RENDER CHAT MESSAGES ------------------
def render_messages(t, meta):
    user_icon = meta["user_icon"]
    bot_icon = meta["bot_icon"]

    chat_html = ""
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            chat_html += f"""
            <div class="chat-bubble-user">
                <div class="bubble-header"><span class="bubble-icon">{user_icon}</span> You</div>
                <div class="bubble-text">{msg['content']}</div>
            </div>"""
        else:
            chat_html += f"""
            <div class="chat-bubble-bot">
                <div class="bubble-header"><span class="bubble-icon">{bot_icon}</span> {meta['label']}</div>
                <div class="bubble-text">{msg['content']}</div>
            </div>"""

    if chat_html:
        st.markdown(f'<div class="chat-container">{chat_html}</div>', unsafe_allow_html=True)


# ------------------ SCOREBOARD ------------------
def render_scoreboard(t, meta):
    user_icon = meta["user_icon"]
    bot_icon = meta["bot_icon"]
    user_score = st.session_state.scores["user"]
    bot_score = st.session_state.scores["bot"]
    round_num = st.session_state.round
    progress = min((round_num - 1) / 5, 1.0)

    st.markdown(f"""
    <div class="score-card">
        <div class="score-item">
            <div style="font-size:1.8rem;">{user_icon}</div>
            <div class="score-number">{user_score}</div>
            <div class="score-label">You</div>
        </div>
        <div class="score-vs">VS</div>
        <div class="score-item">
            <div style="font-size:1.8rem;">{bot_icon}</div>
            <div class="score-number">{bot_score}</div>
            <div class="score-label">{meta['label']}</div>
        </div>
    </div>
    <div style="text-align:center; margin-bottom:0.5rem;">
        <span class="round-badge">ROUND {min(round_num, 5)} / 5</span>
    </div>
    """, unsafe_allow_html=True)

    st.progress(progress)


# ------------------ DARK MODE TOGGLE ------------------
def render_toggle():
    icon = "🌙 Dark" if st.session_state.dark_mode else "☀️ Light"
    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button(icon, key="toggle_mode"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()


# ------------------ MAIN APP ------------------

# Always resolve theme first
if st.session_state.personality:
    t, meta = get_theme()
else:
    # Use calm dark as default for selection screen
    t = PERSONALITIES["Calm 🧘"]["dark" if st.session_state.dark_mode else "light"]
    meta = PERSONALITIES["Calm 🧘"]

inject_css(t, meta)

# Toggle
render_toggle()

# ---- PERSONALITY SELECTION ----
if st.session_state.personality is None:
    show_personality_select(t, meta)
    st.stop()

# ---- RE-RESOLVE THEME after personality set ----
t, meta = get_theme()

# ---- GAME OVER SCREEN ----
if st.session_state.game_over:
    st.markdown(f"""
    <div class="hero-section">
        <h1>🏁 Debate Over!</h1>
    </div>
    """, unsafe_allow_html=True)

    render_scoreboard(t, meta)

    user_s = st.session_state.scores["user"]
    bot_s = st.session_state.scores["bot"]

    if user_s > bot_s:
        st.success(f"🎉 You win {user_s}–{bot_s}! Outstanding!")
    elif bot_s > user_s:
        st.error(f"💀 {meta['label']} wins {bot_s}–{user_s}. Better luck next time!")
    else:
        st.info(f"🤝 It's a tie {user_s}–{bot_s}! Well played both.")

    render_messages(t, meta)

    full_debate = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
    feedback_prompt = f"""
Analyze this user's debate performance against a {meta['label']} opponent.

Debate:
{full_debate}

Give concise, actionable feedback:
1. 2 weak points in the user's arguments
2. 1-2 logical mistakes
3. 3 specific tips to improve debate skills

Keep it sharp, helpful, and under 200 words.
"""
    with st.spinner("Analyzing your performance..."):
        feedback = model.generate_content(feedback_prompt).text

    st.markdown(f"""
    <div class="feedback-card">
        <h3>📊 Performance Analysis</h3>
        <p style="color:{t['text']}; line-height:1.7;">{feedback}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Play Again", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    st.stop()

# ---- ACTIVE GAME SCREEN ----
# Header
st.markdown(f"""
<div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:0.2rem;">
    <span style="font-size:2.5rem; filter:drop-shadow(0 4px 8px rgba(0,0,0,0.4));">{meta['bot_icon']}</span>
    <div>
        <h1 style="margin:0;">⚔️ Debate Bot</h1>
        <span class="personality-badge">{meta['emoji']} {meta['label']} Mode — {meta['tagline']}</span>
    </div>
</div>
""", unsafe_allow_html=True)

render_scoreboard(t, meta)

st.markdown("<hr>", unsafe_allow_html=True)

render_messages(t, meta)

# ---- CHAT INPUT ----
user_input = st.chat_input(f"Make your argument against {meta['label']}...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    style = PERSONALITY_STYLE_PROMPTS[st.session_state.personality]

    prompt = f"""You are a debate opponent with this style: {style}

Rules:
- Always counter the user's argument
- Stay strictly under 90 words
- Stay fully in character at all times
- Be sharp and direct

User's argument: {user_input}
"""

    response = st.session_state.chat.send_message(prompt)
    bot_reply = response.text
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    judge_prompt = f"""
User argument: {user_input}
Bot argument: {bot_reply}

Which argument is stronger and more convincing?
Reply with ONLY one word: user OR bot
"""
    judge = model.generate_content(judge_prompt).text.strip().lower()

    if "user" in judge:
        st.session_state.scores["user"] += 1
    else:
        st.session_state.scores["bot"] += 1

    st.session_state.round += 1

    if st.session_state.round > 5:
        st.session_state.game_over = True

    st.rerun()