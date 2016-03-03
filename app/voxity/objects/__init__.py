# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)


class ObjectBase(object):
    """ObjectBase to implémente default methode in object"""

    _DICT_KEYS = []

    def __init__(self, *args, **kwargs):
        super(ObjectBase, self).__init__()
        self.from_dict(kwargs)

    def __repr__(self):
        return "<{0}>".format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()

    def from_dict(self, dico):
        '''
        :param dict dico:
        '''
        if not isinstance(dico, dict):
            raise ValueError('from_dict : arg1 must be a dict')

        for k in dico.keys():
            setattr(self, k, dico[k])

    def to_dict(self):
        d = {}
        for k in self._DICT_KEYS:
            d[k] = getattr(self, k)
        return d

from .devices import Device
