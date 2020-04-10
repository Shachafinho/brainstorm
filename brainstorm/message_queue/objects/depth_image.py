import attr
import numpy as np


_TYPE_KEY = 'depth_image'


@attr.s(auto_attribs=True, slots=True)
class DepthImage():
    data: np.ndarray

    @property
    def width(self):
        return self.data.shape[1]

    @property
    def height(self):
        return self.data.shape[0]

    def serialize(self, context):
        data_path = context.path('depth_image.npy')
        np.save(data_path, self.data)
        return {_TYPE_KEY: str(data_path)}

    @classmethod
    def deserialize(cls, serialized_depth_image):
        data_path = serialized_depth_image[_TYPE_KEY]
        return cls(np.load(data_path))
