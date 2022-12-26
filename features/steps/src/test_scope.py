# -*- coding: utf-8 -*-
# import allure
# import pytest
import common
import print_for_test
from scope import Scopes


class TestScope:
    def test_register_exists_in_scope_by_default(self):
        scopes = Scopes()
        assert "IoC.register" in scopes.content["main"]

    def test_ioc_register(self, capsys):
        ioc = common.IoC()
        scopes = Scopes()
        scopes.current(ioc)
        a = print_for_test.PrintForTest()
        ioc.resolve(key="IoC.register", registered_name="MyScope",
                    called_method=a.current).execute()
        ioc.resolve("MyScope", "34", 88).execute()
        captured = capsys.readouterr()
        assert captured.out == "34\n88\n"
