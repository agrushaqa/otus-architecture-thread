class Executor:
    def __init__(self, method, *argv, **kwargs):
        self.method = method
        self._argv = argv
        self._kwargs = kwargs

    def execute(self):
        return self.method(*self._argv, **self._kwargs)
