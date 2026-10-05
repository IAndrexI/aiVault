# aiVault: Sovereign AI Agent Memory & Personality Stack

A composable, self-hosted, and future-proof long-term memory architecture for AI agents (Antigravity IDE, Cursor, Claude Code, and self-hosted local agents).

---

## Architecture Overview

```
                      ┌────────────────────────────────────────┐
                      │              CLIENT LAYER              │
                      │  Antigravity IDE / Local Python Agents │
                      └───────────────────┬────────────────────┘
                                          │
 ┌────────────────────────────────────────┼────────────────────────────────────────┐
 │                                        │ (MCP Protocol)                         │ (REST / Vector)
 ▼                                        ▼                                        ▼
┌───────────────────────┐        ┌───────────────────────┐        ┌───────────────────────┐
│     PERSONALITY       │        │    DYNAMIC MEMORY     │        │   DEEP CODE & DOCS    │
│  SOUL.md (Markdown)   │        │      Mem0 Engine      │        │     Qdrant Engine     │
├───────────────────────┤        ├───────────────────────┤        ├───────────────────────┤
│ • Identity & Voice    │        │ • Hardware configs    │        │ • Entire repositories │
│ • Behavioral Rules    │        │ • Coding preferences  │        │ • API documentations  │
│ • Zero lock-in        │        │ • Auto-deduplicated   │        │ • Sub-ms vector search│
└───────────────────────┘        └──────────┬────────────┘        └───────────▲───────────┘
                                          │                                   │
                                          └────── Stores Vectors In ──────────┘
```

---

## Quick Start Deployment

### 1. Clone & Configure Environment
```bash
git clone https://github.com/IAndrexI/aiVault.git /opt/agent-memory
cd /opt/agent-memory
cp .env.example .env
nano .env # Add your LLM provider and API key
```

### 2. Start the Services
```bash
docker compose up -d
```

### 3. Verify Health
- **Qdrant Dashboard:** `http://<HOST_IP>:6333/dashboard`
- **Mem0 API:** `http://<HOST_IP>:8888/docs`

---

## Connecting Your Agents (Antigravity / MCP)

Add the server to your MCP configuration (`mcp_config.json`):

```json
{
  "mcpServers": {
    "agent-memory": {
      "command": "npx",
      "args": ["-y", "mem0-mcp"],
      "env": {
        "MEM0_API_URL": "http://<HOST_IP>:8888",
        "MEM0_USER_ID": "your_username"
      }
    }
  }
}
```

---

## Personality & Governance (`SOUL.md`)

Place `SOUL.md` in your project root or Obsidian vault. Antigravity and compatible agents will adopt these instructions as the core persona and operating rules.

---

## Zero Lock-In Export

To export all memories into plain JSON at any time:

```bash
curl -X GET "http://<HOST_IP>:8888/v1/memories?user_id=your_username" -o memories_backup.json
```
