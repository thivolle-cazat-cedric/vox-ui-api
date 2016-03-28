# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)
from wtforms.fields import Field
from wtforms.widgets import TextInput


class ListField(Field):
    widget = TextInput()

    def __init__(self, label='', validators=None, remove_duplicates=True, **kwargs):
        super(ListField, self).__init__(label, validators, **kwargs)
        self.remove_duplicates = remove_duplicates

    def _value(self):
        if self.data:
            return ','.join(self.data)
        else:
            return ''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
        else:
            self.data = []

        if self.remove_duplicates:
            self.data = list(self._remove_duplicates(self.data))

    @staticmethod
    def _remove_duplicates(seq):
        """Remove duplicates in a case insensitive, but case preserving manner"""
        d = {}
        for item in seq:
            if item.lower() not in d:
                d[item.lower()] = True
                yield item