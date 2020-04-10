from brainstorm.message_queue.objects import Feelings


class FeelingsParser:
    tag = 'feelings'
    bindings = ('snapshot', tag)

    def __call__(self, context, snapshot):
        return Feelings(
            snapshot.feelings.hunger,
            snapshot.feelings.thirst,
            snapshot.feelings.exhaustion,
            snapshot.feelings.happiness,
        )
