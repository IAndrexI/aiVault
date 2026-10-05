FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir "mem0ai" "fastapi" "uvicorn[standard]" "qdrant-client" "pydantic"

# Copy API server code
COPY server.py .

EXPOSE 8888

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8888"]
