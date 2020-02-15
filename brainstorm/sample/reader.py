from .reader_manager import reader_manager


class Reader:
    def __init__(self, path):
        reader_driver_class = reader_manager.find_reader(path)
        self.reader_driver = reader_driver_class(path)

    def __enter__(self):
        return self.reader_driver.__enter__()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        return self.reader_driver.__exit__(exc_type, exc_value, exc_traceback)


if __name__ == '__main__':
    path = '/home/user/Downloads/sample.mind'
    with Reader(path) as reader:
        print(reader.user_information)
        for snapshot in reader.snapshots:
            print(snapshot)
