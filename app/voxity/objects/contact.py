# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)
from . import ObjectBase


class Contact(ObjectBase):
    """
    :param str uid: unique id
    :param str cn: contact name
    :param str telephone_number:  principal phone number
    :param str mobile:  second phone number
    :param str mail:  mail address
    :param str phone_number_raccourci: shortened  extension to call principal phone number
    :param str phone_mobile_raccourci: shortened  extension to call second phone number
    """

    __ATTR__ = [
        'uid',
        'cn',
        'telephone_number',
        'mobile',
        'mail',
        'phone_number_raccourci',
        'phone_mobile_raccourci'
    ]

    uid = None
    cn = None
    telephone_number = None
    mobile = None
    mail = None
    phone_number_raccourci = None
    phone_mobile_raccourci = None

    def from_dict(self, dico):
        '''
        :param dict dico:
        '''
        if not isinstance(dico, dict):
            raise AttributeError('voxity.object.Contact : from_dict : args 1 must be dict instance')

        self.uid = dico.get('uid', None)
        self.cn = dico.get('cn', None)
        self.telephone_number = dico.get('telephone_number', dico.get('telephoneNumber', None))
        self.mobile = dico.get('mobile', None)
        self.mail = dico.get('mail', None)
        self.phone_number_raccourci = dico.get('phone_number_raccourci', dico.get('phoneNumberRaccourci', None))
        self.phone_mobile_raccourci = dico.get('phone_mobile_raccourci', dico.get('employeeNumber', None))
