import pathlib

import arrow

from brainstorm.utils.blob_store import BlobStore
from brainstorm.utils.paths import ROOT_DIR


DEFAULT_DATA_DIR = ROOT_DIR.parent / 'mq_data'
TIMESTAMP_FORMAT = 'YYYY-MM-DD_HH-mm-ss-SSSSSS'


class Context:
    """Serves both as a data container and a utility provider.

    The object holds convenient information (based on the message context).

    In addition, it supports numerous utility functions which rely on said
    information.
    """

    def __init__(self, user_id=None, snapshot_timestamp=None, data_dir=None):
        """Construct the context object.

        Args:
            user_id (int): ID of the snapshot owner.
            snapshot_timestamp (:class:`arrow.Arrow`):
              Timestamp of the associated snapshot.
            data_dir (str): Path to the directory which stores all temporary
              data passed in between topics.
        """
        self.user_id = user_id
        self.snapshot_timestamp = snapshot_timestamp
        self._data_dir = pathlib.Path(str(data_dir)) if data_dir \
            else DEFAULT_DATA_DIR
        self._blob_store = BlobStore(self.data_dir)

    @property
    def data_dir(self):
        """The path to the data directory.

        Return:
            str: The path to the data directory.
        """
        return self._data_dir

    def load(self, token):
        """Return the data associated with the specified token.

        Args:
            token (str): Some key associated with stored data.

        Return:
            bytes: The data associated with the specified token.
        """
        return self._blob_store.load(token)

    def save(self, data, suffix=None, prefix=None, subdir=None):
        """Store the specified data and return an associated token.

        Args:
            data (bytes): The data to store.
            suffix (str): Suffix for the file in which the data is stored.
            prefix (str): Prefix for the file in which the data is stored.
            subdir (str): Subdirectory for the file in which the data is
              stored.

        Return:
            str: The token associated with the stored data.
        """
        user_id_str = str(self.user_id) if self.user_id is not None else ''
        timestamp_str = self.snapshot_timestamp.format(TIMESTAMP_FORMAT) \
            if self.snapshot_timestamp is not None else ''
        subdir = subdir or ''

        full_subdir = pathlib.Path(user_id_str, timestamp_str, subdir)
        return self._blob_store.save(data, suffix, prefix, full_subdir)

    def remove(self, token):
        """Remove the data associated with the specified token.

        Args:
            token (str): Some key associated with the stored data.
        """
        self._blob_store.remove(token)

    def serialize(self):
        """Serialize the context object.

        Return:
            dict: A serialized context object.
        """
        context_dict = {
            'data_dir': str(self.data_dir),
        }
        if self.user_id:
            context_dict['user_id'] = self.user_id
        if self.snapshot_timestamp:
            context_dict['snapshot_timestamp'] = \
                self.snapshot_timestamp.float_timestamp

        return context_dict

    @classmethod
    def deserialize(cls, context_dict):
        """Deserialize a context object from its serialized format (dict).

        Args:
            context_dict (dict): A serialized context object.

        Return:
            :class:`~brainstorm.message_queue.Context`:
              The deserialzed context object.
        """
        snapshot_timestamp = arrow.get(context_dict['snapshot_timestamp']) \
            if 'snapshot_timestamp' in context_dict else None
        return cls(
            user_id=context_dict.get('user_id'),
            snapshot_timestamp=snapshot_timestamp,
            data_dir=context_dict['data_dir'],
        )
