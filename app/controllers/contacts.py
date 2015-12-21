# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from flask import Blueprint, render_template, session, request
from flask.json import jsonify
from app.voxity import get_contacts
from math import ceil


CONTACT = Blueprint('CONTACT', __name__)

LIST_AVAILABLE = [5, 10, 25, 50, 100]


def roundup(x):
    return int(ceil(x))


@CONTACT.route('', methods=["GET"])
def json_data():
    return jsonify({'data': get_contacts()})


@CONTACT.route('view.html', methods=["GET"])
def view():

    item = request.args.get('item', 'Tout')
    page = request.args.get('page', 1)
    pager = dict()

    if item != 'Tout':
        contact = get_contacts(page=page, limit=item)
        contact_total = int(contact['pager']['total'])

        try:
            item = int(item)
            pager['current'] = int(contact['pager']['curent_page'])
            pager['max'] = int(contact['pager']['max_page'])
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
            contact = get_contacts()
            item = 'Tout'
    else:
        contact = get_contacts()
        contact_total = contact['pager']

    return render_template(
        'contacts/index.html',
        contacts=contact['list'],
        pager=pager,
        item=item,
        items=LIST_AVAILABLE,
        contact_total=contact_total,
        usr=session['user']
    ).encode('utf-8')


@CONTACT.route('<uid>-view.html', methods=["GET"])
def test_view(uid=None):
    return str(uid)
