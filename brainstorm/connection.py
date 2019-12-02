import socket


class Connection:
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
        total_received_bytes = b''
        while len(total_received_bytes) < size:
            received_bytes = self.socket.recv(size - len(total_received_bytes))
            if not received_bytes:
                raise ConnectionAbortedError()
            total_received_bytes += received_bytes
        return total_received_bytes

    def close(self):
        self.socket.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    @classmethod
    def connect(cls, host, port):
        return cls(socket.create_connection((host, port)))
