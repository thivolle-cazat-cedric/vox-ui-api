# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from flask import Blueprint, render_template, session, request, redirect, url_for
from flask.json import jsonify
from app.voxity import get_contacts, refresh_token
from app.controllers import is_auth
from math import ceil

CONTACT = Blueprint('CONTACT', __name__)

LIST_AVAILABLE = [5, 10, 25, 50, 100]


def roundup(x):
    return int(ceil(x))

@CONTACT.route('all.json', methods=["GET"])
@is_auth
def json_data():
    return jsonify({'data': get_contacts()})


@CONTACT.route('', methods=["GET"])
@CONTACT.route('index.html', methods=["GET"])
@is_auth
def view():

    item = request.args.get('item', 25)
    page = request.args.get('page', 1)
    pager = dict()

    if item != 'all':
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
            item = 'all'
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
        search_mode=False
    ).encode('utf-8')


@CONTACT.route('<uid>-view.html', methods=["GET"])
@is_auth
def test_view(uid=None):
    return str(uid)

@CONTACT.route('search.html', methods=['GET'])
@is_auth
def search():
    contact = list()
    form_value = dict()
    if not request.args.get('name', ''):
        return redirect(url_for('CONTACT.view'))
    else:
        form_value['name'] = "{0}".format(request.args.get('name', ''))

    contact = get_contacts(**form_value)
    print(contact)
    return render_template(
        'contacts/index.html',
        contacts=contact['list'],
        item="all",
        contact_total=len(contact['list']),
        search_mode=True,
        form_value=form_value
    ).encode('utf-8')
