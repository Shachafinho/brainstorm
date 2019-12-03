# Brainstorm

The main project for "Advanced System Design" course.\
It simulates a brainstorm in the sense that each user (client) can share (upload) his thoughts with the central server.\
A webserver is used to expose all of the shared thoughts, grouped by their owner.


## Installation

1. Clone the repository
```sh
$ git clone git@github.com:Shachafinho/brainstorm.git

...
$ cd brainstorm/
```

2. Run the installation script

```sh
$ ./scripts/install.sh
```

3. Activate the virtual environment

```sh
$ source .env/bin/activate
[brainstorm] $ # Environment has been activated
```

4. Verify everything works as intented by running the tests

```sh
$ pytest tests/
```


## Basic Usage

The `brainstorm` package provides the following classes:

* `Thought`

    This class represents a user's message at some given time.

    It is used mostly to hold data, and can be serialized and deserialized:

    ```python
    >>> import datetime as dt
    >>> from brainstorm import Thought
    >>> thought = Thought(user_id=1, timestamp=dt.datetime.now(), thought='Hello world')
    >>> thought.serialize()
    b'\x01\x00\x00\x00\x00\x00\x00\x00\x??\x??\x??\x??\x??\x??\x??\x??\x0b\x00\x00\x00Hello world'
    >>> Thought.deserialize(_)
    Thought(user_id=1, timestamp=datetime.datetime(...), thought='Hello world')
    ```

The `brainstorm` package also provides the following functions, which can be invoked via CLI as well:

* `run_server`

    Run the centralized thoughts server, which accepts and records users' thoughts.

    CLI invocation:

    ```sh
    $ python -m brainstorm run-server [-a <address>] [-d <data_directory>]
    # Server awaits clients' requests...
    ```

    For example, if we wish the server to listen on 127.0.0.1 port 5555, and store incoming thoughts in `data_directory`, we run:

    ```sh
    $ python -m brainstorm run-server -a 127.0.0.1 5555 -d data_directory
    ```

* `run_webserver`

    Run the webserver at a given address, bound to a specified thoughts data directory.

    The webserver showcases all users in the system, each with its own collection of thoughts.

    CLI invocation:

    ```sh
    python -m brainstorm run-webserver [-a <address>] [-d <data_directory>]
    ```

    For example, if we wish the server to listen on 127.0.0.1 port 8888, and expose users' thoughts stored in `data_directory`, we run:

    ```sh
    $ python -m brainstorm run-webserver -a 127.0.0.1 8888 -d data_directory
    ```

* `upload_thought`

    Send a user's thought to the server.

    CLI invocation:

    ```sh
    python -m brainstorm upload-thought [-a <address>] -u <user_id> -t <thought>
    ```

    For example, if we wish to send *Hello world* by user *1* to the server at 127.0.0.1 port 5555, we run:

    ```sh
    $ python -m brainstorm upload-thought -a 127.0.0.1 5555 -u 1 -t "Hello world"
    ```
