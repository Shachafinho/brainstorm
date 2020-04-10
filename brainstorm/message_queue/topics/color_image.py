from brainstorm.message_queue.objects import ColorImage


def serialize(context, color_image):
    return color_image.serialize(context)


def deserialize(serialized_color_image):
    return ColorImage.deserialize(serialized_color_image)
