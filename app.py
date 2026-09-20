import streamlit as st
from google import genai

# App ka Title aur Design
st.set_page_config(page_title="Vinaygupta9660 AI", page_icon="🤖")
st.title("🤖 Vinaygupta9660 AI")
st.subheader("Aapka Personal Assistant")

# Yahan double quotes ke andar apni AQ... wali key daalein
API_KEY = "YAHAN_APNI_AQ_WALI_KEY_PASTE_KAREIN"
client = genai.Client(api_key=API_KEY)

# Chat session setup
if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(
        model="gemini-3.6-flash",
        config=genai.types.GenerateContentConfig(
            system_instruction="Tumhara naam 'Vinaygupta9660 AI' hai. Tumhe Vinay ne develop kiya hai aur tum Vinay ke personal assistant ho."
        )
    )
    st.session_state.messages = []

# Purane messages dikhana
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

# Naya message bhejna
if prompt := st.chat_input("Apna sawaal yahan likhein..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "text": prompt})

    with st.chat_message("model"):
        try:
            response = st.session_state.chat_session.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "model", "text": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
