from brainstorm.database.objects import Feelings
from brainstorm.message_queue import Topic


_RESULT_NAME = 'feelings'


def _mq_to_db(mq_feelings):
    return Feelings(
        mq_feelings.hunger, mq_feelings.thirst,
        mq_feelings.exhaustion, mq_feelings.happiness,
    )


class FeelingsSaver:
    topic = 'feelings'

    def __call__(self, database, data):
        context, mq_feelings = Topic(self.topic).deserialize(data)
        print(f'Saving MQ feelings data: {data}')
        context.save('feelings.raw', data)

        # Save the result to the DB.
        database.save_result(
            context.user_id, context.snapshot_timestamp, _RESULT_NAME,
            _mq_to_db(mq_feelings),
        )
