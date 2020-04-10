from brainstorm.message_queue.objects import UserInformation


def serialize(context, user_information):
    return user_information.serialize(context)


def deserialize(serialized_user_information):
    return UserInformation.deserialize(serialized_user_information)
