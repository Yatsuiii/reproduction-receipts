import os
import numpy as np

if os.path.exists("cache/scores.npy"):
    scores = np.load("cache/scores.npy")
else:
    scores = np.random.default_rng(0).normal(size=(100, 5))
    np.save("cache/scores.npy", scores)
print(scores.mean())
