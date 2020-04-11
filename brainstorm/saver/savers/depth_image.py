import io

import matplotlib.pyplot as plt

from brainstorm.database import DBError
from brainstorm.database.objects import DepthImage
from brainstorm.message_queue import Topic


_RESULT_NAME = 'depth_image'


def _mq_to_db(mq_depth_image, blob_store):
    bio = io.BytesIO()
    plt.imsave(bio, mq_depth_image.data)
    data_token = blob_store.save(
        bio.getvalue(), subdir='depth_image', suffix='.png')

    return DepthImage(
        mq_depth_image.width,
        mq_depth_image.height,
        data_token,
    )


class DepthImageSaver:
    topic = 'depth_image'

    def __call__(self, database, data):
        context, mq_depth_image = Topic(self.topic).deserialize(data)
        print(f'Saving MQ depth image data: {data}')
        context.save('depth_image.raw', data)

        # Save the result to the DB.
        db_depth_image = _mq_to_db(mq_depth_image, database.blob_store)
        try:
            database.save_result(
                context.user_id, context.snapshot_timestamp, _RESULT_NAME,
                db_depth_image,
            )
        except DBError:
            # Remove redundant file
            database.blob_store.remove(db_depth_image.data_token)
            raise
