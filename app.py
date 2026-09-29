import os
import time
import base64
import streamlit as st
from google import genai
from google.genai import types

# 1. Page Configuration
st.set_page_config(
    page_title="Vinay AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# Logo detect logic
logo_path = None
for name in ["logo.png.jpg", "logo.png", "logo.jpg", "logo.jpeg"]:
    if os.path.exists(name):
        logo_path = name
        break

# Convert logo to base64
def get_base64_image(image_path):
    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

logo_b64 = get_base64_image(logo_path)

# Custom Styling
st.markdown("""
<style>
    .top-nav {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 0px 16px 0px;
        border-bottom: 1px solid rgba(128, 128, 128, 0.15);
        margin-bottom: 25px;
    }
    .top-nav img {
        width: 36px;
        height: 36px;
        border-radius: 8px;
    }
    .top-nav-title {
        font-size: 1.15rem;
        font-weight: 700;
        margin: 0;
    }
    .hero-container {
        text-align: center;
        margin-top: 35px;
        margin-bottom: 30px;
    }
    .hero-logo {
        width: 76px;
        height: 76px;
        border-radius: 18px;
        margin-bottom: 15px;
    }
    .hero-title {
        font-size: 1.85rem;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .hero-sub {
        color: #71767b;
        font-size: 0.95rem;
    }
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 20px;
    }
    .sidebar-brand img {
        width: 32px;
        height: 32px;
        border-radius: 8px;
    }
    .sidebar-brand span {
        font-weight: 600;
        font-size: 1.05rem;
    }
</style>
""", unsafe_allow_html=True)

# 2. API Key Setup
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("API Key नहीं मिली! कृपया `.streamlit/secrets.toml` में GEMINI_API_KEY सेट करें।")
    st.stop()

client = genai.Client(api_key=api_key)

# 3. Session State for Chat Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Sidebar
with st.sidebar:
    if logo_b64:
        st.markdown(f"""
        <div class="sidebar-brand">
            <img src="data:image/jpeg;base64,{logo_b64}">
            <span>Vinay AI</span>
        </div>
        """, unsafe_allow_html=True)
    st.subheader("⚙️ Settings")
    if st.button("🗑️ Clear Chat History", key="clear_chat_sidebar_btn", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 5. Top Bar
if logo_b64:
    st.markdown(f"""
    <div class="top-nav">
        <img src="data:image/jpeg;base64,{logo_b64}">
        <span class="top-nav-title">Vinay AI</span>
    </div>
    """, unsafe_allow_html=True)

# 6. Hero Screen
if len(st.session_state.messages) == 0:
    logo_img_tag = f'<img class="hero-logo" src="data:image/jpeg;base64,{logo_b64}">' if logo_b64 else '🤖'
    st.markdown(f"""
    <div class="hero-container">
        {logo_img_tag}
        <div class="hero-title">आज मैं आपकी क्या मदद कर सकता हूँ?</div>
        <p class="hero-sub">आपका पर्सनल AI असिस्टेंट</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("💡 Business Idea बताओ", key="btn_starter_biz", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "एक नया और अच्छा business idea बताओ"})
            st.rerun()
    with col_b:
        if st.button("🐍 Python Script लिखो", key="btn_starter_py", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "Python में एक useful automation script लिखो"})
            st.rerun()

# 7. Avatar Setup
assistant_avatar = logo_path if logo_path else "🤖"

# 8. Render All Previous History
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else assistant_avatar
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# 9. Handle New Input (Defining need_reply)
user_input = st.chat_input("मुझसे कुछ भी पूछें...")
need_reply = False

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    need_reply = True
elif len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
    need_reply = True

# 10. Generate AI Response
if need_reply:
    chat_contents = []
    for m in st.session_state.messages:
        role = "user" if m["role"] == "user" else "model"
        chat_contents.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=m["content"])]
            )
        )

    with st.chat_message("assistant", avatar=assistant_avatar):
        with st.spinner("सोच रहा हूँ..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=chat_contents,
                    config=types.GenerateContentConfig(
                        system_instruction="You are Vinay AI, an intelligent, helpful, and polite assistant. Reply clearly in the user's language."
                    )
                )
                assistant_reply = response.text
                st.markdown(assistant_reply)
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
            except Exception as err:
                st.error(f"Request Error: {err}")
