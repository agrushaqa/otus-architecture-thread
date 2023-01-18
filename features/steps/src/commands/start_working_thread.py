from features.steps.src.commands.command import Command
from features.steps.src.ioc_working_thread import WorkingThread


class ThreadConfig:
    def __init__(self):
        self.scope = None
        self.ioc = None
        self.mytask = None

    def get_scope(self):
        return self.scope

    def get_ioc(self):
        return self.ioc

    def set_scope(self, scope):
        self.scope = scope

    def set_ioc(self, ioc):
        self.ioc = ioc

    def get_task(self):
        return self.mytask

    def set_task(self, mytask):
        self.mytask = mytask


class StartWorkingThread(Command):
    def __init__(self, thread_config):
        self.thread_config = thread_config

    def execute(self):
        thread = WorkingThread(target=self.thread_config.get_task(),
                               scope=self.thread_config.get_scope(),
                               ioc=self.thread_config.get_ioc())
        thread.start()
        thread.join()
