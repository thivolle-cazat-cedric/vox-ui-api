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

    contact = get_contacts()
    item = request.args.get('item', 'Tout')
    pager = dict()
    contact_total = len(contact)

    if item != 'Tout':
        try:
            item = int(item)
            pager['current'] = int(request.args.get('page', 1))
            pager['max'] = roundup(contact_total / item)
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
            constact_start = pager['current'] * item - item
            contact_end = pager['current'] * item
            contact = contact[constact_start:contact_end]

        except Exception:
            item = 'Tout'

    return render_template(
        'contacts/index.html',
        contacts=contact,
        pager=pager,
        item=item,
        items=LIST_AVAILABLE,
        contact_total=contact_total,
        usr=session['user']
    ).encode('utf-8')

@CONTACT.route('<uid>-view.html', methods=["GET"])
def test_view(uid=None):
    return str(uid)
    