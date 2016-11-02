# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)
import re
from wtforms.fields import StringField, HiddenField
from wtforms.fields.html5 import EmailField, TelField
from wtforms.validators import InputRequired, optional, Email, Length
from . import ObjectBase
from .validators import (
    BaseForm, MandatoryOrOther, PhoneNumberFormat, MandatoryIfField, NotEqual
)
from .validators.contact import ShortcutTelFormat
from app.utils.jinja2_filters import number_clear


def is_mobile(number):
    mobile_regex = re.compile(r'^0[67]\d{8}$')
    if number and mobile_regex.match(number_clear(number, space=False)):
        return True
    else:
        return False


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

    LOCAL_EXTEN = {
        '8500': 'Messagerie',
        '8501': 'Messagerie',
        '0': 'Iconnue',
        '#8600': 'Enregistrement de fichier'
    }

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

        for k in self.__ATTR__ + ['phoneNumberRaccourci', 'employeeNumber']:
            if k in dico and isinstance(dico[k], type('')):
                dico[k] = dico[k].strip()

        self.uid = dico.get('uid', None)
        self.cn = dico.get('cn', None)
        self.telephone_number = dico.get('telephone_number', dico.get('telephoneNumber', ''))
        self.mobile = dico.get('mobile', '')
        self.mail = dico.get('mail', '')
        self.phone_number_raccourci = dico.get('phone_number_raccourci', dico.get('phoneNumberRaccourci', ''))
        self.phone_mobile_raccourci = dico.get('phone_mobile_raccourci', dico.get('employeeNumber', ''))

    def to_dict(self, is_query=False):
        dico = super(Contact, self).to_dict()
        if is_query:
            dico['telephoneNumber'] = dico.pop('telephone_number', None)
            dico['phoneNumberRaccourci'] = dico.pop('phone_number_raccourci', None)
            dico['employeeNumber'] = dico.pop('phone_mobile_raccourci', None)

        return dico

    def have_mobile(self):
        mobiles = []
        if is_mobile(self.telephone_number):
            mobiles.append(self.telephone_number)
        if is_mobile(self.mobile):
            mobiles.append(self.mobile)

        return mobiles


class ContactForm(BaseForm):
    uid = HiddenField('uid', validators=[
        optional()
    ])
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
