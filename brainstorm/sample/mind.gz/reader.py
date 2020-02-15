import contextlib


class Reader:
    def __init__(self, path):
        self.path = path
        self.user_information = self._read_user_information()

    def __enter__(self):
        # TODO
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # TODO
        pass

    def _read_user_information(self):
        # TODO
        pass

    def _read_snapshot(self):
        # TODO
        pass

    @property
    def snapshots(self):
        with contextlib.suppress(StopIteration):
            while True:
                yield self._read_snapshot()


if __name__ == '__main__':
    path = '/home/user/Downloads/sample.mind.gz'
    with Reader(path) as reader:
        print(reader.user_information)
        for snapshot in reader.snapshots:
            print(snapshot)
