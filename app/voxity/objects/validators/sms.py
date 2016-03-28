# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)
from wtforms.validators import ValidationError
import re

TEL_REG = re.compile('^0[67]\d{8}$')


class PhoneNumberList(object):
    """
    :param str message:
        Error message to raise in case of a validation error. Can be
        interpolated with `%(other_label)s` and `%(other_name)s` to provide a
        more helpful error.
    """

    def __init__(self, message=None):
        self.message = message or "Format error"

    def __call__(self, form, field):
        if isinstance(field.data, list):
            for num in field.data:
                if not TEL_REG.match(num):
                    raise ValidationError(self.message)
