def create_instance(module_name, class_name, *args, **kwargs):
    module_meta = __import__(module_name, globals(), locals(), [class_name])
    class_meta = getattr(module_meta, class_name)
    obj = class_meta(*args, **kwargs)
    return obj


def create_command_instance(class_name, *args, **kwargs):
    return create_instance("features.steps.src.commands", class_name, *args,
                           **kwargs)
    # TODO Заменить "features.steps.src.commands"
