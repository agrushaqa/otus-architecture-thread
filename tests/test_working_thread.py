import os.path

import features.steps.src.write_to_file_for_test as write_to_file_for_test
from features.steps.src.commands.start_working_thread import (
    StartWorkingThread, ThreadConfig)
from features.steps.src.ioc.common import IoC
from features.steps.src.ioc_working_thread import WorkingThread
from features.steps.src.scope import Scopes


class TestWorkingThread:

    def test_parallel_write_file_to_text(self, mkdir_tmp_if_not_exist):
        path = os.path.join(mkdir_tmp_if_not_exist, 'samplefile.txt')

        def mytask(ioc):
            a = write_to_file_for_test.WriteToFileForTest
            ioc.resolve(key="IoC.register",
                        registered_name="MyScope",
                        called_method=a).execute()
            ioc.resolve("MyScope", path, "34").execute().execute()

        thread = WorkingThread(target=mytask, scope=Scopes(), ioc=IoC())
        thread.start()
        thread.join()
        with open(path, 'r') as f:
            content = f.read()
        os.remove(path)
        assert content == "34\n"

    def test_write_file_to_text(self, mkdir_tmp_if_not_exist):
        path = os.path.join(mkdir_tmp_if_not_exist, 'samplefile1.txt')
        a = write_to_file_for_test.WriteToFileForTest(path, "34")
        a.execute()
        with open(path, 'r') as f:
            content = f.read()
        os.remove(path)
        assert content == "34\n"

    def test_command_thread(self, mkdir_tmp_if_not_exist):
        path = os.path.join(mkdir_tmp_if_not_exist, 'test_command_thread.txt')

        def mytask(ioc):
            a = write_to_file_for_test.WriteToFileForTest
            ioc.resolve(key="IoC.register",
                        registered_name="MyScope",
                        called_method=a).execute()
            ioc.resolve("MyScope", path, "54").execute().execute()

        ioc = IoC()
        scope = Scopes()
        thread_config = ThreadConfig()
        thread_config.set_ioc(ioc)
        thread_config.set_scope(scope)
        thread_config.set_task(mytask)
        scope.current(ioc)
        ioc.resolve(key="IoC.register",
                    registered_name="StartThreadCommand",
                    called_method=StartWorkingThread).execute()
        ioc.resolve("StartThreadCommand", thread_config).execute().execute()
        with open(path, 'r') as f:
            content = f.read()
        os.remove(path)
        assert content == "54\n"
