import construct
import socket


_DEFAULT_CHUNK_SIZE = 2048


class Connection:
    Message = construct.PrefixedArray(
        construct.Int32ul, construct.Byte).compile()

    def __init__(self, socket):
        self.socket = socket

    def __repr__(self):
        class_name = self.__class__.__name__

        src_addr = self.socket.getsockname()
        dst_addr = self.socket.getpeername()
        src_addr_str = '{addr[0]}:{addr[1]}'.format(addr=src_addr)
        dst_addr_str = '{addr[0]}:{addr[1]}'.format(addr=dst_addr)

        return f'<{class_name} from {src_addr_str} to {dst_addr_str}>'

    def send(self, data, chunk_max_size=None):
        chunk_max_size = chunk_max_size or _DEFAULT_CHUNK_SIZE

        total_bytes_sent = 0
        while total_bytes_sent < len(data):
            bytes_to_send = min(chunk_max_size, len(data) - total_bytes_sent)
            bytes_sent = self.socket.send(
                data[total_bytes_sent:total_bytes_sent + bytes_to_send])
            total_bytes_sent += bytes_sent
        return total_bytes_sent

    def receive(self, size, chunk_max_size=None):
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
        message_bytes = self.Message.build(data)
        self.send(message_bytes)

    def receive_message(self):
        size_field = construct.Int32ul
        msg_size = size_field.parse(self.receive(size_field.sizeof()))
        return self.receive(msg_size)

    def close(self):
        self.socket.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    @classmethod
    def connect(cls, host, port):
        return cls(socket.create_connection((host, port)))
