from brainstorm.database.objects import User
from brainstorm.message_queue import Topic


class UserInformationSaver:
    topic = 'user_information'

    def __call__(self, database, data):
        context, mq_user_information = Topic(self.topic).deserialize(data)
        print(f'Saving MQ user information data: {data}')
        context.save('user.raw', data)

        database.save_user(User(
            mq_user_information.user_id, mq_user_information.name,
            mq_user_information.birth_date, mq_user_information.gender,
        ))
