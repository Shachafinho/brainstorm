import PIL.Image as Image

from brainstorm.message_queue.objects import ColorImage


class ColorImageParser:
    tag = 'color_image'
    bindings = ('snapshot', tag)

    def __call__(self, context, snapshot):
        size = snapshot.color_image.width, snapshot.color_image.height
        image = Image.frombytes('RGB', size, snapshot.color_image.data)
        return ColorImage(image)
