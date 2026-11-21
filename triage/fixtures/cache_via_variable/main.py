import os
import numpy as np

cache_path = os.path.join("results", "svc_scores.npy")
if not os.path.exists(cache_path):
    scores = np.random.default_rng(0).normal(size=(100, 5))
    np.save(cache_path, scores)
scores = np.load(cache_path)
print(scores.mean())
