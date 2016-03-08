# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals


class ExceptVoxityTokenExpired(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, **kwargs):
        self.expr = 'Token Expired'
        self.msg = 'Acces token is expired, pleas refresh'