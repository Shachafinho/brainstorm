from brainstorm.message_queue.objects import Feelings


class FeelingsParser:
    tag = 'feelings'
    bindings = ('snapshot', tag)

    def __call__(self, context, mq_snapshot):
        return context, Feelings(
            mq_snapshot.feelings.hunger,
            mq_snapshot.feelings.thirst,
            mq_snapshot.feelings.exhaustion,
            mq_snapshot.feelings.happiness,
        )
