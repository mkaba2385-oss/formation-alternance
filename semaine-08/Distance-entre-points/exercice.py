import numpy as np

points = np.random.rand(100, 2)

diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]

distances = np.sqrt(np.sum(diff**2, axis=-1))
print(distances.shape)