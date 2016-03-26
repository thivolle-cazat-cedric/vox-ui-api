# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)
from wtforms.form import Form
from wtforms.validators import ValidationError, StopValidation
import re


TEL_REG = re.compile('^(\+\d{2}|\d)([\ -_.\/]?\d){2,14}$')


class BaseForm(Form):
    """docstring for baseForm"""

    def strip_value(self):
        for field in self._fields:
            try:
                self._fields[field.name].data = field.data.strip()
            except Exception:
                pass


    def to_dict(self):
        return {self[f].name: self[f].data for f in self._fields}

    def get_object(self, object_class):
        return object_class(**self.to_dict())


class MandatoryOrOther(object):
    """
    :param str fieldname: The name of the other field to compare to.
    :param str message:
        Error message to raise in case of a validation error. Can be
        interpolated with `%(other_label)s` and `%(other_name)s` to provide a
        more helpful error.
    """

    def __init__(self, fieldname, message=None, strip_whitespace=True):
        self.fieldname = fieldname
        self.message = message or "Mandatory field."
        self.strip_whitespace = strip_whitespace

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError("Invalid field name {0}.".format(
                self.fieldname
            ))
        if not other.data and not field.data:
            raise StopValidation(self.message)

        if self.strip_whitespace:
            if (other.data and not bool(other.data.strip())) and (field.data and not bool(field.data.strip())):
                raise StopValidation(self.message)
        else:
            if not bool(other.data) and not bool(field.data):
                raise StopValidation(self.message)


class PhoneNumberFormat(object):
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

        if data and not TEL_REG.match(data):
            raise ValidationError(self.message)


class MandatoryIfField(object):
    """
    :param str fieldname: The name of the other field to compare to.
    :param str message:
        Error message to raise in case of a validation error. Can be
        interpolated with `%(other_label)s` and `%(other_name)s` to provide a
        more helpful error.
    """

    def __init__(self, fieldname, message=None, strip_whitespace=True):
        self.fieldname = fieldname
        self.message = message or "Mandatory field"
        self.strip_whitespace = strip_whitespace

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError("Invalid field name {0}.".format(
                self.fieldname
            ))

        if self.strip_whitespace and other.data:
            data = other.data.strip()
        elif not self.strip_whitespace and other.data:
            data = other.data
        else:
            data = ''

        if field.data and self.strip_whitespace:
            current = field.data.strip()
        elif field.data:
            current = field.data.strip()
        else:
            current = ''
        if data and not current:
            raise ValidationError(self.message)

class NotEqual(object):
    """
    :param str message:
        Error message to raise in case of a validation error. Can be
        interpolated with `%(other_label)s` and `%(other_name)s` to provide a
        more helpful error.
    :param str fieldname: The name of the other field to compare to.
    :param bool case_sensitive: check case charset
    :param bool strip_whitespace: check case charset
    """

    def __init__(self, fieldname, message=None, case_sensitive=False, strip_whitespace=True):
        self.message = message or "not equal to {0} field".format(fieldname)
        self.strip_whitespace = strip_whitespace
        self.case_sensitive = case_sensitive
        self.fieldname = fieldname

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError("Invalid field name {0}.".format(
                self.fieldname
            ))

        if self.strip_whitespace and other.data:
            data = other.data.strip()
        elif other.data:
            data = other.data
        else:
            data = ''

        if field.data and self.strip_whitespace:
            current = field.data.strip()
        elif field.data:
            current = field.data.strip()
        else:
            current = ''

        if not self.case_sensitive:
            data = data.lower()
            current = current.lower()

        if data == current:
            raise ValidationError(self.message)
