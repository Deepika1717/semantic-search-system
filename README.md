# Semantic Search System with Fuzzy Clustering and Semantic Cache

## Project Overview

This project implements a **Semantic Search System** using the **20 Newsgroups dataset**. The goal is to allow users to search documents based on **meaning (semantic similarity)** instead of exact keyword matches.

The system converts documents into **vector embeddings**, groups similar documents using **Fuzzy C-Means clustering**, and improves performance using a **Semantic Cache**.

A **FastAPI service** is built on top of the system so users can send queries through an API and retrieve relevant documents.

---

# Features

• Semantic document search using embeddings
• Fuzzy clustering to group similar documents
• Custom semantic cache to reuse previous results
• FastAPI backend for querying the system
• Dataset preprocessing and cleaning
• Modular project structure

---

# Dataset

The project uses the **20 Newsgroups dataset**, which contains about **20,000 news articles** across **20 categories** such as:

* politics
* sports
* religion
* technology
* space
* medicine

This dataset is commonly used for **text classification and NLP experiments**.

---

# Project Structure

```
semantic-search-project

api/
    main.py                # FastAPI server

cache/
    semantic_cache.py      # Semantic cache logic

clustering/
    fuzzy_clustering.py    # Fuzzy C-Means clustering implementation

data/
    loader.py              # Dataset loading and preprocessing

embeddings/
    embedding_model.py     # Sentence transformer model

search/
    semantic_search.py     # Search logic using cosine similarity

index/
    embeddings.pkl         # Saved document embeddings
    documents.pkl          # Saved documents

requirements.txt
README.md
```

---

# How the System Works

The system follows this pipeline:

```
User Query
   ↓
FastAPI Endpoint
   ↓
Query converted to embedding
   ↓
Semantic Cache Check
   ↓
If cache hit → return cached results
If cache miss → perform semantic search
   ↓
Find similar documents
   ↓
Return results
   ↓
Store query in cache
```

---

# Data Preprocessing

Before creating embeddings, the dataset is cleaned.

The preprocessing steps include:

• removing email headers
• removing signatures
• removing quoted replies
• converting text to lowercase
• removing URLs and punctuation
• removing very short documents

This ensures the embeddings capture **meaningful text content**.

---

# Embedding Model

The system uses the **SentenceTransformer model**

```
all-MiniLM-L6-v2
```

Why this model was chosen:

• lightweight and fast
• good semantic understanding
• widely used for semantic search tasks

Each document is converted into a **384-dimensional vector**.

These vectors represent the **semantic meaning of the document**.

---

# Semantic Search Implementation

Semantic search is implemented using **cosine similarity** between embeddings.

Steps:

1. Convert user query to embedding
2. Compare query embedding with document embeddings
3. Calculate cosine similarity scores
4. Return the top most similar documents

This allows the system to find documents with **similar meaning even if the exact words differ**.

Example:

Query:

```
space missions
```

Possible results:

```
NASA launches new satellite
Mars exploration program
International space station updates
```

---

# Fuzzy Clustering

Instead of assigning each document to a single cluster, the system uses **Fuzzy C-Means clustering**.

This means a document can belong to **multiple clusters with different probabilities**.

Example:

```
Document A
Cluster 1 → 0.60
Cluster 2 → 0.30
Cluster 3 → 0.10
```

This is useful because real-world topics often overlap.

Example overlaps:

• politics + firearms
• technology + space
• science + medicine

The clustering helps analyze **topic similarity within the dataset**.

---

# Semantic Cache

Traditional caching works only for **exact query matches**.

Example:

```
query 1: space missions
query 2: space exploration
```

These are similar queries but traditional cache would treat them as different.

The **Semantic Cache** solves this problem by storing:

```
query
query_embedding
search_result
cluster
```

When a new query arrives:

1. The query embedding is compared with cached query embeddings
2. If similarity is above a threshold
3. Cached results are returned

This reduces repeated computations and improves performance.

---

# API Implementation

The project exposes an API using **FastAPI**.

To start the server:

```
uvicorn api.main:app --reload
```

Open API documentation:

```
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## Query Endpoint

```
POST /query
```

Example request:

```
{
 "query": "space exploration"
}
```

Example response:

```
{
 "cache_hit": false,
 "result": [
   "document1",
   "document2",
   "document3"
 ]
}
```

---

## Cache Statistics

```
GET /cache/stats
```

Returns:

```
{
 "total_entries": 10,
 "hits": 3,
 "misses": 7
}
```

---

## Clear Cache

```
DELETE /cache
```

This removes all cached queries.

---

# How to Run the Project

Install dependencies

```
pip install -r requirements.txt
```

Run the API

```
uvicorn api.main:app --reload
```

Open browser

```
http://127.0.0.1:8000/docs
```

You can test queries directly from the interactive API page.

---

# Technologies Used

Python
FastAPI
Sentence Transformers
Scikit-Learn
NumPy
Pickle

---

# Future Improvements

Possible extensions:

• integrate FAISS for faster vector search
• add query result summarization using LLMs
• improve clustering visualization
• deploy the API using Docker
• use Redis for distributed caching

---

# Conclusion

This project demonstrates a **complete semantic search pipeline** including:

• document preprocessing
• embedding generation
• semantic similarity search
• fuzzy clustering
• semantic caching
• API deployment

The system shows how **modern NLP techniques can improve search systems beyond traditional keyword matching**.

---
