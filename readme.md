# Operus — Local AI Assistant with Hybrid RAG

Operus is an intelligent AI assistant built with a hybrid retrieval pipeline (FAISS + BM25 + cross-encoder reranking), LLM-based intent routing, real-time web search, and voice interface. It automatically decides whether to answer from documents, search the web, or respond directly — no manual switching needed.

## Architecture

```
User Query
    ↓
Intent Router (LLM-based)
    ↓
┌─────────────┬──────────────┬─────────────┐
needs_retrieval  needs_web      chat/direct
    ↓               ↓              ↓
FAISS+BM25    DuckDuckGo     LLM response
hybrid search  web search
    ↓               ↓
Cross-encoder  Query rewriter
reranking      (context-aware)
    ↓               ↓
└─────────────┴──────────────┘
    ↓
LLM Generation (Groq API / local Qwen2.5)
    ↓
Response + Session Memory update
```

## Features
- **Hybrid RAG** — FAISS semantic search + BM25 keyword search fused with Reciprocal Rank Fusion, reranked with cross-encoder
- **Intent routing** — LLM classifies each query into needs_retrieval, needs_web, chat, or direct_answer
- **Web search** — DuckDuckGo search with context-aware query rewriting for follow-up questions
- **Conversation memory** — rolling 5-turn history per session
- **Voice interface** — Whisper STT + Kokoro TTS (terminal)
- **FastAPI backend** — REST API with session isolation

## Setup

```bash
git clone https://github.com/QuidUtsav/Operus-prototype
cd Operus-prototype
pip install fastapi uvicorn pydantic groq python-dotenv faiss-cpu numpy rank_bm25 sentence-transformers faster-whisper kokoro-onnx duckduckgo-search sounddevice scipy
```

Create `.env` in project root:
```
api_key=your_groq_api_key
```

Get a free Groq API key at console.groq.com

For voice feature, download:
```bash
wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
```

## Running

**Terminal mode:**
```bash
python main.py
```

**API mode:**
```bash
uvicorn api:app --reload
```

## API

### POST /chat
```json
{
  "query": "what is the weather in Pokhara?",
  "session_id": "user123"
}
```
Response:
```json
{
  "response": "The current temperature in Pokhara...",
  "intent": "needs_web",
  "session_id": "user123"
}
```

### GET /health
```json
{"status": "ok"}
```

## Local Model (GPU required, 5GB+ VRAM)
Uncomment the Qwen section in `core/generation.py` and comment out the Groq section to run fully locally with Qwen2.5-1.5B-Instruct.