import matplotlib.pyplot as plt
import numpy as np

from brainstorm.database.objects import DepthImage
from brainstorm.message_queue import Topic


class DepthImageSaver:
    topic = 'depth_image'

    def __call__(self, database, data):
        context, mq_depth_image = Topic(self.topic).deserialize(data)
        print(f'Saving MQ depth image data: {data}')
        context.save('depth_image.raw', data)

        width, height = mq_depth_image.shape
        data_path = context.path('depth_image.png')
        plt.imsave(data_path, mq_depth_image)
        database.save_result(
            context.user_id, context.snapshot_timestamp, 'depth_image',
            DepthImage(width, height, str(data_path))
        )
