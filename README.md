# Advanced RAG with Hybrid Search and Reranking

An advanced document question-answering system using semantic search, keyword search, hybrid retrieval, and cross-encoder reranking before generating answers with an LLM.

## Project Pipeline

Documents → Text Extraction → Chunking → Semantic + Keyword Search → Hybrid Search → Reranking → Top Results → LLM Answer

## Structure

- `app.py` — Streamlit application
- `src/` — RAG pipeline modules
- `knowledge_base/` — document knowledge base
- `requirements.txt` — Python dependencies
