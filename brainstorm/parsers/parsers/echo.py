class EchoParser:
    tag = 'echo'
    bindings = [('snapshot', 'echo'), ('echo', 'result')]

    def __call__(self, message):
        return message
