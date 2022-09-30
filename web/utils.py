import random
import time

from web.constants import BACKOFF_IN_SECONDS


def exponential_wait_considering_attempts(attempt):
    time.sleep(2**attempt)


def exponential_wait_considering_attempts_extra(attempt):
    time.sleep(BACKOFF_IN_SECONDS*2**attempt + random.random())


def determine_initial_event_id(estimate):
    from rest import determine_events
    while len(determine_events(estimate)) > 0:
        estimate = estimate*2
    else:
        while len(determine_events(estimate)) == 0:
            estimate = int(estimate/2)

    return estimate
