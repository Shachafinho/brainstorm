from brainstorm.message_queue.objects import DepthImage


def serialize(context, depth_image):
    return depth_image.serialize(context)


def deserialize(serialized_depth_image):
    return DepthImage.deserialize(serialized_depth_image)
