# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
import re
from jinja2.filters import do_mark_safe
from flask import session

EXTERNAL_PHONE_NUM_RE = re.compile('\+?\d{5,}')
PHONE_NUM_FR = re.compile('\d{10}')


def number_clear(value, space=True):
    num = value
    if value and len(value) > 3 and value[0:3] == "+33":
        value = '0' + value[3:]

    if value and space and PHONE_NUM_FR.match(value):
        value = " ".join(value[i:i + 2] for i in range(0, len(value), 2))

    return value or ''


def val_or_label(value, default, strip_value=True, label_class="default"):
    try:
        label_class = label_class.lower()
        if label_class not in ['default', 'danger', 'warning', 'info', 'primary']:
            raise ValueError('val_or_label : label_class {0} not allowed'.format(
                label_class))
    except:
        label_class = 'default'

    if strip_value and isinstance(value, type('')):
        value = value.strip()

    if value:
        return value
    else:
        return do_mark_safe('<span class="label label-{0}">{1}</span>'.format(
            label_class,
            default))


def is_admin(**kwargs):
    try:
        return bool(session['user']['is_admin'])
    except Exception:
        return False
