from working_thread import WorkingThread
import write_to_file_for_test
import os.path
from pathlib import Path


class TestWorkingThread:

    def test_parallel_write_file_to_text(self):
        BASE_DIR = Path(__file__).resolve().parent
        path = os.path.join(BASE_DIR, "tmp", 'samplefile.txt')

        def mytask(mydata):
            a = write_to_file_for_test.WriteToFileForTest()
            mydata.ioc.resolve(key="IoC.register", registered_name="MyScope",
                               called_method=a.execute).execute()
            mydata.ioc.resolve("MyScope", path, "34").execute()

        thread = WorkingThread(target=mytask)
        thread.start()
        thread.join()
        with open(path, 'r') as f:
            content = f.read()
        os.remove(path)
        assert content == "34\n"

    def test_write_file_to_text(self):
        BASE_DIR = Path(__file__).resolve().parent
        path = os.path.join(BASE_DIR, "tmp", 'samplefile.txt')
        a = write_to_file_for_test.WriteToFileForTest()
        a.execute(path, "34")
        with open(path, 'r') as f:
            content = f.read()
        os.remove(path)
        assert content == "34\n"
