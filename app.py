import streamlit as st
import google.generativeai as genai

# App ka Title aur Design
st.set_page_config(page_title="Vinaygupta9660 AI", page_icon="🤖")
st.title("🤖 Vinaygupta9660 AI")
st.subheader("Aapka Personal Assistant")

# API aur AI Setup
API_KEY = "AQ.Ab8RN6LvE2S87Ym6nVDk-gBtq2Mcfn8KlFvrKKQkTitbn27WLQ" 
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    'gemini-3.6-flash',
    system_instruction="Tumhara naam 'Vinaygupta9660 AI' hai. Tum Google ya Gemini nahi ho. Tumhe Vinay ne develop kiya hai aur tum Vinay ke personal assistant ho. Jab bhi koi tumhara naam pooche, toh yahi batana."
)

# Chat History save rakhne ka code (Memory)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani baatein screen par dikhana
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Box jahan aap type karenge
sawal = st.chat_input("Apna sawaal yahan likhein...")

if sawal:
    # Aapka sawaal screen par dikhana
    with st.chat_message("user"):
        st.markdown(sawal)
    st.session_state.messages.append({"role": "user", "content": sawal})
    
    # AI se jawab mangna
    try:
        jawab = model.generate_content(sawal)
        with st.chat_message("assistant"):
            st.markdown(jawab.text)
        st.session_state.messages.append({"role": "assistant", "content": jawab.text})
    except Exception as e:
        st.error("Kuch gadbad hui: " + str(e))
