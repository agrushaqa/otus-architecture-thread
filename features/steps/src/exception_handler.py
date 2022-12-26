from src.cmd_graph import get_target_method


def exception_handler(queue, cmd, ex):
    action = get_target_method(cmd, ex)
    queue.put(action)
