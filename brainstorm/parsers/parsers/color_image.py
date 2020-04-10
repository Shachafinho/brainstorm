import PIL.Image as Image

from brainstorm.message_queue.objects import ColorImage


class ColorImageParser:
    tag = 'color_image'
    bindings = ('snapshot', tag)

    def __call__(self, context, mq_snapshot):
        size = mq_snapshot.color_image.width, mq_snapshot.color_image.height
        image = Image.frombytes('RGB', size, mq_snapshot.color_image.data)
        return context, ColorImage(image)
