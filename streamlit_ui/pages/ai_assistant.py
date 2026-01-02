import streamlit as st
import requests
from utils.api import fetch_data # Assuming you added a 'post_data' helper

st.title("🤖 Travel AI Assistant")
st.caption("Ask me about hotels, food, or places in your selected destination!")

# 1. Check for Destination Context
if 'selected_dest_id' not in st.session_state:
    st.warning("Please select a destination first to give the AI context.")
    st.stop()

dest_name = st.session_state.selected_dest_name
dest_id = st.session_state.selected_dest_id

# 2. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": f"Hi! I'm your assistant for {dest_name}. How can I help you plan your trip?"}
    ]

# 3. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Chat Input
if prompt := st.chat_input("Ask something..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. Call Django Chatbot API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # We send the question AND the destination_id so the AI knows the context
                payload = {
                    "query": prompt,
                    "destination_id": dest_id
                }
                # Update this URL to match your 'dashboard.chatbot.urls'
                response = requests.post("http://127.0.0.1:8000/api/chatbot/", json=payload)
                
                if response.status_code == 200:
                    answer = response.json().get('reply', "I'm sorry, I couldn't process that.")
                    st.markdown(answer)
                    # Add AI response to history
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("Error connecting to Chatbot API.")
            except Exception as e:
                st.error(f"Error: {e}")