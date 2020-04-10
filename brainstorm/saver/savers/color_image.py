from brainstorm.database.objects import ColorImage
from brainstorm.message_queue import Topic


_RESULT_NAME = 'color_image'


def _mq_to_db(mq_color_image, blob_store):
    data_path = blob_store.path(
        subdir='color_image', suffix='.jpg')
    mq_color_image.image.save(data_path)

    return ColorImage(
        mq_color_image.width,
        mq_color_image.height,
        str(data_path)
    )


class ColorImageSaver:
    topic = 'color_image'

    def __call__(self, database, data):
        context, mq_color_image = Topic(self.topic).deserialize(data)
        print(f'Saving MQ color image data: {data}')
        context.save('color_image.raw', data)

        user_id = context.user_id
        snapshot_timestamp = context.snapshot_timestamp

        # Ensure the result doesn't already exist in the DB.
        if database.get_result(user_id, snapshot_timestamp, _RESULT_NAME):
            return

        # Save the result to the DB.
        database.save_result(
            user_id, snapshot_timestamp, _RESULT_NAME,
            _mq_to_db(mq_color_image, database.blob_store),
        )
