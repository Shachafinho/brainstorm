import matplotlib.pyplot as plt
import numpy as np

from brainstorm.database.objects import DepthImage
from brainstorm.message_queue import Topic


_RESULT_NAME = 'depth_image'


def _mq_to_db(mq_depth_image, blob_store):
    width, height = mq_depth_image.shape
    data_path = blob_store.path(
        subdir='depth_image', suffix='.png')
    plt.imsave(data_path, depth_image)
    return DepthImage(width, height, str(data_path))


class DepthImageSaver:
    topic = 'depth_image'

    def __call__(self, database, data):
        context, mq_depth_image = Topic(self.topic).deserialize(data)
        print(f'Saving MQ depth image data: {data}')
        context.save('depth_image.raw', data)

        user_id = context.user_id
        snapshot_timestamp = context.snapshot_timestamp

        # Ensure the result doesn't already exist in the DB.
        if database.get_result(user_id, snapshot_timestamp, _RESULT_NAME):
            return

        # Save the result to the DB.
        database.save_result(
            user_id, snapshot_timestamp, _RESULT_NAME,
            _mq_to_db(mq_depth_image, database.blob_store),
        )
