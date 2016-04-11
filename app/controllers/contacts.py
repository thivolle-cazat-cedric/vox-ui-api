# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from flask import Blueprint, render_template, request, abort, redirect, url_for, session
from flask.json import jsonify
from app.voxity import contact
from app.controllers import is_auth, is_admin
from app.utils import value_or_zero
from app.voxity.objects.contact import ContactForm


CONTACT = Blueprint('CONTACT', __name__)
LIST_AVAILABLE = [5, 10, 25, 50, 100]


@CONTACT.route('all.json', methods=["GET"])
@is_auth
def json_data():
    resp = contact.get().get('list', [])
    for num in contact.Contact.LOCAL_EXTEN.keys():
        resp.append({
            'telephoneNumber': num,
            'cn': contact.Contact.LOCAL_EXTEN[num]
        })
    return jsonify({'data': resp})


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
        search_mode=False,
    ).encode('utf-8')


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
    if not request.args.get('name', None):
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

    if number in contact.Contact.LOCAL_EXTEN:
        c.append({
            'telephoneNumber': number,
            'cn': contact.Contact.LOCAL_EXTEN[number]
        })
    else:
        c += contact.get()['list']

    for elt in c:
        if elt.get('mobile', '') == number or \
           elt.get('telephoneNumber', '') == number:
            name_list.append(elt)

    return jsonify({'data': name_list})


@CONTACT.route('add.html', methods=['GET'])
@is_auth
@is_admin
def get_add(form=None, api_errors=None):
    validate_state = False
    if form:
        validate_state = True
    return render_template(
        'contacts/form.html',
        form=form or ContactForm(),
        api_errors=api_errors,
        validate_state=validate_state
    ).encode('utf-8')


@CONTACT.route('add.html', methods=['POST'])
@is_auth
@is_admin
def post_add():
    api_errors = None
    form = ContactForm(request.form)
    form.strip_value()
    if form.validate():
        c = form.get_object(contact.Contact)
        resp = contact.add(**c.to_dict(is_query=True))
        if resp.get('status', False) == 200 and resp.get('result', {}).get('uid', False):
            session['new_contact'] = c.to_dict()
            return redirect(url_for('.view'))
        else:
            api_errors = resp.get('error', {'internal': 'Error inconnue'})

    return get_add(form=form, api_errors=api_errors)


@CONTACT.route('<uid>.html', methods=["GET"])
@is_auth
def view_uid(uid):
    c = contact.get_uid(uid=uid, ret_object=True)
    if not c:
        abort(404)

    return render_template(
        'contacts/view.html',
        contact=c,
    ).encode('utf-8')


@CONTACT.route('edit/<uid>.html', methods=["GET"])
@is_auth
@is_admin
def edit(uid=None):
    c = contact.get_uid(uid=uid, ret_object=True)
    if c:
        c_form = ContactForm(**c.to_dict())
        return render_template(
            'contacts/form.html',
            form=c_form,
            edit_mode=True
        ).encode('utf-8')
    else:
        abort(404)


@CONTACT.route('edit/<uid>.html', methods=["POST"])
@is_auth
@is_admin
def edit_save(uid=None):
    c = contact.get_uid(uid=uid, ret_object=True)
    if not c:
        abort(404)

    if request.form['uid'] != uid:
        abort(400)

    c_form = ContactForm(request.form)
    c_form.strip_value()
    if c_form.validate():
        c = c_form.get_object(contact.Contact)
        resp = contact.update(**c.to_dict(is_query=True))
        if resp and resp.get('result') and resp.get('result').get('uid', None) == uid and not resp.get('errors'):
            session['update_contact'] = c.to_dict()
            return redirect(url_for('.view'))
        else:
            return render_template(
                'contacts/form.html',
                form=c_form,
                edit_mode=True,
                api_errors=resp.get('error', {}),
                validate_state=True
            ).encode('utf-8')
    else:
        return render_template(
            'contacts/form.html',
            form=c_form,
            edit_mode=True,
            validate_state=True
        ).encode('utf-8')


@CONTACT.route('remove-<uid>.html', methods=["GET"])
@is_auth
@is_admin
def remove_warning(uid):
    c = contact.get_uid(uid=uid, ret_object=True)
    if not c:
        abort(404)

    return render_template(
        'contacts/remove.html',
        contact=c
    ).encode('utf-8')


@CONTACT.route('remove-<uid>.html', methods=["POST"])
@is_auth
@is_admin
def remove(uid):
    c = contact.get_uid(uid=uid, ret_object=True)
    if not c:
        abort(404)

    if request.form['uid'] != uid:
        abort(400)

    if contact.remove(uid):
        session['remove_contact'] = c.to_dict()
        return redirect(url_for('.view'))
    else:
        abort(500)
