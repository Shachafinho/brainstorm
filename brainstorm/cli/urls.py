import furl.furl as furl


def api_base_url(host, port):
    """Return API base URL.

    Args:
        host (str): API server hostname.
        port (int): API server port.

    Return:
        str: API base URL.
    """
    return furl(scheme='http', host=host, port=port)


def get_users_url(host, port):
    """Return API URL to get all users.

    Args:
        host (str): API server hostname.
        port (int): API server port.

    Return:
        str: API URL to get all users.
    """
    return api_base_url(host, port) / 'users'


def get_user_url(host, port, user_id):
    """Return API URL to get a specific user's details.

    Args:
        host (str): API server hostname.
        port (int): API server port.
        user_id (int): ID of a specific user.

    Return:
        str: API URL to get a specific user's details.
    """
    return get_users_url(host, port) / str(user_id)


def get_snapshots_url(host, port, user_id):
    """Return API URL to get a specific user's snapshots.

    Args:
        host (str): API server hostname.
        port (int): API server port.
        user_id (int): ID of the snapshots owner.

    Return:
        str: API URL to get a specific user's snapshots.
    """
    return get_user_url(host, port, user_id) / 'snapshots'


def get_snapshot_url(host, port, user_id, snapshot_id):
    """Return API URL to get a specific snapshot.

    Args:
        host (str): API server hostname.
        port (int): API server port.
        user_id (int): ID of the snapshot owner.
        snapshot_id (int): ID of a specific snapshot.

    Return:
        str: API URL to get a specific snapshot.
    """
    return get_snapshots_url(host, port, user_id) / str(snapshot_id)


def get_result_url(host, port, user_id, snapshot_id, result_name):
    """Return API URL to get a specific snapshot's result.

    Args:
        host (str): API server hostname.
        port (int): API server port.
        user_id (int): ID of the snapshot owner.
        snapshot_id (int): ID of a specific snapshot.
        result_name (str): Name of the result.

    Return:
        str: API URL to get a specific snapshot's result.
    """
    return get_snapshot_url(host, port, user_id, snapshot_id) / \
        str(result_name)
