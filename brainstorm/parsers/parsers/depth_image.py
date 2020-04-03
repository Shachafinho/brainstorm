import numpy as np


class DepthImageParser:
    tag = 'depth_image'

    def __call__(self, context, snapshot):
        size = snapshot.depth_image.height, snapshot.depth_image.width
        return np.reshape(np.asfarray(snapshot.depth_image.data), size)
