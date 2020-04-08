class PoseParser:
    tag = 'pose'

    def __call__(self, context, snapshot):
        return snapshot.pose
