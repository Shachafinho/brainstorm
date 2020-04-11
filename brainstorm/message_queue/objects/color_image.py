import io

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
        bio = io.BytesIO()
        self.image.save(bio, format='jpeg')
        data_token = context.save(
            bio.getvalue(), subdir='color_image', suffix='.jpg')
        return {_TYPE_KEY: data_token}

    @classmethod
    def deserialize(cls, context, serialized_color_image):
        data_token = serialized_color_image[_TYPE_KEY]
        bio = io.BytesIO(context.load(data_token))
        return cls(Image.open(bio))
