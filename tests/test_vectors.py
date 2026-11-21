import numpy as np
import pytest

from rag.vectors import cosine, top_k


def test_cosine_of_same_direction_is_one():
    assert cosine(np.array([1.0, 2.0]), np.array([2.0, 4.0])) == pytest.approx(1.0)


def test_top_k_orders_by_similarity():
    vectors = np.array([[1.0, 0.0], [0.0, 1.0], [0.7, 0.7]])
    assert top_k(np.array([1.0, 0.1]), vectors, k=2) == [0, 2]
