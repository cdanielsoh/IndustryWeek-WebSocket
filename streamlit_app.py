import streamlit as st
import boto3
import json
from lambda_function import lambda_handler

# Initialize AWS clients
lambda_client = boto3.client('lambda')

# List of predefined questions
questions = [
    "What is AWS?",
    "When is AWS Industry Week?",
]

st.title("Question Selector")

# Create a dropdown to select a question
selected_question = st.selectbox("Choose a question:", questions)

if st.button("Send Question"):
    # Invoke Lambda function
    # response = lambda_client.invoke(
    #     FunctionName='QuestionProcessorFunction',
    #     InvocationType='RequestResponse',
    #     Payload=json.dumps({'question': selected_question})
    # )
    response = lambda_handler({'question': selected_question},None)

    result = response
    st.success(f"Question sent: {selected_question}")
    st.info(f"Lambda response: {result}")