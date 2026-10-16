import boto3
import json

def get_bedrock_client():
    return boto3.client(
        service_name="bedrock-runtime",
        region_name="us-east-1"  # Matches your active us-east-1 region
    )

def invoke_nova_mentor(chat_history_messages, user_input):
    client = get_bedrock_client()
    model_id = "amazon.nova-micro-v1:0"
    
    # Format existing session state messages for Bedrock Converse API
    formatted_messages = []
    for msg in chat_history_messages:
        role = "user" if msg["role"] == "user" else "assistant"
        formatted_messages.append({
            "role": role,
            "content": [{"text": msg["content"]}]
        })
    
    # Append the current prompt
    formatted_messages.append({
        "role": "user",
        "content": [{"text": user_input}]
    })
    
    try:
        response = client.converse(
            modelId=model_id,
            messages=formatted_messages,
            inferenceConfig={
                "maxTokens": 1000,
                "temperature": 0.7
            }
        )
        
        # Extract the response text safely from the Bedrock converse output
        output_text = response["output"]["message"]["content"][0]["text"]
        return output_text
        
    except Exception as e:
        return f"⚠️ Error communicating with Amazon Bedrock (Nova Micro): {str(e)}"