"""
The client exposes the following API:

.. code-block:: python

    >>> from brainstorm.client import upload_sample
    >>> upload_sample(
    ...     host='127.0.0.1',
    ...     port=8000,
    ...     path='protobuf://path/to/sample.mind.gz'
    ... )
    ... # upload path to host:port

It also provides the following CLI:

.. code-block:: sh

    $ python -m brainstorm.client upload-sample \\
        -h/--host '127.0.0.1' \\
        -p/--port 8000 \\
        'protobuf://path/to/sample.mind.gz'
"""

from .client import upload_sample


__all__ = ['upload_sample']
