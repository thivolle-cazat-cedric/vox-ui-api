# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

def number_clear(value, space=False):
    if value[0:3] == "+33":
        value = '0' + value[3:]

    if space:
        value = " ".join(value[i:i + 2] for i in range(0, len(value), 2))

    return value