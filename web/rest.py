import json
import random

import requests

from web.utils import exponential_wait_considering_attempts_extra, exponential_wait_considering_attempts
from web.mappings import create_wallet_mapping, perform_settlement_mapping
from web.mappings import get_events_mapping


def send_request(request):
    request_json = request.get('json', {})
    backoff_in_seconds = 3

    method_func = getattr(requests, request['type'].lower(), None)
    attempts = 0
    max_attempts = 10
    while attempts < max_attempts:
        response = method_func(
            request['url'],
            json=request_json,
            headers=request.get('headers', {}),
            params=request.get('params', {})
        )
        if response.status_code != 500:
            break
        if response.status_code == 500:
            print('Status code is 500 for ' + request['url'] + ', backing: ',
                  backoff_in_seconds * 2 ** attempts + random.random())
            exponential_wait_considering_attempts_extra(attempts)
            attempts += 1
            continue

    json_response = json.loads(response.text) if response.text else {
        'error_message': 'some error'}

    return [], json_response


def create_wallet(wallet_id):
    request = create_wallet_mapping.logic_to_request(wallet_id)

    retry = True
    while retry:
        errors, response = send_request(request)
        if response['result'] == 'error':
            retry = False
    return wallet_id


def perform_settlement(wallet_id, type, iban, amount):
    request = perform_settlement_mapping.logic_to_request(wallet_id, type, iban, amount)

    errors, response = send_request(request)

    return perform_settlement_mapping.response_to_logic(response)


# @ratelim.greedy(2, 10)
def retrieve_events(event_id):
    attempts = 1
    retry = True
    while retry:
        errors, response = send_request(get_events_mapping.logic_to_request(event_id))
        if response.get('events') is not None and len(response['events']) > 1:
            retry = False
        elif response.get('events') is not None and len(response['events']) == 0:
            event_id = int(event_id * 1 / attempts)
            attempts += 1

        exponential_wait_considering_attempts(attempts)

    return get_events_mapping.response_to_logic(response)


def determine_events(event_id):
    errors, response = send_request(get_events_mapping.logic_to_request(event_id))

    return get_events_mapping.response_to_logic(response)
