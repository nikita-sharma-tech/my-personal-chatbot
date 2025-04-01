import streamlit as st
import requests
import datetime

# Mistral API key
API_KEY = "lzTHMs9bYEjgtRyVj5EeRmA91xj1GU0y"

# Mistral API URL
API_URL = "https://api.mistral.ai/v1/chat/completions"

# Request headers
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_mistral_response(prompt):
    """Send user input to Mistral AI and return the response."""
    data = {
        "model": "mistral-tiny",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(API_URL, headers=HEADERS, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.json()}"

# Streamlit UI
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 AI Chatbot")
st.markdown("Chat with the AI! Your conversation history is saved by date.")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

# Get current date
current_date = datetime.date.today().strftime("%Y-%m-%d")

# Ensure today's chat history exists
if current_date not in st.session_state.chat_history:
    st.session_state.chat_history[current_date] = []

# Sidebar for history selection
st.sidebar.title("📜 Chat History")
date_keys = list(st.session_state.chat_history.keys())[::-1]
selected_date = st.sidebar.selectbox("Select a date", date_keys, index=0 if date_keys else None)

# User input
user_input = st.text_input("You:", "")
if st.button("Send") and user_input:
    bot_response = get_mistral_response(user_input)
    
    # Store messages
    st.session_state.chat_history[current_date].append(("You", user_input))
    st.session_state.chat_history[current_date].append(("Bot", bot_response))

# Display chat history
st.subheader(f"Chat History - {selected_date}")
for sender, message in st.session_state.chat_history[selected_date]:
    with st.chat_message("user" if sender == "You" else "assistant"):
        st.markdown(f"**{sender}:** {message}")
