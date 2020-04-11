from brainstorm.message_queue.objects import ColorImage


def serialize(context, color_image):
    return color_image.serialize(context)


def deserialize(context, serialized_color_image):
    return ColorImage.deserialize(context, serialized_color_image)
