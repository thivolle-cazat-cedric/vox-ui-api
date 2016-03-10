from . import ObjectBase
from datetime import datetime


class Channel(ObjectBase):
    """
    :param str id: unique id
    :param str channel_id: Local serveur's channel reference
    :param int channel_state: Correspond to a channel state, see channelstatedesc for more information.
    :param str channelstatedesc: Correspond to a channel state
    :param str caller_num: Caller number for this channel
    :param str caller_name: Caller name (if it can be determined) for this channel
    :param str exten: If provided, this field describe extension composed by an agent or an external call
    :param str originated_by_incomming_call:
    :param str is_external_channel: Channel facin to external world
    :param str has_music_onhold: Provide which music on-hold is currently played on this channel (need onhold status)
    :param str transfer_to: In case of transfer (see appropriate state), give the number where this channel will be transfered
    :param str transfer_type: in case of transfer (see appropriate state), give the following type: blint(direct transfer) or attended (assisted transfer)
    :param str protocol: Protocol og this channel, will be all time SIP.
    """

    _DICT_KEYS = [
        'id',
        'channel_id',
        'channel_state',
        'channelstatedesc',
        'caller_num',
        'caller_name',
        'exten',
        'originated_by_incomming_call',
        'is_external_channel',
        'has_music_onhold',
        'transfer_to',
        'transfer_type',
        'protocol'
    ]

    _FA_ICON = {
        0: 'fa fa-times',
        5: 'fa fa fa-bell-o',
        6: 'fa fa-play',
        11: 'fa fa-pause'
    }

    @staticmethod
    def litst_object_from_dict(lst_dict):
        if isinstance(lst_dict, list):
            channels = []
            for dico in lst_dict:
                channels.append(Channel(**dico))
            return channels

    def __init__(self, *args, **kwargs):
        super(Channel, self).__init__(*args, **kwargs)
        try:
            self.channel_state = int(self.channel_state)
        except Exception:
            raise ValueError(
                'Channel.state : must ben integer not [{0} : {1}]'.format(
                self.channel_state,
                type(self.channel_state).__name__
            ))


    def is_incomming_call(self):
        return not self.caller_num == self.exten


    def get_icon_stat(self):
        '''
        :rettype: str
        :return: fa icon class
        '''
        # try:
        return self._FA_ICON[self.channel_state]
        # except Exception:
            # return ""
