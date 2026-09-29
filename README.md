# E-Commerce AI Knowledge Graph Retrieval System

## 1. Project Overview
This repository implements a lightweight, complete Knowledge Graph-backed AI Agent pipeline for an e-commerce platform. It demonstrates how to parse natural language to query a graph strictly, eliminating hallucinations by separating retrieval from generation.

## 2. Architecture
The pipeline adheres strictly to a **Retrieval Augmented Generation (RAG)** pattern implemented via graphs:
1. **Natural Language Router:** User input is routed to the Google Gemini LLM which is constrained (via JSON schema instructions) to output a structured JSON intent (e.g., `products_by_category`).
2. **Graph Traversal Layer:** Pure Python (NetworkX) intercepts the JSON and executes strict semantic traversals across node edges. **No arbitrary python execution is allowed.**
3. **Grounding Synthesizer:** Gemini is fed back ONLY the resulting NetworkX output and instructed not to use outside knowledge.

## 3. Knowledge Graph Structure & Entity Relationships
Powered by NetworkX `DiGraph`, the schema maps semantics to physical edges:
* `Customer` -> `PLACED` -> `Order`
* `Order` -> `CONTAINS` -> `Product`
* `Product` -> `MADE_BY` -> `Brand`
* `Product` -> `BELONGS_TO` -> `Category`
* `Vendor` -> `SUPPLIES` -> `Product`

## 4. Project Structure
```text
ecommerce_knowledge_graph/
├── data/
│   └── ecommerce_data.json   # Base graph dataset
├── src/
│   ├── graph.py              # Knowledge graph builder (NetworkX)
│   ├── retrieval.py          # Deterministic graph query functions
│   ├── prompts.py            # LLM prompts governing instructions & grounding
│   ├── llm.py                # Google GenAI SDK interface integration
│   └── main.py               # Application entry point / CLI 
├── tests/
│   └── test_graph.py         # Pytest coverage including edge validation
├── .env.example
├── requirements.txt
└── README.md