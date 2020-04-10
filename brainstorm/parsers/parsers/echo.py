# This is a dummy parser and is not in use.


class EchoParser:
    tag = 'echo'
    bindings = ('snapshot', None)

    def __call__(self, context, mq_obj):
        print(f'Got object: {mq_obj}')
        return context, mq_obj
