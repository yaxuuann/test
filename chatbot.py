import streamlit as st
import requests

# Dummy function for your LLaMA chatbot – replace with your real code
def generate_llama_response(prompt):
    return f"LLaMA says: {prompt[::-1]}"  # Reverse as dummy response

# Product recommendation fetcher
def get_recommendations(user_id):
    url = f"https://icp-t02-grp4-api.onrender.com/api/v1/ecommerce/recommendation/user/{user_id}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                return data
            else:
                return "No recommendations found for this user."
        else:
            return f"API error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

# Page config
st.set_page_config(page_title="TokoSawit Chatbot", page_icon="🛍️")
st.title("🛍️ TokoSawit Assistant")

# Session state
if "mode" not in st.session_state:
    st.session_state.mode = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mode selection buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("🛒 Recommended for You"):
        st.session_state.mode = "recommend"
        st.session_state.messages = []

with col2:
    if st.button("💬 General Chat"):
        st.session_state.mode = "chat"
        st.session_state.messages = []

# If mode is selected
if st.session_state.mode:
    # Display previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    prompt = st.chat_input("Say something...")

    if prompt:
        # Show user message
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Handle recommendation mode
        if st.session_state.mode == "recommend":
            with st.chat_message("assistant"):
                with st.spinner("Fetching recommendations..."):
                    user_id = "13f5223e-f04a-4fa8-9ef2-cf36060f0d6d"  # Static test user
                    recommendations = get_recommendations(user_id)

                    if isinstance(recommendations, list):
                        formatted = "Here are some products recommended for you:\n\n"
                        for i, rec in enumerate(recommendations, 1):
                            formatted += f"{i}. **{rec.get('product_name', 'Unknown')}**\n"
                            formatted += f"   - Category: {rec.get('category', 'N/A')}\n"
                            formatted += f"   - Price: ${rec.get('price', 'N/A')}\n\n"
                    else:
                        formatted = f"⚠️ {recommendations}"

                    st.markdown(formatted)
                    st.session_state.messages.append({"role": "assistant", "content": formatted})

        # Handle LLaMA general chat mode
        elif st.session_state.mode == "chat":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = generate_llama_response(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
