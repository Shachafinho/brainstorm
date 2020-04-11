from brainstorm.database.objects import User
from brainstorm.message_queue import Topic


def _mq_to_db(mq_user_information):
    return User(
        mq_user_information.user_id, mq_user_information.name,
        mq_user_information.birth_date, mq_user_information.gender,
    )


class UserInformationSaver:
    topic = 'user_information'

    def __call__(self, database, data):
        context, mq_user_information = Topic(self.topic).deserialize(data)
        print(f'Saving MQ user information data: {data}')
        context.save('user.raw', data)

        # Save the user to the DB.
        database.save_user(_mq_to_db(mq_user_information))
