import pathlib

import flask
import furl.furl as furl


_APP_DIR = pathlib.Path(__file__).parent / 'app' / 'build'
_DEFAULT_STATIC_DIR = _APP_DIR / 'static'
_API_URL_PLACEHOLDER = '__API_URL__'


def _create_app(api_host, api_port):
    app = flask.Flask(__name__)
    app._static_folder = _DEFAULT_STATIC_DIR

    @app.route('/')
    @app.route('/index')
    def index():
        api_url = str(furl(scheme='http', host=api_host, port=api_port))
        with open(_APP_DIR / 'index.html') as index_file:
            return index_file.read().replace(_API_URL_PLACEHOLDER, api_url)

    return app


def run_server(host, port, api_host, api_port):
    """Run the GUI server.

    The server listens on the specified host and port, and reflects the API
    server running on the specified *api_host* and *api_port*.

    Args:
        host (str): GUI server hostname to listen on.
        port (int): GUI server port to listen on.
        api_host (str): API server hostname.
        api_port (int): API server port.
    """
    app = _create_app(api_host, api_port)
    app.run(host=host, port=port, debug=True)
