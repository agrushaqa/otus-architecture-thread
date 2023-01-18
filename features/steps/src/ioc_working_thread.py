from threading import Thread, local

from features.steps.src.ioc.common import IoC
from features.steps.src.scope import Scopes

data = local()


class WorkingThread(Thread):
    def __init__(self, target, scope, ioc):
        super().__init__(target=target)
        self.scope = scope
        self.ioc = ioc

    def init_ioc(self):
        initialized = getattr(data, 'initialized', None)
        if initialized is None:
            self.scope.current(self.ioc)
            data.initialized = True

    def run(self):
        self.thread_name = self.name
        self.init_ioc()
        self._target(self.get_ioc(), *self._args, **self._kwargs)

    def get_scope(self):
        try:
            return self.scope
        except Exception:
            return None

    def get_ioc(self):
        try:
            return self.ioc
        except Exception:
            return None
