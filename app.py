import streamlit as st
import subprocess

# Page config
st.set_page_config(page_title="🩺 MedWise Chatbot", layout="centered")
st.title("🩺 MedWise - Your Friendly Health Chatbot")

# Medical keywords for filtering
medical_keywords = [
    "health", "doctor", "medicine", "symptom", "treatment", "cure", "disease",
    "mental", "anxiety", "depression", "pain", "fever", "injury", "wellness",
    "nutrition", "diet", "exercise", "fitness", "first aid", "hospital", "clinic"
]

# Check if user input is medical
def is_medical_query(text):
    return any(word in text.lower() for word in medical_keywords)

# Query local Ollama LLaMA 3 model
def query_ollama(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Response took too long. Try again."
    except Exception as e:
        return f"Error: {str(e)}"

# Initial message
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm your medical assistant. How can I help you today?"}
    ]

# Display previous chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Clear history button
def clear_chat_history():
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm your medical assistant. How can I help you today?"}
    ]

st.sidebar.title("🩺 MedWise")
st.sidebar.button("🧹 Clear Chat", on_click=clear_chat_history)
st.sidebar.markdown("🤝🏻 [Let's connect on LinkedIn](https://www.linkedin.com/in/geetika-kanwar-61a33b223)")

# User input
user_input = st.chat_input("Ask me a medical question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            if is_medical_query(user_input):
                system_prompt = (
                    "You are a helpful and friendly medical assistant. "
                    "Give general health advice, info about symptoms, mental wellness, or first aid. "
                    "Don't diagnose or prescribe. Always suggest visiting a certified doctor.\n\n"
                    f"User: {user_input}\n\nAssistant:"
                )
                response = query_ollama(system_prompt)
            else:
                polite_prompt = (
                    f"I'm only trained to talk about health. But here's a brief, polite note on: {user_input} "
                    "Keep it under 80 words."
                )
                response = query_ollama(polite_prompt)

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
