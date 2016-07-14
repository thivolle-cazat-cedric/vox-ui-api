# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from flask import Blueprint, render_template, request, session, abort
from flask.json import jsonify
from app.voxity.channel import get_log
from app.controllers import is_auth
from app.utils import value_or_zero


CALLS_LOG = Blueprint('CALLS_LOG',
    __name__,
    template_folder='templates',
    url_prefix='/calls_log/'
)

LIST_AVAILABLE = [5, 10, 25, 50, 100]


@CALLS_LOG.route('all.json', methods=["GET"])
@is_auth
def json_data():
    return jsonify({'data': get_log()})


@CALLS_LOG.route('my.json', methods=["GET"])
@is_auth
def my_json():
    return jsonify(
        {'data': get_log(
            dstchannel=session['user']['internalExtension']
        )}
    )


@CALLS_LOG.route('<direction>_calls.html', methods=["GET"])
@is_auth
def view(direction='incoming'):
    if direction not in ['incoming', 'outing']:
        abort(404)

    item = request.args.get('item', 25)
    page = request.args.get('page', 1)
    pager = dict()
    params = dict()

    if item != 'all':
        params['page'] = page
        params['limit'] = item

    if direction == "outing":
        params['src_phonenumber'] = session['user']['internalExtension']
    else:
        params['dstchannel'] = '*-{0}-*'.format(
            session['user']['internalExtension']
        )

    log = get_log(**params)

    try:
        if item != "all":
            item = int(item)
            pager['current'] = int(value_or_zero(log['pager']['curent']))
            pager['max'] = int(value_or_zero(log['pager']['max_page']))
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

    except Exception as e:
        raise e

    return render_template(
        'calls_log/index.html',
        log=log['list'] or [],
        pager=pager,
        item=item,
        items=LIST_AVAILABLE,
        log_total=int(value_or_zero(log['pager']['total_item'])),
    ).encode('utf-8')


@CALLS_LOG.route('<direction>_calls.json', methods=["GET"])
@is_auth
def json_view(direction='incoming'):
    if direction not in ['incoming', 'outing']:
        abort(404)

    item = request.args.get('item', 25)
    page = request.args.get('page', 1)
    pager = dict()
    params = dict()

    if item != 'all':
        params['page'] = page
        params['limit'] = item

    if direction == "outing":
        params['src_phonenumber'] = session['user']['internalExtension']
    else:
        params['dstchannel'] = '*-{0}-*'.format(
            session['user']['internalExtension']
        )

    log = get_log(**params)

    try:
        item = int(item)
        pager['current'] = int(value_or_zero(log['pager']['curent']))
        pager['max'] = int(value_or_zero(log['pager']['max_page']))
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

    except Exception, e:
        raise e
        abort(500)

    return jsonify(
        {'data': log}
    )
