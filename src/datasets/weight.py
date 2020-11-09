"""Functions to compute weights for a given dataset"""

import numpy as np

def compute_split_weights(X_paths, y):
    """Compute weights for a given dataset"""
    return [1 - np.sum(y == label) / len(y) for label in set(y)]
