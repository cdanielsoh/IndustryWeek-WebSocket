import json
import boto3
import websocket
from time import sleep

bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-west-2'
)

ws_url = f"ws://localhost:8765"


def lambda_handler(event, context):
    question = event['question']

    message = {
        "role": "user",
        "content": [
            {"text": json.dumps(question)},
        ]
    }

    response = bedrock_runtime.converse(
        modelId='anthropic.claude-3-haiku-20240307-v1:0',
        messages=[message]
    )

    bedrock_response = response["output"]["message"]["content"][0]["text"]

    try:
        ws = websocket.create_connection(ws_url)
        ws.send(json.dumps({"message": bedrock_response}))
        sleep(10)
        ws.close()

        return {
            'statusCode': 200,
            'body': json.dumps(f'Message: {bedrock_response} sent to WebSocket')
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to send message')
        }
