class EchoParser:
    tag = 'echo'
    bindings = [('snapshot', 'echo'), ('echo', 'result')]

    def __call__(self, context, message):
        return message
