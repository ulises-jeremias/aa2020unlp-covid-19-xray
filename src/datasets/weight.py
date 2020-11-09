"""Functions to compute weights for a given dataset"""

from collections import Counter

def compute_split_weights(X_paths, y):
    """Compute weights for a given dataset"""
    c = Counter(y)
    return [1 - c[label] / len(y) for label in set(y)]
