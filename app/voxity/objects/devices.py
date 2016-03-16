# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)
from . import ObjectBase
from datetime import datetime


class Device(ObjectBase):
    """
    :param str id: unique id
    :param str extension: internal extension of device
    :param str last_update: last update information
    :param int state: device state code
    :param str state_desc: device state description
    :param str state_class: class for html state (color/animation)
    """

    __ATTR__ = [
        'id',
        'extension',
        'last_update',
        'state',
        'state_desc',
        'icon_class'
    ]

    _DESCRIPTION = {
        'fr': {
            'unavailable': "non connecté",
            'available': 'disponible',
            'ring': 'sonne',
            'ringing': 'sonne',
            'in-use': 'en communication',
            'unknow': 'iconnue'
        }
    }
    _lang = 'fr'

    id = None
    extension = None
    last_update = None
    state = None
    state_desc = None
    icon_class = None

    @staticmethod
    def litst_obj_from_list(lst_dict, sort_by_extention=False):
        if isinstance(lst_dict, list):
            l = []
            if sort_by_extention:
                lst_dict = sorted(lst_dict, key=lambda k: k['extension'])
            for dico in lst_dict:
                l.append(Device(**dico))
            return l


    def __init__(self, *args, **kwargs):
        super(Device, self).__init__(*args, **kwargs)
        if 'state' in kwargs:
            try:
                self.state = int(kwargs.get('state'))
            except Exception:
                self.state = -1
                self.state_desc = 'unknow'
            pass
        else:
            raise ValueError('Device : attribut state mendatory')

        try:
            self.last_update = datetime.strptime(
                self.last_update, '%Y-%m-%dT%H:%M:%S.%fZ'
            )
        except ValueError:
            pass

    @property
    def icon_class(self):
        default = "fa fa-2x fa-fw fa-phone-square"
        icon_class = ''
        if self.state == 0:
            icon_class = default + " text-success"
        elif self.state == 2:
            icon_class = default + " text-danger animated infinite flash"
        elif self.state == 3:
            icon_class = default + " text-danger"
        elif self.state == 5:
            icon_class = default + " text-muted"
        else:
            icon_class = "fa fa-2x fa-fw fa-question-circle text-muted"
        return icon_class

    @property
    def state_description(self):
        try:
            return self._DESCRIPTION[self._lang][self.state_desc.lower()]
        except Exception:
            try:
                return self._DESCRIPTION[self._lang]['unknow']
            except Exception, e:
                return self.state_desc or 'unknow'

    def to_dict(self):
        ret = super(Device, self).to_dict()
        if isinstance(self.last_update, datetime):
            ret['last_update'] = self.last_update.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        return ret
