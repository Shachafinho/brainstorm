import socket

from brainstorm.utils import Connection


class Listener:
    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr

        self.socket = socket.socket()
        if self.reuseaddr:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))

    def __repr__(self):
        class_name = self.__class__.__name__
        port, host, backlog, reuseaddr = \
            self.port, self.host, self.backlog, self.reuseaddr
        return f'{class_name}({port=}, {host=}, {backlog=}, {reuseaddr=})'

    def start(self):
        self.socket.listen(self.backlog)

    def stop(self):
        self.socket.close()

    def accept(self):
        conn_socket, _ = self.socket.accept()
        return Connection(conn_socket)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exce_type, exc_value, exc_traceback):
        self.stop()
