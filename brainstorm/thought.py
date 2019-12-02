import datetime as dt
import struct


class Thought:
    HEADER_FORMAT = '<QQL'
    TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, user_id, timestamp, thought):
        self.user_id = user_id
        self.thought = thought
        self.timestamp = timestamp

    def __str__(self):
        datetime_str = self.timestamp.strftime(Thought.TIMESTAMP_FORMAT)
        return f'[{datetime_str}] user {self.user_id}: {self.thought}'

    def __repr__(self):
        class_name, user_id, timestamp, thought = \
            self.__class__.__name__, self.user_id, self.timestamp, self.thought
        return f'{class_name}({user_id=}, {timestamp=}, {thought=})'

    def __eq__(self, other):
        if not isinstance(other, Thought):
            return False
        return (self.user_id == other.user_id and
                self.thought == other.thought and
                self.timestamp == other.timestamp)

    def serialize_header(self):
        # Thought header format is as follows:
        # * 8 bytes (uint64) of user ID
        # * 8 bytes (uint64) of timestamp
        # * 4 bytes (uint32) of the thought's length
        timestamp_num = int(self.timestamp.timestamp())
        return struct.pack(Thought.HEADER_FORMAT, self.user_id,
                           timestamp_num, len(self.thought))

    def serialize_data(self):
        return self.thought.encode()

    def serialize(self):
        # Concatenate header and data to form a complete thought.
        return self.serialize_header() + self.serialize_data()

    @classmethod
    def get_header_size_in_bytes(cls):
        return struct.calcsize(Thought.HEADER_FORMAT)

    @classmethod
    def deserialize_header(cls, header_bytes):
        expected_size = cls.get_header_size_in_bytes()
        if len(header_bytes) != expected_size:
            raise ValueError(
                'Thought header is of wrong size. '
                f'Got {len(header_bytes)}, expected {expected_size}')

        # Extract thought header from bytes.
        user_id, timestamp, thought_size = \
            struct.unpack(Thought.HEADER_FORMAT, header_bytes)
        return user_id, dt.datetime.fromtimestamp(timestamp), thought_size

    @classmethod
    def deserialize_data(cls, data_bytes):
        return data_bytes.decode()

    @classmethod
    def deserialize(cls, data):
        # Deserialize the header.
        header_bytes = data[:cls.get_header_size_in_bytes()]
        user_id, timestamp, thought_size = cls.deserialize_header(header_bytes)

        # Deserialize the data.
        data_bytes = data[len(header_bytes):]
        if len(data_bytes) != thought_size:
            raise ValueError(
                'Thought data is of wrong size. '
                f'Got {len(data_bytes)}, expected {thought_size}')
        thought = cls.deserialize_data(data_bytes)

        # Return a new thought instance from deserialized information.
        return Thought(user_id, timestamp, thought)
