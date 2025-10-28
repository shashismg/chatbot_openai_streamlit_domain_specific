
# 💬 Insurance Chatbot

This is a Streamlit-powered chatbot designed to assist users with insurance-related queries. It utilizes the OpenAI API to provide conversational responses, helping users with topics such as insurance types, claims, policy details, and more.

## Features

- **API Key Setup**: The chatbot can fetch the OpenAI API key from the system environment variable or allow the user to input a custom key.
- **Real-time Chat**: The chatbot uses Streamlit's real-time capabilities to interact with users and stream responses.
- **Error Handling**: If the API key is invalid or there's any error in generating a response, the issue is clearly shown to the user and logged in the chat history.
- **Insurance Domain-Specific**: The chatbot is pre-configured with insurance-related system prompts to ensure that the responses are relevant to the insurance domain.
- **User-friendly API Key Error**: If the API key is missing, the app will display a friendly error message and ask the user to input the key.

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

5. **User-Friendly API Key Error**:
   - If the user tries to interact with the chatbot without providing the API key, a clear error message will be shown asking them to enter the key, and this message will be added to the chat history.

