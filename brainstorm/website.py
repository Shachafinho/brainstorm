import functools

from http.server import ThreadingHTTPServer

from custom_http_request_handler import CustomHTTPRequestHandler


class Website:
    def __init__(self, path_handlers=None):
        self.path_handlers = path_handlers or []

    def route(self, path):
        def decorator(f):
            # Add function as a handler, according to the specified path.
            self.path_handlers.append((path, f))
            return f
        return decorator

    def run(self, address):
        # Parameterize the request handler's initializator.
        request_handler_cls = functools.partial(
            CustomHTTPRequestHandler, self.path_handlers)

        # Run the server.
        server = ThreadingHTTPServer(address, request_handler_cls)
        server.serve_forever()
