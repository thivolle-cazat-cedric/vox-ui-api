from __future__ import division, unicode_literals
from flask import Blueprint, request, abort
from flask.json import jsonify
from app.controllers import is_auth
from app.voxity import api_proxy


API_PROXY = Blueprint('api',
    __name__,
    url_prefix='/api/',
)

@API_PROXY.route('<path:uri>', methods=['GET'])
@is_auth
def proxy(uri):
    # v1/login/status
    # raise ValueError('fo chec')    
    ret = api_proxy(uri, 'get', params=request.args.to_dict())
    if ret.status_code == 200:
        return jsonify({'resp': ret.json()})
    else:
        abort(ret.status_code)