import streamlit as st
import boto3
import json

st.set_page_config(page_title="AI Career Mentor - UpCareer AI", page_icon="🤖")

st.title("🤖 AI Career Mentor")
st.caption("Ask questions about your career path, interview prep, or missing skills!")

# Define the Bedrock Nova invocation function directly here
def invoke_nova_mentor(chat_history_messages, user_input):
    try:
        client = boto3.client(
            service_name="bedrock-runtime",
            region_name="us-east-1"
        )
        model_id = "amazon.nova-micro-v1:0"
        
        formatted_messages = []
        for msg in chat_history_messages:
            role = "user" if msg["role"] == "user" else "assistant"
            formatted_messages.append({
                "role": role,
                "content": [{"text": msg["content"]}]
            })
        
        formatted_messages.append({
            "role": "user",
            "content": [{"text": user_input}]
        })
        
        response = client.converse(
            modelId=model_id,
            messages=formatted_messages,
            inferenceConfig={
                "maxTokens": 1000,
                "temperature": 0.7
            }
        )
        
        output_text = response["output"]["message"]["content"][0]["text"]
        return output_text
        
    except Exception as e:
        return f"⚠️ Error communicating with Amazon Bedrock (Nova Micro): {str(e)}"

# Initialize session state for messages if it doesn't exist
if "mentor_messages" not in st.session_state:
    st.session_state["mentor_messages"] = []

# Display prior chat history
for message in st.session_state["mentor_messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input from chat box
if user_prompt := st.chat_input("Ask your mentor anything..."):
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state["mentor_messages"].append({"role": "user", "content": user_prompt})
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking with Nova Micro..."):
            response_text = invoke_nova_mentor(st.session_state["mentor_messages"][:-1], user_prompt)
            st.markdown(response_text)
            
    st.session_state["mentor_messages"].append({"role": "assistant", "content": response_text})