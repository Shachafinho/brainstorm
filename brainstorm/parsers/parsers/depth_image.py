import numpy as np

from brainstorm.message_queue.objects import DepthImage


class DepthImageParser:
    tag = 'depth_image'
    bindings = ('snapshot', tag)

    def __call__(self, context, snapshot):
        shape = snapshot.depth_image.height, snapshot.depth_image.width
        array = np.asarray(snapshot.depth_image.data, np.float32)
        return DepthImage(np.reshape(array, shape))
