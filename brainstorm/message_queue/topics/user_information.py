import arrow

from brainstorm.common import UserInformation


def serialize(context, user_information):
    return {
        'user': {
            'user_id': user_information.user_id,
            'name': user_information.name,
            'birth_date': user_information.birth_date.float_timestamp,
            'gender': user_information.gender,
        }
    }


def deserialize(user_information_dict):
    return UserInformation(
        user_information_dict['user_id'],
        user_information_dict['name'],
        arrow.get(user_information_dict['birth_date']),
        user_information_dict['gender'],
    )
