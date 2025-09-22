# app.py
import os, json
import boto3
from bedrock_agentcore.runtime import BedrockAgentCoreApp

# ---- config (override in the runtime's env if you want) ----
REGION   = os.environ.get("AWS_REGION", "us-east-1")
MODEL_ID = os.environ.get("MODEL_ID", "anthropic.claude-opus-4-20250514-v1:0")

bedrock = boto3.client("bedrock-runtime", region_name=REGION)
app = BedrockAgentCoreApp()

def _converse(prompt: str) -> str:
    if not prompt:
        return "Hi! Send a 'prompt' field in your payload."
    resp = bedrock.converse(
        modelId=MODEL_ID,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
    )
    parts = resp["output"]["message"]["content"]
    return "".join(p.get("text", "") for p in parts).strip() or "(empty response)"

# AgentCore calls this function with your JSON payload
@app.entrypoint
def invoke(payload: dict):
    """
    Expected payload shape:
      { "prompt": "your message here" }
    """
    try:
        prompt = payload.get("prompt", "")
        return _converse(prompt)
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    # Running locally or in a generic container:
    # this starts the AgentCore app server that handles invoke requests.
    app.run()
