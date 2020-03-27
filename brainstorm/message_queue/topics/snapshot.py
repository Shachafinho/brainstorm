from brainstorm.formats import Formatter


DEFAULT_FORMATTER = Formatter('protobuf')


def serialize(context, snapshot_obj):
    snapshot_path = context.path('snapshot')
    with open(snapshot_path, 'wb') as wf:
        DEFAULT_FORMATTER.write_snapshot(snapshot_obj, wf)

    return {'snapshot': str(snapshot_path)}


def deserialize(snapshot_dict):
    snapshot_path = snapshot_dict['snapshot']
    with open(snapshot_path, 'rb') as rf:
        return DEFAULT_FORMATTER.read_snapshot(rf)
