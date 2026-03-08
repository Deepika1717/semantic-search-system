from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed_documents(documents):

    embeddings = model.encode(
        documents,
        show_progress_bar=True
    )

    return embeddings


def embed_query(query):

    return model.encode([query])[0]