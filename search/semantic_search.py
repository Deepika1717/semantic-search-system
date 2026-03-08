from sklearn.metrics.pairwise import cosine_similarity

def semantic_search(query_embedding, documents, embeddings, top_k=5):

    similarities = cosine_similarity(
        [query_embedding],
        embeddings
    )[0]

    top_indices = similarities.argsort()[-top_k:][::-1]

    results = [documents[i] for i in top_indices]

    return results