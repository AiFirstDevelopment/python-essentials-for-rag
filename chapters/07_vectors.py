# Chapter 7: NumPy. Arrays overload - * @ and <, so math on a whole array is one expression.
import numpy as np

old = np.array([0.82, 0.91, 0.40, 0.77])
new = np.array([0.85, 0.62, 0.71, 0.79])

change = new - old                    # every question at once, no loop
print(change.round(2))                # [ 0.03 -0.29  0.31  0.02]
print(change < -0.1)                  # [False  True False False]

a = np.array([1.0, 2.0, 3.0])
b = np.array([2.0, 4.0, 6.5])
cosine = a @ b / (np.linalg.norm(a) * np.linalg.norm(b))   # how alike two embeddings are
print(round(float(cosine), 4))
