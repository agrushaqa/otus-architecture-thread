import threading
from io import StringIO
from unittest.mock import patch

from behave import given, then, when
from src.commands import TestConnectionError, TestEnvironmentError
from src.commands_queue import CommandsQueue
from src.create_class import create_command_instance


@given('queue')
def given_queue(context):
    context.command_queue = CommandsQueue()


@given('text ({text})')
def given_text(context, text):
    context.printed_text = text


@given('with ({command}) command')
def given_command(context, command):
    context.command = create_command_instance(command,
                                              context.printed_text)


@when('raise connection exception')
def when_connection_exception(context):
    context.command = TestConnectionError(context.command)


@when('raise environment exception')
def when_environment_exception(context):
    context.command = TestEnvironmentError(context.command)


@when('call')
def when_call(context):
    context.command_queue.add_command(context.command)
    with patch('sys.stdout', new=StringIO()) as fake_out:
        context.thread = threading.Thread(
            target=context.command_queue.commands_worker(),
            daemon=True)
        context.thread.start()
        context.output = fake_out


@then('print output')
def then_print_output(context):
    context.output.seek(0)
    print(context.output.read())


@then('execute (Log) {text_count} time')
def then_execute_log(context, text_count):
    context.output.seek(0)
    output = context.output.read()
    assert output.count(context.printed_text) == int(text_count)
    assert output.count(context.printed_text) == int(text_count)


@then('wait when finish queue')
def wait_all_tasks(context):
    context.command_queue.stop()
    context.thread.join(10)
