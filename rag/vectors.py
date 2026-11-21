import numpy as np


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


def top_k(query: np.ndarray, vectors: np.ndarray, k: int = 3) -> list[int]:
    """Indexes of the k rows of `vectors` most like `query`, best first."""
    scores = vectors @ query / (np.linalg.norm(vectors, axis=1) * np.linalg.norm(query))
    return [int(i) for i in np.argsort(scores)[::-1][:k]]
