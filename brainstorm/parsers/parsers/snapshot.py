class SnapshotParser:
    tag = 'snapshot'

    def __call__(self, context, whole_data):
        return whole_data.snapshot
