# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)
from . import ObjectBase
from datetime import datetime
from .validators import BaseForm
from wtforms.fields import StringField, TextAreaField
from wtforms.fields.html5 import TelField
from wtforms.validators import InputRequired, Length, Regexp
from app.voxity.objects.validators.fields import ListField
from app.voxity.objects.validators.sms import PhoneNumberList
from re import IGNORECASE


class Sms(ObjectBase):
    """
    :param str id: The message id returned after the sending
    :param datetime.datetime send_date: The date of the sending
    :param str phone_number: The receiver phone number (FORMAT: /^[0-9]{10}$/)
    :param str content: The content
    :param int nb_sms: The number of messages in a single sending
    :param str status: Gives information on the message status. Values {PENDING,DELIVERED,ERROR}
    :param datetime.datetime delivery_date: The message delivery date (format "YYYY-MM-DD HH:mm:ss")
    :param int code: A status code at the sending
    :param str code_message: A description of the status code
    :param str statut: It reports any error after the sending
    :param str libelle: It reports any error after the sending
    :param str code_erreur: It reports any error after the sending.
    :param str operateur: The receiver's operator
    """

    __ATTR__ = [
        'id',
        'send_date',
        'phone_number',
        'content',
        'nb_sms',
        'status',
        'delivery_date',
        'code',
        'code_message',
        'statut',
        'libelle',
        'code_erreur',
        'operateur'
    ]

    _STATUS = {
        'fr': {
            'PENDING': "En cours",
            'DELIVERED': "Délivré",
            'ERROR': "Erreur"
        }
    }
    _ERROR_CODE = {
        'fr': {
            0: "Votre message à été envoyé",
            4: "Vous devez saisir un message",
            5: "Le message ne doit pas dépasser 160 caractères",
            6: "Vous devez saisir un numéro de téléphone",
            7: "Un numéro de téléphone est sur 10 chiffres",
            11: "Le numéro de téléphone est dans la liste noire",
            16: "L’émetteur ne peut pas être vide",
            17: "L’émetteur doit être sur plus de 3 caractères et 11 caractères maximum",
            18: "L’émetteur ne peut pas comporter que des chiffres",
            19: "Si un émetteur est indiqué, le message ne peut pas dépasser 141 caractères",
            21: "Le numéro de téléphone n’est pas attribué",
            24: "No commercial sending between 8PM and 8AM, neither sundays and public holidays",
            27: "L’indicatif pays du téléphone n’est pas autorisé !",
            29: "Nous ne pouvons donner suite à votre demande (overflow)",
            36: "Vous n’etes pas autorisé à retirer le STOP SMS !",
        },
    }

    @staticmethod
    def litst_obj_from_list(lst_dict, sort_by_send_date=True):
        if isinstance(lst_dict, list):
            l = []
            if sort_by_send_date:
                lst_dict = sorted(lst_dict, key=lambda k: k['send_date'], reverse=True)
            for dico in lst_dict:
                l.append(Sms(**dico))
            return l

    def from_dict(self, dico):
        """
        :param dict dico:
        """
        super(Sms, self).from_dict(dico)
        try:
            self.nb_sms = int(self.nb_sms)
        except Exception:
            raise ValueError('Sms.nb_sms must be integer not {0}'.format(
                type(self.nb_sms).__name__)
            )

        try:
            self.code = int(self.code)
        except Exception:
            raise ValueError('Sms.code must be integer not {0}'.format(
                type(self.nb_sms).__name__)
            )

        try:
            if self.delivery_date:
                self.delivery_date = datetime.strptime(
                    self.delivery_date, '%Y-%m-%d %H:%M:%S'
                )
        except ValueError:
            pass

        try:
            if self.send_date:
                self.send_date = datetime.strptime(
                    self.send_date, '%Y-%m-%d %H:%M:%S'
                )
        except ValueError:
            pass

    @property
    def is_delivery(self):
        return bool(self.delivery_date)

    @property
    def status_local(self):
        try:
            return self._STATUS['fr'][self.status]
        except Exception:
            return self.status

    @property
    def code_message_local(self):

        try:
            return self._ERROR_CODE['fr'][self.code]
        except Exception:
            return self.code_message


class SmsRespons(ObjectBase):
    """
    :param: str id: The response id
    :param: str id_sms_sent: The message id for which this response is intended to
    :param: str send_date: The date of the sending
    :param: str phone_number: The receiver phone number (FORMAT: /^[0-9]{10}$/)
    :param: str content: The content
    """

    __ATTR__ = [
        'id',
        'id_sms_sent',
        'send_date',
        'phone_number',
        'content'
    ]


class SmsForm(BaseForm):
    def strip_value(self):
        for field in self._fields:
            if field != 'phone_number':
                self._fields[field].data = self._fields[field].data.strip()

            if self.phone_number.data:
                striped_list = []
                for num in self.phone_number.data:
                    striped_list.append(num.strip())
                self.phone_number.data = striped_list

    content = TextAreaField('Message', validators=[
        InputRequired('Obligatoire'),
        Length(min=1, max=160, message="Le message doit contenir au Minimum %(min) caractère et au Maximum %(max) caractères")
    ])
    phone_number = ListField('Destinataire', validators=[
        InputRequired('Obligatoire'),
        PhoneNumberList(message="Le(s) numéro(s) doit(vent) être(s) au(x) format 0605040302 et séparer par ',' pour un envoie multiple"),
    ])
    emitter = StringField('Non de l\'émétteur', validators=[
        InputRequired('Obligatoire'),
        Regexp('^[a-z]{4,10}$', flags=IGNORECASE, message="Doit contenir entre 4 et 10 caractères [a-Z]")
    ])
