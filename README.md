# Ashvon RAG Chatbot

A retrieval-augmented chatbot for the Ashvon Technologies website.

It answers visitor questions using only approved public website content and provides source links.

## Features
- Website content ingestion
- Semantic retrieval
- Grounded answer generation
- Source citations
- FastAPI chat API
- Embeddable website chat widget

## Approved Knowledge Sources
- https://ashvontech.com/
- https://ashvontech.com/about
- https://ashvontech.com/edtech
- https://ashvontech.com/it-services

## Tech Stack
- Python
- FastAPI
- OpenAI embeddings and chat model
- ChromaDB for MVP vector storage
- JavaScript chat widget

## Setup
1. Clone the repository
2. Create a virtual environment
3. Install dependencies
4. Copy `.env.example` to `.env`
5. Add API keys
6. Run website ingestion
7. Start the API

## Important
Do not commit `.env`, API keys, scraped client content, chat logs, or private documents.
