from threading import local
from threading import Thread
from scope import Scopes
from common import IoC

data = local()


class WorkingThread(Thread):
    def init_ioc(self):
        data.scope = Scopes()
        data.ioc = IoC()
        data.scope.current(data.ioc)

    def run(self):
        data.thread_name = self.name
        self.init_ioc()
        self._target(data, *self._args, **self._kwargs)
