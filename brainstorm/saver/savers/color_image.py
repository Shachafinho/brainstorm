import PIL.Image as Image

from brainstorm.database.objects import ColorImage
from brainstorm.message_queue import Topic


class ColorImageSaver:
    topic = 'color_image'

    def __call__(self, database, data):
        context, mq_color_image = Topic(self.topic).deserialize(data)
        print(f'Saving MQ color image data: {data}')
        context.save('color_image.raw', data)

        width, height = mq_color_image.size
        data_path = context.path('color_image.jpg')
        mq_color_image.save(data_path)
        database.save_result(
            context.user_id, context.snapshot_timestamp, 'color_image',
            ColorImage(width, height, str(data_path))
        )
