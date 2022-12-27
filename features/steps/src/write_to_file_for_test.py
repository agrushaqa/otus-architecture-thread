

class WriteToFileForTest:
    def execute(self, path, text):
        with open(path, 'w') as sample:
            print(text, file=sample)
