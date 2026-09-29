import streamlit as st
from google import genai
from PIL import Image
import os

# Page setup
st.set_page_config(page_title="विनय का AI", page_icon="🤖")
ai_name = "vinay9660"
st.title(f"🤖 {ai_name} - आपका अपना AI")
st.write("नमस्ते! मैं आपका नया AI असिस्टेंट हूँ।")

# API Key aur GenAI client setup
try:
    my_api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=my_api_key)
except Exception as e:
    st.error(f"असली एरर यह है: {e}")
    st.stop()

# 1. Chat History ke liye Memory banana
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purane messages ko screen par dikhana
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 2. Sidebar me Image Upload ka feature
with st.sidebar:
    st.header("⚙️ Extra Features")
    st.write("Yahan aap photo upload karke AI se uske baare me pooch sakte hain.")
    uploaded_image = st.file_uploader("Photo upload karein (Optional)", type=["png", "jpg", "jpeg"])
    
    image = None
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Aapki Upload ki gayi photo", use_container_width=True)

# 3. Chat Input aur AI Response
user_input = st.chat_input("Apna sawaal yahan likhein:")

if user_input:
    # User ka message screen par dikhana aur memory me save karna
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # AI se response lena
    try:
        with st.spinner("Soch raha hoon..."):
            # Agar image upload hui hai, toh text aur image dono AI ko bhejein
            if image:
                contents = [user_input, image]
            else:
                contents = [user_input]

# System Prompt
system_prompt = f"तुम्हारा नाम {ai_name} है। तुम्हें विनय ने बनाया है। अगर कोई भी तुमसे पूछे कि तुम्हें किसने बनाया है या तुम किसके AI हो, तो तुम्हें साफ-साफ बताना है कि 'मुझे विनय ने बनाया है'।"

user_question = st.text_input("अपना सवाल यहाँ लिखें:")

if st.button("जवाब खोजें 🚀"):
    if user_question:
        with st.spinner("सोच रहा हूँ..."):
            try:
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=user_question,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                    )
                )
                
                st.success("जवाब:")
                st.write(response.text)
            except Exception as e:
                st.error(f"AI का एरर: {e}")
    else:
        st.warning("कृपया पहले कोई सवाल टाइप करें!")
        