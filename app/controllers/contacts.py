# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from flask import Blueprint, render_template, request, abort
from flask.json import jsonify
from app.voxity import get_contacts
from app.controllers import is_auth
from math import ceil
from app.utils import value_or_zero

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
        contact_total = int(value_or_zero(contact['pager']['total_item']))

        try:
            item = int(item)
            pager['current'] = int(value_or_zero(contact['pager']['curent_page']))
            pager['max'] = int(value_or_zero(contact['pager']['max_page']))
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
        container_class='container-fluid',
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
        aboort(400)
    else:
        form_value['name'] = "{0}".format(request.args.get('name', ''))

    contact = get_contacts(cn=form_value['name'])
    return render_template(
        'contacts/index.html',
        contacts=contact['list'],
        item="all",
        contact_total=len(contact['list']),
        search_mode=True,
        form_value=form_value
    ).encode('utf-8')

@CONTACT.route('search.json', methods=['GET'])
@is_auth
def search_json():
    search = dict()
    for k in request.args:
        search[k] = request.args[k]

    contact = get_contacts(item=2500, **search)
    return jsonify({'data': contact})

@CONTACT.route('whois.html', methods=['GET'])
@is_auth
def whois():
    contacts = list()
    name_list = list()
    form_value = dict()
    if not request.args.get('number', ''):
        abort(400)
    number = '{0}'.format(request.args.get('number')).replace(' ', '').replace('.', '').replace('-', '')

    contacts += get_contacts()['list']

    for c in contacts:
        if c.get('mobile', '') == number or c.get('telephoneNumber', '') == number:
            name_list.append(c)

    return jsonify({'data': name_list})
