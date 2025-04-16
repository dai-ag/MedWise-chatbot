import streamlit as st
import subprocess

# Page config
st.set_page_config(page_title="🩺 MedWise Chatbot", layout="centered")
st.title("🩺 MedWise - Your Friendly Health Chatbot")

# Run LLaMA 3 locally using Ollama
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

# New: Use LLM to classify the query
def is_medical_query_llm(query):
    classification_prompt = (
        "Decide if the following question is about health or medicine. "
        "Reply with only 'Yes' or 'No'.\n\n"
        f"Question: {query}\n\nAnswer:"
    )
    response = query_ollama(classification_prompt).lower()
    return "yes" in response

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm your medical assistant. How can I help you today?"}
    ]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Sidebar actions
def clear_chat_history():
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm your medical assistant. How can I help you today?"}
    ]

st.sidebar.title("🩺 MedWise")
st.sidebar.button("🧹 Clear Chat", on_click=clear_chat_history)
st.sidebar.markdown("🤝🏻 [Let's connect on LinkedIn](https://www.linkedin.com/in/geetika-kanwar-61a33b223)")

# Chat input
user_input = st.chat_input("Ask me a medical question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            if is_medical_query_llm(user_input):
                system_prompt = (
                    "You are a helpful and friendly medical assistant. "
                    "Answer general health-related questions, provide wellness info, and basic first aid guidance. "
                    "Avoid diagnosing or prescribing. Always suggest seeing a real doctor.\n\n"
                    f"User: {user_input}\n\nAssistant:"
                )
            else:
                system_prompt = (
                    f"The following question is not related to medicine or health: '{user_input}'\n"
                    "Respond politely in 20 to 60 words, but let the user know you're mainly focused on health topics."
                )

            response = query_ollama(system_prompt)

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
