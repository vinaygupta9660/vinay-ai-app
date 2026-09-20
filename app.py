import streamlit as st
from google import genai

st.set_page_config(page_title="Vinaygupta9660 AI", page_icon="🤖")
st.title("🤖 Vinaygupta9660 AI")
st.subheader("Aapka Personal Assistant")

# Yahan double quotes ke andar apni API Key daalein
API_KEY = "YAHAN_APNI_API_KEY_DAALEIN"

# Memory ka naya naam (my_ai_client) use kiya hai taaki purana kachra delete ho jaye
if "my_ai_client" not in st.session_state:
    st.session_state.my_ai_client = genai.Client(api_key=API_KEY)
    st.session_state.my_ai_chat = st.session_state.my_ai_client.chats.create(
        model="gemini-1.5-flash",
        config={"system_instruction": "Tumhara naam 'Vinaygupta9660 AI' hai. Tumhe Vinay ne develop kiya hai aur tum Vinay ke personal assistant ho."}
    )
    st.session_state.my_ai_msgs = []

# Messages dikhana
for msg in st.session_state.my_ai_msgs:
    st.chat_message(msg["role"]).write(msg["text"])

# Naya message bhejna
prompt = st.chat_input("Apna sawaal yahan likhein...")
if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.my_ai_msgs.append({"role": "user", "text": prompt})
    
    try:
        response = st.session_state.my_ai_chat.send_message(prompt)
        st.chat_message("model").write(response.text)
        st.session_state.my_ai_msgs.append({"role": "model", "text": response.text})
    except Exception as e:
        st.error(f"Error: {e}")
