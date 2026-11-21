import numpy as np
from sklearn.cross_validation import cross_val_score
from sklearn.svm import LinearSVC

y = np.loadtxt("data/labels.csv", dtype=np.int, delimiter=",")
X = np.loadtxt("data/features.csv", delimiter=",")
print(cross_val_score(LinearSVC(), X, y, cv=5).mean())
