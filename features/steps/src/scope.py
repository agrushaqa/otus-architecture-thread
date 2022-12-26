# -*- coding: utf-8 -*-
from common import IoC


class Scopes:
    content = {}

    def __init__(self, default_scope='main'):
        self.default_scope = default_scope
        self._set(default_scope, {})
        self._add_method_to_current_scope("IoC.register", self.register)

    def get_name_default_scope(self) -> str:
        return self.default_scope

    def new_clean_existing(self, scope_id: str) -> dict:
        self._set(scope_id, {})
        return self._get(scope_id)

    def set_current(self, scope_id: str) -> dict:
        self.default_scope = scope_id
        return self._get(self.default_scope)

    def current(self, linked_ioc: IoC) -> None:
        linked_ioc.replace_all_methods(self.get_current())

    def get_current(self) -> dict:
        return self._get(self.default_scope)

    def _get(self, scope_id) -> dict:
        return self.content[scope_id]

    def _set(self, scope_id: str, scope: str) -> None:
        self.content[scope_id] = scope

    def add(self, scope: str):
        '''
        Для наследования scope
        :param scope:
        :return:
        '''
        current_scope = self.get_current()
        self.set_current(scope.update(current_scope))

    def register(self, registered_name: str, called_method: str):
        self._add_method_to_current_scope(registered_name, called_method)

    def _add_method_to_current_scope(self, registered_name: str,
                                     called_method: str):
        self.content[self.default_scope][registered_name] = called_method
