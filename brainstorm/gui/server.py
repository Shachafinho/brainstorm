import datetime as dt
import pathlib

import flask
import furl.furl as furl


_DEFAULT_STATIC_DIR = pathlib.Path(__file__).parent / 'static'


def create_app(api_host, api_port):
    app = flask.Flask(__name__)
    app._static_folder = _DEFAULT_STATIC_DIR

    @app.route('/')
    @app.route('/index')
    def index():
        api_url = furl(scheme="http", host=api_host, port=api_port)
        return flask.render_template(
            'index.html', title='index', api_url=str(api_url))

    return app


def run_server(host, port, api_host, api_port):
    app = create_app(api_host, api_port)
    app.run(host=host, port=port, debug=True)
