# Dockerfile
FROM python:3.11-slim

# Avoid interactive prompts and speed up installs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (if you add more tools later, add libs here)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App
COPY app.py .

# Default env you can override in AgentCore Runtime console
ENV AWS_REGION=us-east-1 \
    MODEL_ID=anthropic.claude-opus-4-20250514-v1:0

# Run the AgentCore app server
CMD ["python", "app.py"]
