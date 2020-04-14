import connexion
import flask

from .resolver import DatabaseAwareResolver
from brainstorm.database import Database


DEFAULT_SPECIFICATION_DIR = 'spec'
SWAGGER_FILE = 'swagger.yaml'


def create_app(database, specification_dir=None):
    specification_dir = specification_dir or DEFAULT_SPECIFICATION_DIR
    app = connexion.App(__name__, specification_dir=specification_dir)

    resolver = DatabaseAwareResolver(database)
    app.add_api(SWAGGER_FILE, resolver=resolver, validate_responses=True)

    return app


def run_api_server(host, port, database_url):
    app = create_app(Database(database_url))
    app.run(host=host, port=port, debug=True)
