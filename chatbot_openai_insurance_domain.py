import openai
import streamlit as st
import time
import os

# -------------------------------
# ✅ Function to stream text like ChatGPT
# -------------------------------
def stream_data(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.03)

# -------------------------------
# ✅ Function to test API key
# -------------------------------
def test_api_key(api_key):
    try:
        client = openai.Client(api_key=api_key)
        client.chat.completions.create(
            model="gpt-3.5-turbo",  # Test the API with a simple model call
            messages=[{"role": "system", "content": "Test connection"}]
        )
        return True
    except Exception as e:
        return False

# -------------------------------
# ✅ Ask the user for API Key Input
# -------------------------------
with st.sidebar:
    st.subheader("🔐 API Key Setup")

    # Ask user to enter API key in the sidebar
    api_input = st.text_input("Enter OpenAI API Key", type="password")

    # If API key is entered, validate it
    if api_input:
        if test_api_key(api_input):
            st.session_state.openai_api_key = api_input
            st.success("✅ API key is working!")
        else:
            st.error("❌ Invalid API key. Please check your key and try again.")

# -------------------------------
# ✅ Chatbot UI
# -------------------------------
st.title("💬 Insurance Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

system_prompt = """
You are an insurance advisor chatbot.
You can answer questions related to insurance types, claims, policy details, etc.
You are not allowed to answer questions outside the insurance domain.
"""

# -------------------------------
# ✅ Initialize message history
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": "How can I help you in the Insurance domain?"}
    ]

# Display chat history except system prompt
for msg in st.session_state.messages[1:]:
    st.chat_message(msg["role"]).write(msg["content"])

# -------------------------------
# ✅ Chat input
# -------------------------------
prompt = st.chat_input("Type your message...")

if prompt:
    # Check if the API key is valid before proceeding
    if not st.session_state.get("openai_api_key"):
        # Add error message to chat history
        st.session_state.messages.append({"role": "assistant", "content": "⚠️ Please enter a valid API key in the sidebar to continue."})
        
        # Display friendly error message
        st.error("❌ API Key not found. Please enter your API Key in the sidebar to continue.")
        
        # Stop further execution
        st.stop()

    # If API key is available, proceed with the model call
    client = openai.Client(api_key=st.session_state.openai_api_key)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Get model response
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})

        # Stream output
        with st.chat_message("assistant"):
            st.write_stream(stream_data(msg))
    except Exception as e:
        error_message = f"❌ Error: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": error_message})
        st.error(error_message)
