import datetime as dt
import pathlib

import flask

from brainstorm import Thought


def run_webserver(address, data_dir):
    website = flask.Flask(__name__)

    @website.route('/')
    @website.route('/index')
    def index():
        # Obtain all users in the system.
        directory_iterator = pathlib.Path(data_dir).iterdir()
        users_ids = sorted([user_dir.name for user_dir in directory_iterator
                            if not user_dir.name.startswith('.')])

        return flask.render_template('index.html', users_ids=users_ids)

    @website.route('/users/<int:user_id>')
    def user(user_id):
        user_dir = pathlib.Path(data_dir).joinpath(str(user_id))

        if not user_dir.exists():
            flask.abort(404)

        # Obtain all user's thoughts.
        thoughts = []
        for thought_file in user_dir.iterdir():
            # Thought file's name represents the timestamp, but its format
            # must be reconfigured. File's content is the thought message.
            timestamp = \
                dt.datetime.strptime(thought_file.stem, '%Y-%m-%d_%H-%M-%S')
            thought_message = thought_file.read_text()

            thoughts.append(Thought(user_id, timestamp, thought_message))

        thoughts = sorted(thoughts)

        return flask.render_template(
            'user.html', user_id=user_id, thoughts=thoughts)

    website.run(host=address[0], port=address[1])
