import threading

from commands_queue import CommandsQueue

# используется только для обратной совместимости
if __name__ == '__main':
    # Turn-on the worker thread.
    command = CommandsQueue()
    threading.Thread(target=command.commands_worker(), daemon=True).start()
