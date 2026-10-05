import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Union
from mem0 import Memory

app = FastAPI(title="aiVault Mem0 Server")

# Configure vector store and LLM provider
config: Dict[str, Any] = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": os.getenv("QDRANT_HOST", "agent_qdrant"),
            "port": int(os.getenv("QDRANT_PORT", "6333")),
        }
    },
    "llm": {
        "provider": os.getenv("LLM_PROVIDER", "openai"),
        "config": {
            "api_key": os.getenv("OPENAI_API_KEY", ""),
        }
    }
}

# Optional local Ollama embeddings configuration
if os.getenv("OLLAMA_BASE_URL"):
    config["embedder"] = {
        "provider": "ollama",
        "config": {
            "model": os.getenv("OLLAMA_MODEL", "bge-m3"),
            "ollama_base_url": os.getenv("OLLAMA_BASE_URL"),
        }
    }

memory = Memory.from_config(config)

class AddMemoryRequest(BaseModel):
    messages: Union[str, List[Dict[str, str]]]
    user_id: Optional[str] = "default_user"
    agent_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class SearchMemoryRequest(BaseModel):
    query: str
    user_id: Optional[str] = "default_user"
    agent_id: Optional[str] = None

@app.post("/v1/memories")
def add_memory(req: AddMemoryRequest):
    try:
        return memory.add(req.messages, user_id=req.user_id, agent_id=req.agent_id, metadata=req.metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/memories")
def get_memories(user_id: Optional[str] = "default_user"):
    try:
        return memory.get_all(user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/memories/search")
def search_memory(req: SearchMemoryRequest):
    try:
        return memory.search(req.query, user_id=req.user_id, agent_id=req.agent_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "healthy"}
