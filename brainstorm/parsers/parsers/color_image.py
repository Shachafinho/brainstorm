import PIL.Image as Image


class ColorImageParser:
    tag = 'color_image'

    def parse(self, context, snapshot):
        path = context.path('color_image.jpg')
        size = snapshot.color_image.width, snapshot.color_image.height
        image = Image.frombytes('RGB', size, snapshot.color_image.data)
        image.save(path)
