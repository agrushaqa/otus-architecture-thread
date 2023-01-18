

class WriteToFileForTest:
    def __init__(self, path, text):
        self.path = path
        self.text = text

    def execute(self):
        with open(self.path, 'w') as sample:
            print(self.text, file=sample)
