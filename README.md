# SHL Conversational Assessment Recommender

# Live Deployment

## API Base URL
[https://YOUR-RENDER-URL.onrender.com](https://shl-ai-agent-xfrz.onrender.com)

## Swagger Documentation
[https://YOUR-RENDER-URL.onrender.com/docs](https://shl-ai-agent-xfrz.onrender.com/docs)

## Health Endpoint
[https://YOUR-RENDER-URL.onrender.com/health](https://shl-ai-agent-xfrz.onrender.com/health)




## Overview
This project is a conversational AI-based recommendation system built using FastAPI.

It helps recruiters and hiring managers discover suitable SHL assessments through natural language conversations.

The system supports:
- assessment recommendations
- clarification handling
- conversational refinement
- refusal handling
- assessment comparison

The application uses the official SHL product catalog dataset for recommendations.

---

# Features

- FastAPI REST API
- Conversational recommendation engine
- Stateless conversation handling
- Real SHL catalog integration
- Assessment comparison support
- Clarification prompts
- Refusal handling for unsupported queries
- Relevance-based recommendation matching
- JSON API responses

---

# Tech Stack

- Python
- FastAPI
- Pydantic
- JSON dataset
- Uvicorn

---

# Project Structure

```text
shl-ai-agent/
│
├── app/
│   └── main.py
│
├── data/
│   └── tests.json
│
├── requirements.txt
├── README.md
└── .env


---
---

# API Endpoints

## GET `/health`

Returns API health status.

Response
```json
{
  "status": "ok"
}
```
---

## POST `/chat`

Accepts conversation history and returns SHL assessment recommendations.
---

# Request Example

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Need Java backend developer assessment"
    }
  ]
}
```
---


Response Example
```json
{
  "reply": "Found 3 matching SHL assessments.",
  "recommendations": [
    {
      "name": "Java 8 (New)",
      "url": "https://www.shl.com/solutions/products/product-catalog/view/java-8-new/",
      "test_type": "Technical",
      "remote_support": "yes",
      "adaptive_support": "no"
    }
  ],
  "end_of_conversation": true
}

```

---

Supported Capabilities
Recommendation Queries

Example:

Need Python backend developer assessment
Clarification Queries

Example:

assessment
Comparison Queries

Example:

difference between OPQ and GSA
Refusal Handling

Example:

Give legal hiring advice


---

# Recommendation Logic

The recommendation engine:
1. Combines all conversation messages
2. Extracts relevant keywords
3. Matches keywords against:
   - assessment names
   - descriptions
   - categories
4. Scores assessments by relevance
5. Returns top matching assessments

---


# Dataset

The project uses the SHL product catalog dataset containing:
- assessment names
- descriptions
- product URLs
- categories
- remote support information
- adaptive support information

Dataset Source:

https://tcp-us-prod-rnd.shl.com/voiceRater/shl-ai-hiring/shl_product_catalog.json

---


# Run Locally

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 2. Start Server

```bash
uvicorn app.main:app --reload
```

---
## 3. Open Swagger Documentation

```text
http://127.0.0.1:8000/docs
```

---

# Deployment

The project can be deployed on:
- Render
- Railway
- AWS
- Azure

Recommended start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 10000
```

---
# Assumptions

- Recommendations are keyword and relevance-score based
- Conversations are stateless
- Only SHL assessment-related queries are supported
- SHL catalog data is locally stored in JSON format

---

# Future Improvements

- Semantic search using embeddings
- Vector database integration
- LLM-powered ranking
- Advanced conversational memory
- Real-time SHL catalog synchronization

---

# Author

Mahadev Srinathgoud
