from . import ObjectBase

class Device(ObjectBase):
    """
    :param str id: unique id
    :param str extension: internal extension of device
    :param str last_update: last update information
    :param int state: device state code
    :param str state_desc: device state description
    :param str state_class: class for html state (color/animation)
    """

    _DICT_KEYS = [
        'id',
        'extension',
        'last_update',
        'state',
        'state_desc',
        'icon_class'
    ]

    @staticmethod
    def litst_object_from_dict(lst_dict, sort_by_extention=False):
        if isinstance(lst_dict, list):
            l = []
            if sort_by_extention:
                lst_dict = sorted(lst_dict, key=lambda k: k['extension'])
            for dico in lst_dict:
                l.append(Device(**dico))
            return l

    def __init__(self, *args, **kwargs):
        super(Device, self).__init__(*args, **kwargs)
        try:
            self.state = int(self.state)
        except Exception:
            raise ValueError('Device.state : must ben integer')

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
            icon_class = "fa fa-2x fa-fw fa-phone-time text-muted"
        return icon_class
