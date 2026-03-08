import numpy as np
import skfuzzy as fuzz

def perform_fuzzy_clustering(embeddings, n_clusters=5):

    data = np.array(embeddings).T

    cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
        data,
        c=n_clusters,
        m=2,
        error=0.005,
        maxiter=1000,
        init=None
    )

    return cntr, u