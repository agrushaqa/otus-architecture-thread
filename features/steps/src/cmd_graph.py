import json
import os

from src.create_class import create_command_instance


def get_json_content():
    path = os.path.abspath(os.path.dirname(__file__))
    f = open(os.path.join(path, 'cmd_graph.json'))
    data = json.load(f)
    f.close()
    return data


def get_target_method(cmd, ex):
    str_cmd = cmd.__class__.__name__
    str_exception = str(type(ex))
    json_content = get_json_content()
    for i_list_cmd in json_content:
        if i_list_cmd['from']['class'] == str_cmd:
            if i_list_cmd['exception'] == str_exception:
                instance = create_command_instance(
                                       i_list_cmd['to']["class"],
                                       cmd, ex)
                return instance
    raise Exception(f'Not_found_{str_cmd}_{str_exception}')
