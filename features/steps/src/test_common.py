# import allure
# import pytest
import common
import print_for_test


class TestCommon:

    def test_resolve(self, capsys):
        list_functions = {}
        list_functions["PrintForTest.current"] = (
            print_for_test.PrintForTest.current
        )

        ioc = common.IoC()
        ioc.replace_all_methods(list_functions)
        ioc.resolve("PrintForTest.current",
                    print_for_test.PrintForTest, "34", 88).execute()
        captured = capsys.readouterr()
        assert captured.out == "34\n88\n"

    def test_call_method_with_class_in_attrib(self, capsys):
        print_for_test.PrintForTest.current(print_for_test.PrintForTest,
                                            "34",
                                            88)
        captured = capsys.readouterr()
        assert captured.out == "34\n88\n"
