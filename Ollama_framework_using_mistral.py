# Run this command before executing the script
# ollama run mistral
import requests
import json
import streamlit as st
import os

url = "http://localhost:11434/api/generate"
headers = {
    'Content-Type': 'application/json',
}

conversation_history = []

def generate_response(prompt):
    conversation_history.append(prompt)
    full_prompt = "\n".join(conversation_history)
    data = {
        "model": "mistral",
        "stream": False,
        "prompt": full_prompt,
        }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data["response"]
        conversation_history.append(actual_response)
        return actual_response
    else:
        st.error(f"Error: {response.status_code}, {response.text}")
        return None
    
def main():
    st.title("Chatbot with Streamlit")
    prompt = st.text_area("Enter your prompt here:", key="prompt_input")
    if st.button("Generate Response"):
        if prompt:
            response = generate_response(prompt)
            if response is not None:
                st.text("Bot's Response:")
                st.write(response)

if __name__ == "__main__":
    main()