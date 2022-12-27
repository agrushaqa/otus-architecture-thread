class PrintCmd:
    def __init__(self, cmd, exception=""):
        self.cmd = cmd

    def execute(self):
        print(self.cmd)
