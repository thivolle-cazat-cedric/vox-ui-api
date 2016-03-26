# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)
from wtforms.validators import ValidationError, StopValidation
import re

SHORTCUT_TEL_REG = re.compile('^\*\d{2,6}$')


class ShortcutTelFormat(object):
    """
    :param str message:
        Error message to raise in case of a validation error. Can be
        interpolated with `%(other_label)s` and `%(other_name)s` to provide a
        more helpful error.
    """

    def __init__(self, message=None, strip_whitespace=True):
        self.message = message or "Format error"
        self.strip_whitespace = strip_whitespace

    def __call__(self, form, field):
        data = field.data
        if not data:
            data = ''
        if data and self.strip_whitespace:
            data = data.strip()

        if not SHORTCUT_TEL_REG.match(data):
            raise ValidationError(self.message)
