# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)


class ObjectBase(object):
    """ObjectBase to implémente default methode in object"""

    __ATTR__ = []

    @classmethod
    def litst_obj_from_list(cls_obj, dict_list):
        if isinstance(dict_list, list):
            ret_list = []
            for o in dict_list:
                ret_list.append(cls_obj(**o))
            return ret_list
        else:
            raise ValueError("{0}.litst_obj_from_list : arg1 must be list type".format(
                cls_obj.__name__
            ))


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

        for k in self.__ATTR__:
            try:
                setattr(self, k, dico.get(k, None))
            except Exception:
                pass

    def to_dict(self):
        d = {}
        for k in self.__ATTR__:
            d[k] = getattr(self, k)
        return d
