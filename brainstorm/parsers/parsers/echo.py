class EchoParser:
    tag = 'echo'
    bindings = ('snapshot', None)

    def __call__(self, context, obj):
        print(f'Got object: {obj}')
        return obj
