import functools

from datetime import datetime
from http.server import HTTPStatus
from pathlib import Path

from cli import CommandLineInterface
from website import Website


INDEX_PAGE_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface</title>
    </head>
    <body>
        <ul>
            {user_lines}
        </ul>
    </body>
</html>
'''

USER_LINE_HTML = '''
<li>
    <a href="/users/{user_id}">user {user_id}</a>
</li>
'''

USER_PAGE_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface: User {user_id}</title>
    </head>
    <body>
        <table>
            {thought_lines}
        </table>
    </body>
</html>
'''

THOUGHT_LINE_HTML = '''
<tr>
    <td>{timestamp}</td>
    <td>{thought}</td>
</tr>
'''


cli = CommandLineInterface()


@cli.command
def run_webserver(address, data_dir):
    website = Website()


    # Add website handlers.

    @website.route('/')
    def handle_index_page():
        # Obtain all users in the system.
        users = [user_dir.name for user_dir in Path(data_dir).iterdir()
                 if not user_dir.name.startswith('.')]

        # Generate an html line for each user.
        user_lines_html = sorted(
            [USER_LINE_HTML.format(user_id=user) for user in users])

        # Construct the index html page using the user lines.
        index_page_html = \
            INDEX_PAGE_HTML.format(user_lines='\n'.join(user_lines_html))

        # Return the generated page.
        return HTTPStatus.OK, index_page_html


    @website.route('/users/([0-9]+)')
    def handle_user_page(user_id):
        user_dir = Path(data_dir).joinpath(str(user_id))

        # Obtain all user's thoughts.
        thought_lines_html = []
        for thought_file in user_dir.iterdir():
            # Thought file's name represents the timestamp, but its format
            # must be reconfigured.
            datetime_obj = \
                datetime.strptime(thought_file.stem, '%Y-%m-%d_%H-%M-%S')
            datetime_str = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

            # Read the file to collect its thoughts.
            thought = thought_file.read_text()

            # Add the current thought to the collection.
            thought_lines_html.append(THOUGHT_LINE_HTML.format(
                timestamp=datetime_str, thought=thought))

        # Sort the lines for convenience.
        thought_lines_html = sorted(thought_lines_html)

        # Construct the user html page using the thought lines.
        user_page_html = USER_PAGE_HTML.format(
            user_id=user_id, thought_lines='\n'.join(thought_lines_html))

        # Return the generated page.
        return HTTPStatus.OK, user_page_html


    # Run the website.
    ip, port = address.split(':')
    website.run((ip, int(port)))


def main(argv):
    if len(argv) != 3:
        print(f'USAGE: {argv[0]} <ip_address:port> <data_dir>')
        return 1
    try:
        ip, port = argv[1].split(':')
        address = (ip, int(port))

        run_webserver(address, argv[2])
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    cli.main()
