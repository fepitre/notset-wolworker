#!flask/bin/python3
import os
import json
import logging

from functools import wraps
from flask import Flask, jsonify, request
from authentication import AuthClient
from apierror import ApiError
from wakeonlan import WoLClient

app = Flask(__name__)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def read_config():
    """
    {
      "machines": {
        "server1": "AA:BB:CC:DD:EE:FF",
        "server2": "00:11:22:33:44:55"
      }
    }
    """
    config_path = os.environ.get('WOL_CONFIG',
                                 '/home/user/wolworker.conf')
    with open(config_path, 'r') as cfd:
        conf = json.loads(cfd.read())

    if not conf.get('machines'):
        raise AttributeError(f'Machines not provided')

    if not conf.get('uids'):
        raise AttributeError(f'Empty user list provided')

    if not conf.get('key'):
        raise AttributeError(f'Authentication key not provided')

    return conf


wol_config = read_config()
wol_cli = WoLClient(wol_config.get('machines', {}))
auth_cli = AuthClient(wol_config.get('key'), wol_config.get('uids'))


@app.errorhandler(ApiError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def authentication(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not auth_cli.valid_token(token):
            return jsonify({'message': 'invalid token provided'})

        return f(*args, **kwargs)

    return decorator


@app.route('/api/machines', methods=['GET'])
@authentication
def get_machines():
    """
    GET available machines
    """
    return jsonify(wol_cli.machines)


@app.route('/api/machines/<string:machine_name>', methods=['POST'])
@authentication
def wol_machine(machine_name):
    """
    POST wol for requested machine
    """
    if not wol_cli.machines:
        raise ApiError('No machines configured', status_code=404)

    machine_mac = wol_cli.machines.get(machine_name)
    if not machine_mac:
        raise ApiError(f'No machine with name {machine_name} found',
                       status_code=404)

    logger.info(f'Resolved {machine_name} to {machine_mac}')

    try:
        wol_cli.wake_on_lan(machine_mac)
        logger.info(f'Sent WOL packet to {machine_name} at {machine_mac}')
        return jsonify({'message': f'WOL packet sent to {machine_name}'})
    except Exception as exc:
        raise ApiError(f'Unable to wol machine {machine_name}: {exc}')


if __name__ == '__main__':
    app.run(debug=True)
