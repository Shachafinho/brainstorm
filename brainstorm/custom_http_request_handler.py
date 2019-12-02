import http.server
import re


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, path_handlers, *args, **kwargs):
        self.path_handlers = path_handlers
        super().__init__(*args, **kwargs)

    def send_html(self, status_code, html_body):
        # Send response headers.
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(html_body))
        self.end_headers()

        # Send response contents.
        self.wfile.write(html_body.encode())

    def do_GET(self):
        for path_regex, handler in self.path_handlers:
            # Match regex perfectly against path.
            match = re.match(f'^{path_regex}$', self.path)
            if match:
                # Invoke the corresponding handler with the matched groups,
                # and return its response.
                status_code, html_body = handler(*match.groups())
                self.send_html(status_code, html_body)
                return

        # Errors default to 404 with no data.
        self.send_html(http.server.HTTPStatus.NOT_FOUND, '')
