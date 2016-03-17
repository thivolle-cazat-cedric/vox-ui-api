# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from flask import Blueprint, render_template, request, abort
from flask.json import jsonify
from app.voxity import contact
from app.controllers import is_auth
from app.utils import value_or_zero

CONTACT = Blueprint('CONTACT', __name__)
LIST_AVAILABLE = [5, 10, 25, 50, 100]


@CONTACT.route('all.json', methods=["GET"])
@is_auth
def json_data():
    return jsonify({'data': contact.get().get('list', []) or []})


@CONTACT.route('', methods=["GET"])
@CONTACT.route('index.html', methods=["GET"])
@is_auth
def view():

    item = request.args.get('item', 25)
    page = request.args.get('page', 1)
    pager = dict()

    if item != 'all':
        contacts = contact.get(page=page, limit=item, ret_object=True)
        contact_total = int(value_or_zero(contacts['pager']['total_item']))

        # try:
        item = int(item)
        pager['current'] = int(value_or_zero(contacts['pager']['curent']))
        pager['max'] = int(value_or_zero(contacts['pager']['max_page']))
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

        # except Exception:
            # contacts = contact.get(ret_object=True)
            # item = 'all'
    else:
        contacts = contact.get(ret_object=True)
        contact_total = contact['pager']
    return render_template(
        'contacts/index.html',
        container_class='container-fluid',
        contacts=contacts['list'],
        pager=pager,
        item=item,
        items=LIST_AVAILABLE,
        contact_total=contact_total,
        search_mode=False
    ).encode('utf-8')


@CONTACT.route('<uid>.html', methods=["GET"])
@is_auth
def test_view(uid=None):
    return "Not developed"

@CONTACT.route('<uid>.json', methods=["GET"])
@is_auth
def contact_uid(uid=None):
    c = contact.get_uid(uid=uid)
    if c:
        return jsonify({'data': c})
    else:
        abort(404)


@CONTACT.route('search.html', methods=['GET'])
@is_auth
def search():
    c = list()
    form_value = dict()
    if not request.args.get('name', ''):
        abort(400)
    else:
        form_value['name'] = "{0}".format(request.args.get('name', ''))

    c = contact.get(cn=form_value['name'], ret_object=True)
    return render_template(
        'contacts/index.html',
        container_class='container-fluid',
        contacts=c['list'],
        item="all",
        contact_total=len(c['list']),
        search_mode=True,
        form_value=form_value
    ).encode('utf-8')


@CONTACT.route('search.json', methods=['GET'])
@is_auth
def search_json():
    search = dict()
    for k in request.args:
        search[k] = request.args[k]

    c = contact.get(**search)
    return jsonify({'data': c})


@CONTACT.route('whois.json', methods=['GET'])
@is_auth
def whois():

    if not request.args.get('number', ''):
        abort(400)

    c = list()
    name_list = list()

    number = '{0}'.format(
        request.args.get('number')
    ).replace(' ', '').replace('.', '').replace('-', '')

    c += contact.get()['list']

    for elt in c:
        if elt.get('mobile', '') == number or \
           elt.get('telephoneNumber', '') == number:
            name_list.append(elt)

    return jsonify({'data': name_list})
