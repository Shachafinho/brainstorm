import numpy as np


class DepthImageParser:
    tag = 'depth_image'

    def __call__(self, context, snapshot):
        shape = snapshot.depth_image.height, snapshot.depth_image.width
        array = np.asarray(snapshot.depth_image.data, np.float32)
        return np.reshape(array, shape)
