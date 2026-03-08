Semantic Search System

```markdown
# Semantic Search System with Fuzzy Clustering and Semantic Cache

## Overview

This project implements a lightweight **semantic search system** built on top of the **20 Newsgroups dataset**. The system allows users to query a large corpus of news posts using natural language and retrieve semantically similar documents.

The system includes three major components:

1. **Vector Embeddings & Vector Index**
2. **Fuzzy Clustering of Documents**
3. **Semantic Cache for Query Reuse**
4. **FastAPI Service for Live Query Access**

The design focuses on building the cache and clustering logic **from first principles**, without relying on external caching middleware like Redis or Memcached.

---

# Dataset

The project uses the **20 Newsgroups dataset**, which contains approximately **20,000 news articles across 20 different categories**.

Dataset source:
https://archive.ics.uci.edu/dataset/113/twenty+newsgroups

The dataset contains real-world challenges such as:

- noisy headers
- email signatures
- quoted replies
- inconsistent formatting

These issues are addressed during preprocessing.

---

# System Architecture

The system pipeline follows the architecture below:

```

User Query
│
▼
FastAPI Endpoint
│
▼
Query Embedding
│
▼
Semantic Cache Lookup
│
├── Cache Hit → Return Stored Result
│
└── Cache Miss
│
▼
Semantic Search
│
▼
Cluster Identification
│
▼
Store Result in Cache
│
▼
Return Result

````

---

# Project Structure

```
semantic-search-system

api/
main.py              → FastAPI service

cache/
semantic_cache.py    → Custom semantic cache implementation

clustering/
fuzzy_clustering.py  → Fuzzy C-Means clustering

data/
loader.py            → Dataset loading and preprocessing
20_newsgroups/       → Dataset folder

embeddings/
embedding_model.py   → Sentence Transformer embedding generation

search/
semantic_search.py   → Vector similarity search

index/
embeddings.pkl       → Stored document embeddings
documents.pkl        → Stored documents

requirements.txt
README.md
````

---

# Data Preprocessing

The dataset contains noisy metadata that can negatively affect semantic representation.

The preprocessing pipeline performs:

### Header Removal

Email headers are removed to retain only the meaningful content.

### Quote Removal

Quoted replies from previous messages are removed.

### Signature Removal

Email signatures are removed to avoid noise.

### Text Normalization

* Lowercasing
* URL removal
* punctuation removal
* number removal
* whitespace normalization

Documents shorter than **20 characters** are discarded to avoid meaningless embeddings.

---

# Embedding Model

The project uses:

**SentenceTransformer – all-MiniLM-L6-v2**

Reasons for this choice:

* lightweight and efficient
* strong semantic representation
* widely used for semantic search tasks
* good trade-off between accuracy and performance

Each document is converted into a **384-dimensional vector embedding**.

These embeddings capture **semantic similarity between texts rather than keyword matching**.

---

# Vector Storage

Instead of recomputing embeddings on every startup, embeddings are stored using **pickle serialization**.

Saved files:

```
index/embeddings.pkl
index/documents.pkl
```

Benefits:

* faster API startup
* avoids expensive recomputation
* reduces runtime cost

---

# Fuzzy Clustering

Unlike traditional clustering, **documents may belong to multiple clusters simultaneously**.

This system uses **Fuzzy C-Means clustering**, which assigns each document a **membership probability across clusters** rather than forcing a hard assignment.

Example:

```
Document A
Cluster 1 → 0.65
Cluster 2 → 0.30
Cluster 3 → 0.05
```

This reflects real-world semantics where topics often overlap.

Example overlap:

```
Politics ↔ Firearms ↔ Law
Technology ↔ Space Science
Sports ↔ Health
```

### Cluster Selection

The system currently uses **5 clusters** as a balanced choice between:

* semantic separation
* computational efficiency
* interpretability

Cluster centers are later used to identify the **dominant cluster of a user query**.

---

# Semantic Search

Search is performed using **cosine similarity between embeddings**.

Steps:

1. Convert user query into embedding
2. Compute similarity with all document embeddings
3. Select top-k most similar documents
4. Return the results

Cosine similarity works well for high-dimensional embedding spaces.

---

# Semantic Cache

Traditional caches only match **exact queries**, which fails when users phrase the same question differently.

Example:

```
"What are space missions?"
"Tell me about space exploration."
```

These are semantically similar but textually different.

The implemented **semantic cache** solves this by storing:

```
query
query_embedding
search_result
dominant_cluster
```

When a new query arrives:

1. The query embedding is compared with stored query embeddings
2. If similarity exceeds a defined threshold
3. The stored result is reused

Similarity threshold used:

```
0.85
```

This value balances:

* avoiding false matches
* capturing semantically similar queries

---

# Cache Data Structure

Each cache entry contains:

```
{
query
embedding
result
cluster
}
```

Cache statistics are tracked:

```
total_entries
hit_count
miss_count
hit_rate
```

This helps monitor cache performance.

---

# FastAPI Service

The system exposes a REST API using **FastAPI**.

FastAPI was chosen because it provides:

* high performance
* automatic API documentation
* easy integration with Python ML pipelines

---

# API Endpoints

## POST /query

Accepts a natural language query.

Example request:

```
{
"query": "space exploration missions"
}
```

Example response:

```
{
"query": "space exploration missions",
"cache_hit": false,
"matched_query": null,
"similarity_score": null,
"result": ["document1","document2","document3"],
"dominant_cluster": 2
}
```

---

## GET /cache/stats

Returns cache statistics.

Example:

```
{
"total_entries": 12,
"hit_count": 5,
"miss_count": 7,
"hit_rate": 0.41
}
```

---

## DELETE /cache

Clears the cache and resets statistics.

---

# Running the System

Install dependencies:

```
pip install -r requirements.txt
```

Start the API server:

```
uvicorn api.main:app --reload
```

Open API documentation:

```
http://127.0.0.1:8000/docs
```

---

# Example Workflow

1. User sends query
2. System checks semantic cache
3. If similar query exists → return cached result
4. Otherwise perform semantic search
5. Store result in cache
6. Return response

---

# Key Design Decisions

### Sentence Transformers

Chosen for strong semantic representation and lightweight inference.

### Fuzzy Clustering

Captures overlapping semantic structure rather than rigid labels.

### Semantic Cache

Reduces redundant computation for similar queries.

### Pickle Storage

Avoids repeated embedding computation.

### FastAPI

Provides production-ready API with minimal overhead.

---

# Future Improvements

Potential extensions include:

* ANN vector search using FAISS
* cluster-aware search optimization
* LLM summarization of search results
* adaptive cache thresholds
* distributed vector databases

---

# Conclusion

This project demonstrates a complete semantic search pipeline combining:

* modern NLP embeddings
* fuzzy clustering
* intelligent semantic caching
* production-ready API deployment

The system highlights how semantic understanding and caching strategies can significantly improve search efficiency and scalability.

```

---
