from threading import Thread, local

from features.steps.src.ioc.common import IoC
from features.steps.src.scope import Scopes

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
