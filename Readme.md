[![Build Status](https://travis-ci.org/Shachafinho/brainstorm.svg?branch=master)](https://travis-ci.org/Shachafinho/brainstorm)
[![Coverage](https://codecov.io/gh/Shachafinho/brainstorm/branch/master/graph/badge.svg)](https://codecov.io/gh/Shachafinho/brainstorm)

# Brainstorm

See [full documentation](https://shachafinho-brainstorm.readthedocs.io/en/latest/).

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

See [full documentation](https://shachafinho-brainstorm.readthedocs.io/en/latest/).
