import PIL.Image as Image


class ColorImageParser:
    tag = 'color_image'

    def __call__(self, context, snapshot):
        size = snapshot.color_image.width, snapshot.color_image.height
        image = Image.frombytes('RGB', size, snapshot.color_image.data)
        return image
