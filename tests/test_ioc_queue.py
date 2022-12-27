import sqlite3
import time
from datetime import datetime
from threading import active_count

from loguru import logger

from features.steps.src.create_class import create_command_instance
from features.steps.src.ioc_commands_queue import IocCommandQueue
from features.steps.src.ioc_working_thread import WorkingThread
from features.steps.src.mysql import (delete_table, list_tables_in_db,
                                      read_all_results)


class TestIocThread:

    def test_thread_without_ioc(self):
        assert active_count() == 1
        context_command_queue1 = IocCommandQueue()
        thread = WorkingThread(
            target=context_command_queue1.commands_worker,
            daemon=True)
        thread.start()
        assert active_count() == 2
        context_command_queue1.add_command(context_command_queue1.stop())
        thread.join()
        assert active_count() == 1

    def test_thread_ioc_hard_stop(self):
        assert active_count() == 1
        context_command_queue1 = IocCommandQueue()
        thread = WorkingThread(
            target=context_command_queue1.commands_worker,
            daemon=True)
        context_command_queue1.register_ioc_command(
            "HardStop", context_command_queue1.stop)
        thread.start()
        assert active_count() == 2
        context_command_queue1.add_ioc_command("HardStop")
        thread.join()
        assert active_count() == 1

    def test_thread_ioc_soft_stop(self):
        assert active_count() == 1
        command_queue1 = IocCommandQueue()
        thread = WorkingThread(
            target=command_queue1.commands_worker,
            daemon=True)
        command_queue1.register_ioc_command("SoftStop",
                                            command_queue1.soft_stop)
        thread.start()
        assert active_count() == 2
        command_queue1.add_ioc_command("SoftStop")
        thread.join()
        assert active_count() == 1

    def test_thread_ioc_soft_stop_with_command(self):
        start_time = time.time()
        table_name = f"grusha{datetime.now().strftime('%d%m%Y_%H_%M_%S')}"
        conn = sqlite3.connect("test_mysql_db_26122022.db",
                               isolation_level=None)
        db_cursor = conn.cursor()
        list_tables_in_db(db_cursor)
        # list_tables_before = read_all_results(db_cursor)
        context_command = create_command_instance(
            "MysqlDbCreate",
            "test_mysql_db_26122022.db",
            f'CREATE TABLE IF NOT EXISTS {table_name} '
            f"(ID INTEGER PRIMARY KEY AUTOINCREMENT,"
            f" URL CHAR(2048),"
            f" REQUEST_TIME INTEGER);"
        )
        command_queue1 = IocCommandQueue()
        thread = WorkingThread(
            target=command_queue1.commands_worker,
            daemon=True)
        command_queue1.register_ioc_command("SoftStop",
                                            command_queue1.soft_stop)
        command_queue1.register_ioc_command("Sleep", time.sleep)
        thread.start()
        command_queue1.add_command(context_command)
        command_queue1.add_ioc_command("SoftStop")
        command_queue1.add_ioc_command("Sleep", 12)
        thread.join()
        delete_table(conn, table_name)

        # result = read_all_results(db_cursor)
        # assert result == [('sqlite_sequence',), ]
        # assert result == list_tables_before.append((table_name,))
        conn.close()
        end_time = time.time()
        assert 30 > end_time - start_time > 12

    def test_thread_ioc_hard_stop_with_command(self):
        start_time = time.time()
        context_command_queue1 = IocCommandQueue()
        thread = WorkingThread(
            target=context_command_queue1.commands_worker,
            daemon=True)
        context_command_queue1.register_ioc_command("HardStop",
                                                    context_command_queue1.stop
                                                    )
        context_command_queue1.register_ioc_command("Sleep", time.sleep)
        thread.start()
        context_command_queue1.add_ioc_command("HardStop")
        context_command_queue1.add_ioc_command("Sleep", 12)
        thread.join()
        end_time = time.time()
        timespend = end_time - start_time
        logger.info(timespend)
        assert timespend < 12
