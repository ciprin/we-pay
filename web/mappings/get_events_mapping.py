from web.config import Config

config = Config.test_config()


def logic_to_request(id):
    print('event_id from mapping ', id)
    return {
        'url': f"{config['events_url']}/{id}",
        'type': 'GET',
        'call': 'Get events with an ID of at least from',
    }


def response_to_logic(response):
    return sorted(response['events'], key=lambda d: d['event_id'], reverse=True)
