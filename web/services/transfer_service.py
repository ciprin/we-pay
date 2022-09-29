import threading
import time

from flask import jsonify

from web.utils import determine_initial_event_id
from web.constants import MAXIMUM_SETTLMENT_DURATION, ESTIMATE_INITIAL_EVENT_ID
from web.rest import create_wallet, perform_settlement, retrieve_events

event_id = determine_initial_event_id(ESTIMATE_INITIAL_EVENT_ID)


def initiate_half_transaction(iban, amount, type):
    global event_id

    wallet = create_wallet(iban)
    print('wallet created ', wallet)

    events = get_events_and_increment_event_id(2)
    confirmed = False
    start_settlement_time = time.time()
    settlement_confirm_retries = 1

    while not confirmed:

        settlement = perform_settlement(wallet, type, iban, amount)
        print('settlement initiated ', wallet, type, iban, amount, settlement)

        while time.time() - start_settlement_time < MAXIMUM_SETTLMENT_DURATION:
            current_settlement_time = time.time()
            if any(event['wallet_id'] == wallet for event in events) and any(
                    start_settlement_time <= event['created_at'] <= current_settlement_time for event in events):
                confirmed = True
                print('settlement performed ', wallet, type, iban, amount)
                break
            settlement_confirm_retries += 1
            # wait_considering_attempts(settlement_confirm_retries)

            events = get_events_and_increment_event_id(1 / settlement_confirm_retries)

    print('half transaction completed')

    return confirmed


def initiate_transfer_background(from_iban, to_iban, amount):
    global event_id
    add_initial_money_just_for_testing = initiate_half_transaction(from_iban, amount*2, type='payin')
    pay_in = initiate_half_transaction(to_iban, amount, type='payin')
    if pay_in:
        pay_out = initiate_half_transaction(from_iban, amount, type='payout')
        if not pay_out:
            rollback = initiate_half_transaction(to_iban, amount, type='payout')
            if rollback:
                return jsonify(dict(result='Transaction rolled back.'))
        return jsonify(dict(result='success'))


def initiate_transfer(from_iban, to_iban, amount):
    t = threading.Thread(target=initiate_transfer_background, args=(from_iban, to_iban, amount))
    t.start()


def get_events_and_increment_event_id(adjust):
    global event_id
    print('event_id is ', event_id)
    events = retrieve_events(event_id)
    # event_id = events[0]['event_id']
    event_id = int(events[0]['event_id'] * adjust)
    event_id = event_id if event_id > 0 else 1
    print('event_id is ', event_id)
    return events
