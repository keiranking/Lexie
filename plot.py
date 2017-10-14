from matplotlib import pyplot as plt
import numpy as np
# import matplotlib

# Fixing random state for reproducibility
np.random.seed(19680801)


x = np.arange(0.0, 50.0, 2.0)
y = x ** 1.3 + np.random.rand(*x.shape) * 30.0
z = x ** 1.5 + np.random.rand(*x.shape) * 20.0
s = np.random.rand(*x.shape) * 800 + 500

plt.scatter(x, y, None, c="red", alpha=0.7, marker=r'o',
            label="In")
plt.scatter(x, z, None, c="blue", alpha=0.7, marker=r'o',
            label="Out")
plt.xlabel("Cultural relevance")
plt.ylabel("Crossword appearances")
plt.legend(loc=2)
plt.show()
