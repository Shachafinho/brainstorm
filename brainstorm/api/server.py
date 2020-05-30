import connexion
import flask_cors

from .resolver import DatabaseAwareResolver
from brainstorm.database import Database


_DEFAULT_SPECIFICATION_DIR = 'spec'
_SWAGGER_FILE = 'swagger.yaml'


def _create_app(database, specification_dir=None):
    specification_dir = specification_dir or _DEFAULT_SPECIFICATION_DIR
    app = connexion.App(__name__, specification_dir=specification_dir)

    resolver = DatabaseAwareResolver(database)
    app.add_api(_SWAGGER_FILE, resolver=resolver, validate_responses=True)

    # Add CORS support
    flask_cors.CORS(app.app)

    return app


def run_api_server(host, port, database_url):
    """Run a REST API server.

    The server listens on the specified host and port, and invokes the proper
    API endpoint upon receiving a request.

    Args:
        host (str): API server hostname to listen on.
        port (int): API server port to listen on.
        database_url (str): A URL representing the specific database to use.
          The scheme determines the type of the database (e.g.
          *postgresql*), whereas the host and port determine the address of
          the database.
    """
    app = _create_app(Database(database_url))
    app.run(host=host, port=port, debug=True)
