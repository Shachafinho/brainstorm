import pathlib

import flask


@flask.current_app.route('/')
@flask.current_app.route('/index')
def index():
    # Obtain all users in the system.
    users_ids = [user_dir.name for user_dir in pathlib.Path(data_dir).iterdir()
                 if not user_dir.name.startswith('.')]

    return flask.render_template('index.html', users_ids=users_ids)
