import streamlit as st
import google.generativeai as genai

# ------------------ CONFIG ------------------
genai.configure(api_key="AIzaSyAuUm5vNsdQ1mne38HWZAAl5Kgf4SrLd9c")

model = genai.GenerativeModel('gemini-2.5-flash')
# ------------------ PAGE ------------------
st.set_page_config(page_title="Debate Bot", page_icon="💬")
st.title("💬 AI Debate Bot")

# ------------------ MEMORY ------------------
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------ DISPLAY CHAT ------------------
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ------------------ INPUT ------------------
user_input = st.chat_input("Enter your argument...")

if user_input:
    # show user message
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # -------- GEMINI PROMPT --------
    prompt = f"""
    You are a skilled debate opponent.

    Always take the opposite side of the user's argument.
    Challenge weak reasoning.
    Be logical, clear, and slightly assertive.

    User argument: {user_input}
    """

    # -------- API CALL --------
    response = st.session_state.chat.send_message(prompt)
    bot_reply = response.text

    # show bot reply
    st.chat_message("assistant").write(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})