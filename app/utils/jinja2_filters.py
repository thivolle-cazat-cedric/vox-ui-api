# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
import re

EXTERNAL_PHONE_NUM_RE = re.compile('\+?\d{5,}')

def number_clear(value, space=True):
    if value and len(value) > 3 and value[0:3] == "+33":
        value = '0' + value[3:]

    if value and space and EXTERNAL_PHONE_NUM_RE.match(value):
        value = " ".join(value[i:i + 2] for i in range(0, len(value), 2))

    return value