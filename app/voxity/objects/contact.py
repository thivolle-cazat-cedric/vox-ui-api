from . import ObjectBase


class Contact(ObjectBase):
    """
    :param str id: unique id
    """

    _DICT_KEYS = [
        'uid',
        'cn',
        'telephone_number',
        'mobile',
        'mail',
        'phone_number_raccourci',
        'phone_mobile_raccourci'
    ]

    @staticmethod
    def litst_object_from_dict(lst_dict):
        if isinstance(lst_dict, list):
            contacts = []
            for dico in lst_dict:
                contacts.append(Contact(**dico))
            return contacts

    @property
    def phone_number_raccourci(self):
        return self.phoneNumberRaccourci

    @phone_number_raccourci.setter
    def phone_number_raccourci(self, val):
        self.phoneNumberRaccourci = val

    @property
    def phone_mobile_raccourci(self):
        return self.employeeNumber

    @phone_mobile_raccourci.setter
    def phone_mobile_raccourci(self, val):
        self.employeeNumber = val

    @property
    def telephone_number(self):
        return self.telephoneNumber

    @telephone_number.setter
    def telephone_number(self, val):
        self.telephoneNumber = val
