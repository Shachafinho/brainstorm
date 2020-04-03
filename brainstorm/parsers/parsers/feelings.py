class FeelingsParser:
    tag = 'feelings'

    def __call__(self, context, snapshot):
        return snapshot.feelings
