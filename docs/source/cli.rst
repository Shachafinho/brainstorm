Brainstorm CLI Reference
========================

The ``brainstorm`` package provides the following command-line interface:

The ``run-server`` Command
--------------------------

The ``run-server`` command setups the central server,
which accepts and records users' thoughts.

.. code:: bash

    $ python -m brainstorm run-server [-a <address>] [-d <data_directory>]

The ``run-webserver`` Command
-----------------------------

The ``run-webserver`` command setups the web server,
which showcases users and their thoughts.

.. code:: bash

    $ python -m brainstorm run-webserver [-a <address>] [-d <data_directory>]

The ``upload-thought`` Command
------------------------------

The ``upload-thought`` command sends the user's thought to the central server.

.. code:: bash

    $python -m brainstorm upload-thought [-a <address>] -u <user_id> -t <thought>
