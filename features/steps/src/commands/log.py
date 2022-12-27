class Log:
    def __init__(self, cmd, exception=""):
        self.cmd = cmd
        self.exception = exception

    def execute(self):
        print(f"cmd:{self.cmd}")
        print("self.exception:")
        print(self.exception)
