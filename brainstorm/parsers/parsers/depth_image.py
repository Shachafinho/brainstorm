import numpy as np

from brainstorm.message_queue.objects import DepthImage


class DepthImageParser:
    tag = 'depth_image'
    bindings = ('snapshot', tag)

    def __call__(self, context, mq_snapshot):
        shape = mq_snapshot.depth_image.height, mq_snapshot.depth_image.width
        array = np.asarray(mq_snapshot.depth_image.data, np.float32)
        return context, DepthImage(np.reshape(array, shape))
