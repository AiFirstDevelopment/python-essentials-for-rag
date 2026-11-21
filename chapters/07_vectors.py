# Chapter 7: NumPy.
import numpy as np

old = np.array([0.82, 0.91, 0.40, 0.77])
new = np.array([0.85, 0.62, 0.71, 0.79])

change = new - old
print(change.round(2))
print(change < -0.1)

a = np.array([1.0, 2.0, 3.0])
b = np.array([2.0, 4.0, 6.5])
print(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))
