import construct
import socket


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

    def send(self, data):
        self.socket.sendall(data)

    def receive(self, size):
        chunks = []
        total_received_bytes = 0
        while total_received_bytes < size:
            chunk = self.socket.recv(size - total_received_bytes)
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
