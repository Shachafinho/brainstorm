import construct
import socket


_DEFAULT_CHUNK_SIZE = 2048


class Connection:
    """An object responsible for sending and receiving both data and messages.

    This object accepts a socket and nicely wraps some of its basic
    functionality.
    """

    Message = construct.PrefixedArray(
        construct.Int32ul, construct.Byte).compile()
    """A message object to be parse and build data."""

    def __init__(self, socket):
        """Construct a Connection object.

        Args:
            socket (:class:`socket.socket`): The underlying socket to wrap.
        """
        self.socket = socket

    def __repr__(self):
        class_name = self.__class__.__name__

        src_addr = self.socket.getsockname()
        dst_addr = self.socket.getpeername()
        src_addr_str = '{addr[0]}:{addr[1]}'.format(addr=src_addr)
        dst_addr_str = '{addr[0]}:{addr[1]}'.format(addr=dst_addr)

        return f'<{class_name} from {src_addr_str} to {dst_addr_str}>'

    def send(self, data, chunk_max_size=None):
        """Send the given data over the underlying socket.

        Args:
            data (bytes): The data to send.
            chunk_max_size (int): Maximum number of bytes to be sent in each
              chunk.

        Return:
            int: The total number of bytes sent.
        """
        chunk_max_size = chunk_max_size or _DEFAULT_CHUNK_SIZE

        total_bytes_sent = 0
        while total_bytes_sent < len(data):
            bytes_to_send = min(chunk_max_size, len(data) - total_bytes_sent)
            bytes_sent = self.socket.send(
                data[total_bytes_sent:total_bytes_sent + bytes_to_send])
            total_bytes_sent += bytes_sent
        return total_bytes_sent

    def receive(self, size, chunk_max_size=None):
        """Receive the data of given size from the underlying socket.

        Args:
            size (int): The size of the data to receive.
            chunk_max_size (int): Maximum number of bytes to be received in
              each chunk.

        Return:
            bytes: The received data.
        """
        chunk_max_size = chunk_max_size or _DEFAULT_CHUNK_SIZE

        chunks = []
        total_received_bytes = 0
        while total_received_bytes < size:
            chunk = self.socket.recv(
                min(size - total_received_bytes, chunk_max_size))
            if not chunk:
                raise ConnectionAbortedError()
            chunks.append(chunk)
            total_received_bytes += len(chunk)
        return b''.join(chunks)

    def send_message(self, data):
        """Send a message cotaining the given data over the underlying socket.

        Args:
            data (bytes): The data to send.
        """
        message_bytes = self.Message.build(data)
        self.send(message_bytes)

    def receive_message(self):
        """Receive a message from the underlying socket.

        Return:
            bytes: The received message data.
        """
        size_field = construct.Int32ul
        msg_size = size_field.parse(self.receive(size_field.sizeof()))
        return self.receive(msg_size)

    def close(self):
        """Close the underlying socket."""
        self.socket.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    @classmethod
    def connect(cls, host, port):
        """Construct a Connection object, connected to the given host and port.

        Args:
            host (str): The hostname to connect to.
            port (int): The port to connect to.

        Return:
            :class:`~brainstorm.utils.Connection`:
              The constructed Connection object.
        """
        return cls(socket.create_connection((host, port)))
