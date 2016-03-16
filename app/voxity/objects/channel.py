
# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)
from . import ObjectBase


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

    __ATTR__ = [
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

    id = None
    channel_id = None
    channel_state = None
    channelstatedesc = None
    caller_num = None
    caller_name = None
    exten = None
    originated_by_incomming_call = None
    is_external_channel = None
    has_music_onhold = None
    transfer_to = None
    transfer_type = None
    protocol = None

    def __init__(self, *args, **kwargs):
        super(Channel, self).__init__(*args, **kwargs)
        try:
            self.channel_state = int(self.channel_state)
        except Exception:
            self.channel_state = -1
            self.channelstatedesc = 'unknow'

    def is_incomming_call(self):
        '''
        :rettype: bool
        :return: true if is incomming call
        '''
        return not self.caller_num == self.exten

    def get_icon_stat(self):
        '''
        :rettype: str
        :return: fa icon class
        '''
        try:
            return self._FA_ICON[self.channel_state]
        except Exception:
            return "fa fa-question-circle"
