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

* `run_webserver`

    Run the webserver at a given address, bound to a specified thoughts data directory.

    The webserver showcases all users in the system, each with its own collection of thoughts.

* `upload_thought`

    Send a user's thought to the server.
