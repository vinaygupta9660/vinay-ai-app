import streamlit as st
from google import genai

st.title("🤖 Vinaygupta9660 AI")
st.subheader("Aapka Personal Assistant")

# Yahan double quotes ke andar apni API Key daalein
API_KEY = "YAHAN_APNI_API_KEY_DAALEIN"

if "chat" not in st.session_state:
    client = genai.Client(api_key=API_KEY)
    st.session_state.chat = client.chats.create(
        model="gemini-3.6-flash",
        config={"system_instruction": "Tumhara naam 'Vinaygupta9660 AI' hai. Tumhe Vinay ne develop kiya hai aur tum Vinay ke personal assistant ho."}
    )
    st.session_state.messages = []

# Messages dikhana
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["text"])

# Naya message bhejna
prompt = st.chat_input("Apna sawaal yahan likhein...")
if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "text": prompt})
    
    try:
        response = st.session_state.chat.send_message(prompt)
        st.chat_message("model").write(response.text)
        st.session_state.messages.append({"role": "model", "text": response.text})
    except Exception as e:
        st.error(f"Error: {e}")
