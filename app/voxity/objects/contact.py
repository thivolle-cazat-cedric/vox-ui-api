# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)
from wtforms.fields import StringField
from wtforms.fields.html5 import EmailField, TelField
from wtforms.validators import InputRequired, optional, Email, Length
from . import ObjectBase
from .validators import (
    BaseForm, MandatoryOrOther, PhoneNumberFormat, MandatoryIfField, NotEqual
)
from .validators.contact import ShortcutTelFormat


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

    def __init__(self, *args, **kwargs):
        super(Contact, self).__init__(*args, **kwargs)
        for k in [' ', '-', '_', '.', '/']:
            if self.telephone_number and k in self.telephone_number:
                self.telephone_number = self.telephone_number.replace(k, '')
            if self.mobile and k in self.mobile:
                self.mobile = self.mobile.replace(k, '')

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

    def to_dict(self, is_query=False):
        dico = super(Contact, self).to_dict()
        if is_query:
            dico['telephoneNumber'] = dico.pop('telephone_number', '')
            dico['phonenumberraccourci'] = dico.pop('phone_number_raccourci', '')
            dico['employeenumber'] = dico.pop('phone_mobile_raccourci', '')

        return dico


class ContactForm(BaseForm):

    cn = StringField('Prénom, nom', validators=[
        InputRequired('Nom obligatoire'),
        Length(min=1, max=64, message="Minimum %(min) caractères, Maximum %(max)")
    ])
    telephone_number = TelField('Téléphone principal', validators=[
        MandatoryOrOther('mobile', 'Numéro obligatoire'),
        PhoneNumberFormat('Erreur de format, minimum 3 chiffres'),
        MandatoryIfField('phone_number_raccourci', 'Obligatoire si vous souhaitez un raccourci')
    ])
    mobile = TelField('Téléphone secondaire', validators=[
        MandatoryIfField('phone_mobile_raccourci', 'Obligatoire si vous souhaitez un raccourci'),
        PhoneNumberFormat('Error de format, minimum 3 chiffres')
    ])
    mail = EmailField('mail', validators=[
        optional(),
        Email('Adresse email invalide')
    ])
    phone_number_raccourci = StringField('Raccourci', validators=[
        optional(),
        ShortcutTelFormat("Raccourcie invalide.\n ex: *1234"),
        NotEqual('phone_mobile_raccourci', message='Les raccourcies ne peuvent être égales')
    ])
    phone_mobile_raccourci = StringField('Raccourci', validators=[
        optional(),
        ShortcutTelFormat("Raccourcie invalide.\n ex: *1234"),
        NotEqual('phone_number_raccourci', message="Les raccourcies ne peuvent être égales")
    ])
