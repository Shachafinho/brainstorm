import io

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
        bio = io.BytesIO()
        np.save(bio, self.data)
        data_token = context.save(
            bio.getvalue(), subdir='depth_image', suffix='.npy')
        return {_TYPE_KEY: data_token}

    @classmethod
    def deserialize(cls, context, serialized_depth_image):
        data_token = serialized_depth_image[_TYPE_KEY]
        bio = io.BytesIO(context.load(data_token))
        return cls(np.load(bio))
