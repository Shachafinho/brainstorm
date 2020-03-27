import PIL.Image as Image


def serialize(context, color_image):
    color_image_path = context.path('color_image.jpg')
    color_image.save(color_image_path)
    return {'color_image': str(color_image_path)}


def deserialize(color_image_dict):
    color_image_path = color_image_dict['color_image']
    return Image.open(color_image_path)
