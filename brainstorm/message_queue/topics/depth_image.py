import numpy as np


def serialize(context, depth_image):
    depth_image_path = context.path('depth_image.npy')
    np.save(depth_image_path, depth_image)
    return {'depth_image': str(depth_image_path)}


def deserialize(depth_image_dict):
    depth_image_path = depth_image_dict['depth_image']
    return np.load(depth_image_path)
