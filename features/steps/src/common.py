# -*- coding: utf-8 -*-
import executor


class IoC:
    def __init__(self):
        self.methods = {}

    def replace_all_methods(self, dict_functions):
        self.methods = dict_functions

    def resolve(self, key: str, *argv, **kwargs):
        '''
        отдаёт зависимость
        :param key: - название зависимости
        :param args:
        :return:
        '''
        return executor.Executor(self.methods[key], *argv, **kwargs)
