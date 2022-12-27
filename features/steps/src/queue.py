import queue


class Queue:
    def __init__(self):
        self.q = queue.Queue()

    def get(self):
        value = self.q.get()

        return value

    def task_done(self):
        self.q.task_done()

    def put(self, value):
        self.q.put(value)
