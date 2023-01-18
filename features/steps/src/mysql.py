import logging
import sqlite3
import sys

# https://docs.python.org/3.8/library/sqlite3.html


def sqlite_send_request(connection, request: str, params=""):
    try:
        log = logging.getLogger(__name__)
        log.debug(f"start {sys._getframe().f_code.co_name}")
        log.debug(request)
        log.debug(params)
        connection.execute(request, params)
        log.debug(f"finish {sys._getframe().f_code.co_name}")
    except Exception as e:
        log.exception(request)
        log.exception(params)
        log.exception("Error at %s", "division", exc_info=e)


def sqlite_send_requests(connection, request: str, params):
    try:
        log = logging.getLogger(__name__)
        log.debug(f"start {sys._getframe().f_code.co_name}")
        connection.executemany(request, params)
        log.debug(request)
        log.debug(f"finish {sys._getframe().f_code.co_name}")
    except sqlite3.OperationalError:
        log.exception("request")


def create_table(connection, request: str):
    sqlite_send_request(
        connection,
        request
    )


def delete_table(connection, name: str):
    sqlite_send_request(connection, f'DROP TABLE IF EXISTS "{name}"')


def list_tables_in_db(connection):
    sqlite_send_request(
        connection, "SELECT name FROM sqlite_master WHERE type='table';"
    )


def read_all_results(cursor):
    return cursor.fetchall()


def read_one_string_from_result(cursor):
    return cursor.fetchone()
