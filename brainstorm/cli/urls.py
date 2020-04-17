import furl.furl as furl


def api_base_url(host, port):
    return furl(scheme='http', host=host, port=port)


def get_users_url(host, port):
    return api_base_url(host, port) / 'users'


def get_user_url(host, port, user_id):
    return get_users_url(host, port) / str(user_id)


def get_snapshots_url(host, port, user_id):
    return get_user_url(host, port, user_id) / 'snapshots'


def get_snapshot_url(host, port, user_id, snapshot_timestamp):
    return get_snapshots_url(host, port, user_id) / str(snapshot_timestamp)


def get_result_url(host, port, user_id, snapshot_timestamp, result_name):
    return get_snapshot_url(host, port, user_id, snapshot_timestamp) / \
        str(result_name)
