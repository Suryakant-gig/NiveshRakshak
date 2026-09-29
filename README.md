# NiveshRakshak

AI-powered protection against financial scams and misinformation.

## MVP Flow

Input → Claim Extraction → Scam Signals → Hybrid Evidence Retrieval → Reranking → Risk Engine → Explainable Report

## Run

Backend:
```bash
uvicorn backend.app.main:app --reload
```

Frontend:
```bash
streamlit run frontend/app.py
```
