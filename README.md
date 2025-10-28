
# 💬 Insurance Chatbot

This is a Streamlit-powered chatbot designed to assist users with insurance-related queries. It utilizes the OpenAI API to provide conversational responses, helping users with topics such as insurance types, claims, policy details, and more.

## Features

- **API Key Setup**: The chatbot can fetch the OpenAI API key from the system environment variable or allow the user to input a custom key.
- **Model Selection**: Users can select from popular OpenAI models, including GPT-3.5 and GPT-4.
- **Real-time Chat**: The chatbot uses Streamlit's real-time capabilities to interact with users and stream responses.
- **Error Handling**: If the API key is invalid or there's any error in generating a response, the issue is clearly shown to the user and logged in the chat history.
- **Insurance Domain-Specific**: The chatbot is pre-configured with insurance-related system prompts to ensure that the responses are relevant to the insurance domain.

## Requirements

- Python 3.x
- Streamlit
- OpenAI Python Client

### Install the dependencies

```bash
pip install streamlit openai
```

## How to Run

1. **Set up your OpenAI API Key**:
   - You can either set the `OPENAI_API_KEY` in your environment variable or enter it manually through the app's sidebar.

2. **Run the Streamlit App**:
   - To launch the chatbot, run the following command in the terminal:

   ```bash
   streamlit run app.py
   ```

3. **Start interacting with the chatbot**:
   - The application will open in your browser where you can enter queries related to insurance. You can select a model, provide the OpenAI API key, and begin chatting.

## Project Structure

```
insurance-chatbot/
│
├── app.py                  # Main Streamlit app file
└── requirements.txt        # List of Python dependencies
```

## Code Explanation

### Key Functions:

1. **API Key Setup**: 
   - The app checks if an API key is available in the environment variable (`OPENAI_API_KEY`) or allows the user to input a key through the sidebar.

2. **Test API Key**: 
   - The `test_api_key` function ensures that the provided API key is working before starting the conversation.

3. **Chat History**: 
   - All user inputs and chatbot responses are logged in `st.session_state` to maintain chat history.

4. **Error Handling**: 
   - If there is any error while making an API call (e.g., invalid API key, API rate limits, etc.), the chatbot displays a user-friendly error message.

### Example Usage:

```python
import openai
import streamlit as st
import time
import os

def stream_data(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.03)

def test_api_key(api_key):
    try:
        client = openai.Client(api_key=api_key)
        client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Test connection"}]
        )
        return True
    except Exception as e:
        return False

if "openai_api_key" not in st.session_state:
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key and test_api_key(api_key):
        st.session_state.openai_api_key = api_key
    else:
        st.warning("OPENAI_API_KEY from environment is not working. Please check the system OPENAI_API_KEY.")

with st.sidebar:
    api_key_source = st.radio("Select API Key Source", options=["System Environment Variable", "User Input"], index=0)
    if api_key_source == "User Input":
        api_input = st.text_input("Enter OpenAI API Key", type="password")
        if api_input:
            if test_api_key(api_input):
                st.session_state.openai_api_key = api_input
                st.success("✅ API key working!")
            else:
                st.error("❌ Invalid API key. Please check your key and try again.")                

    model = st.selectbox("Select Model", ["gpt-3.5-turbo", "gpt-4", "gpt-3.5-turbo-16k", "gpt-4-32k"], index=0)

st.title("💬 Insurance Chatbot")
system_prompt = "You are an insurance advisor chatbot. You can answer questions related to insurance types, claims, policy details, etc."

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}, {"role": "assistant", "content": "How can I help you in the Insurance domain?"}]

for msg in st.session_state.messages[1:]:
    st.chat_message(msg["role"]).write(msg["content"])

prompt = st.chat_input("Type your message...")

if prompt:
    if not st.session_state.openai_api_key:
        st.info("⚠️ Please enter a valid API key in the sidebar to continue.")
        st.stop()

    client = openai.Client(api_key=st.session_state.openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=st.session_state.messages
        )
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        with st.chat_message("assistant"):
            st.write_stream(stream_data(msg))
    except Exception as e:
        error_message = f"❌ Error: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": error_message})
        st.error(error_message)
```

## Contributing

Feel free to open issues and submit pull requests for bug fixes or enhancements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
