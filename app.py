import streamlit as st
import replicate
import os

# App title
st.set_page_config(page_title="🩺 MedWise Chatbot")

# Replicate Credentials
with st.sidebar:
    st.title('🩺 MedWise Chatbot')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key already provided!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
    os.environ['REPLICATE_API_TOKEN'] = replicate_api

    st.subheader('Models and Parameters')
    selected_model = st.selectbox('LLM model:', [
        'LLaMA 3 (8B Instruct)'
    ], key='selected_model')

    if selected_model == 'LLaMA 3 (8B Instruct)':
        llm = 'meta/meta-llama-3-8b-instruct'

    temperature = st.slider('temperature', min_value=0.01, max_value=2.0, value=0.1, step=0.01)
    top_p = st.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    st.markdown("🤝🏻 Let's connect on [LinkedIn](https://www.linkedin.com/in/geetika-kanwar-61a33b223)!")

# Store LLM generated responses
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I’m MedWise, your medical assistant. How can I help you today?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I’m MedWise, your medical assistant. How can I help you today?"}]
st.sidebar.button('🧹 Clear Chat History', on_click=clear_chat_history)

# Function to check if prompt is medical-related
def is_medical_topic(prompt):
    medical_keywords = [
        "health", "disease", "symptom", "medicine", "treatment", "diagnosis", "therapy",
        "doctor", "hospital", "surgery", "vaccine", "infection", "pain", "anatomy", "physiology",
        "psychology", "pharmacology", "cardiology", "diabetes", "covid", "fever", "flu", "cancer",
        "mental health", "depression", "nutrition", "exercise", "medical", "checkup", "illness"
    ]
    prompt_lower = prompt.lower()
    return any(keyword in prompt_lower for keyword in medical_keywords)

# Function to generate model response
def generate_llama_response(prompt_input, llm):
    string_dialogue = "You are a helpful assistant focused only on medical topics."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += f"User: {dict_message['content']}\n"
        else:
            string_dialogue += f"Assistant: {dict_message['content']}\n"

    if is_medical_topic(prompt_input):
        final_prompt = f"{string_dialogue}\nUser: {prompt_input}\nAssistant:"
    else:
        final_prompt = (
            f"{string_dialogue}\nUser: {prompt_input}\n"
            "Assistant: I am a medical assistant and I specialize only in health-related topics. "
            "However, here's a brief overview of your topic in 50–80 words:\n"
        )

    inputs = {
        "prompt": final_prompt,
        "temperature": temperature,
        "top_p": top_p,
        "system_prompt": "You are a helpful assistant focused only on medical topics."
    }

    st.write("Debug Input to Replicate:", inputs)

    try:
        output = replicate.run(llm, input=inputs)
    except replicate.exceptions.ReplicateError as e:
        st.error("❌ Error while contacting Replicate API. Check your API token, model name, or quota.")
        st.stop()

    return output

# Chat Input
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate assistant response
if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("🧠 Thinking..."):
            response = generate_llama_response(prompt, llm)
            full_response = ''
            placeholder = st.empty()
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
