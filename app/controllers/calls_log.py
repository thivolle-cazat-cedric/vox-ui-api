# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from flask import Blueprint, render_template, session, request
from flask.json import jsonify
from app.voxity import get_calls_log
from app.controllers import is_auth


CALLS_LOG = Blueprint('CALLS_LOG', __name__)

LIST_AVAILABLE = [5, 10, 25, 50, 100]


@CALLS_LOG.route('all.json', methods=["GET"])
@is_auth
def json_data():
    return jsonify({'data': get_calls_log()})

@CALLS_LOG.route('', methods=["GET"])
@CALLS_LOG.route('index.html', methods=["GET"])
@is_auth
def view():

    item = request.args.get('item', 25)
    page = request.args.get('page', 1)
    pager = dict()

    if item != 'all':
        log = get_calls_log(page=page, limit=item)
        log_total = int(log['pager']['total'])

        try:
            item = int(item)
            pager['current'] = int(log['pager']['curent_page'])
            pager['max'] = int(log['pager']['max_page'])
            pager['min'] = 1
            pager['start'] = 1
            pager['end'] = pager['max']

            if pager['end'] - pager['start'] > 10:
                pager['start'] = pager['current'] - 5
                if pager['start'] < 1:
                    pager['start'] = 1

                pager['end'] = pager['start'] + 10
                if pager['end'] > pager['max']:
                    pager['end'] = pager['max']
                    pager['start'] = pager['end'] - 10

        except Exception:
            log = get_calls_log()
            item = 'all'
    else:
        log = get_calls_log()
        log_total = log['pager']

    return render_template(
        'calls_log/index.html',
        log=log['list'],
        pager=pager,
        item=item,
        items=LIST_AVAILABLE,
        log_total=log_total,
    ).encode('utf-8')