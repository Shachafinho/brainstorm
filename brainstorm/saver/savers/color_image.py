import io

from brainstorm.database import DBError
from brainstorm.database.objects import ColorImage
from brainstorm.message_queue import Topic


_RESULT_NAME = 'color_image'


def _mq_to_db(mq_color_image, blob_store):
    bio = io.BytesIO()
    mq_color_image.image.save(bio, format='jpeg')
    data_token = blob_store.save(
        bio.getvalue(), subdir='color_image', suffix='.jpg')

    return ColorImage(
        mq_color_image.width,
        mq_color_image.height,
        data_token,
    )


class ColorImageSaver:
    topic = 'color_image'

    def __call__(self, database, data):
        context, mq_color_image = Topic(self.topic).deserialize(data)
        print(f'Saving MQ color image data: {data}')
        context.save('color_image.raw', data)

        # Save the result to the DB.
        db_color_image = _mq_to_db(mq_color_image, database.blob_store)
        try:
            database.save_result(
                context.user_id, context.snapshot_timestamp, _RESULT_NAME,
                db_color_image,
            )
        except DBError:
            # Remove redundant file
            database.blob_store.remove(db_color_image.data_token)
            raise
