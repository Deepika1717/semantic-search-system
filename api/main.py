from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

from data.loader import load_dataset
from embeddings.embedding_model import embed_documents, embed_query
from clustering.fuzzy_clustering import perform_fuzzy_clustering
from search.semantic_search import semantic_search
from cache.semantic_cache import SemanticCache

from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(title="Semantic Search API")

class QueryRequest(BaseModel):
    query: str


dataset_path = "data/20_newsgroups"

print("Loading dataset...")
documents, labels = load_dataset(dataset_path)


try:

    print("Loading saved embeddings...")

    with open("index/embeddings.pkl", "rb") as f:
        embeddings = pickle.load(f)

    with open("index/documents.pkl", "rb") as f:
        documents = pickle.load(f)

except:

    print("Generating embeddings...")

    embeddings = embed_documents(documents)

    with open("index/embeddings.pkl", "wb") as f:
        pickle.dump(embeddings, f)

    with open("index/documents.pkl", "wb") as f:
        pickle.dump(documents, f)


print("Running fuzzy clustering...")

cluster_centers, membership = perform_fuzzy_clustering(embeddings)


cache = SemanticCache()


def get_cluster(query_embedding):

    similarities = cosine_similarity(
        [query_embedding],
        cluster_centers
    )[0]

    return int(np.argmax(similarities))


@app.post("/query")
def query_system(request: QueryRequest):

    query = request.query

    query_embedding = embed_query(query)

    hit, entry, score = cache.lookup(query_embedding)

    if hit:

        return {
            "query": query,
            "cache_hit": True,
            "matched_query": entry["query"],
            "similarity_score": float(score),
            "result": entry["result"],
            "dominant_cluster": entry["cluster"]
        }

    results = semantic_search(query_embedding, documents, embeddings)

    cluster = get_cluster(query_embedding)

    cache.add(query, query_embedding, results, cluster)

    return {
        "query": query,
        "cache_hit": False,
        "matched_query": None,
        "similarity_score": None,
        "result": results,
        "dominant_cluster": cluster
    }


@app.get("/cache/stats")
def cache_stats():

    return cache.stats()


@app.delete("/cache")
def clear_cache():

    cache.clear()

    return {"message": "Cache cleared"}