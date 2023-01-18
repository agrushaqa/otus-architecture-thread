class OneCommand:
    def __init__(self, cmd, exception=""):
        self.cmd = cmd
        self.exception = exception

    def execute(self):
        str_cmd = self.cmd.__class__.__name__
        str_exception = str(type(self.exception))
        print(f"{str_cmd} complete with exception {str_exception}")
        self.cmd.execute()
