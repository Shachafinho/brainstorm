import attr
import PIL.Image as Image


_TYPE_KEY = 'color_image'


@attr.s(auto_attribs=True, slots=True)
class ColorImage():
    image: Image.Image

    @property
    def width(self):
        return self.image.width

    @property
    def height(self):
        return self.image.height

    def serialize(self, context):
        image_path = context.path('color_image.jpg')
        self.image.save(image_path)
        return {_TYPE_KEY: str(image_path)}

    @classmethod
    def deserialize(cls, serialized_color_image):
        image_path = serialized_color_image[_TYPE_KEY]
        return cls(Image.open(image_path))
