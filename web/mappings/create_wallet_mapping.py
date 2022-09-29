from web.config import Config

config = Config.test_config()


def logic_to_request(id):
    return {
        'url': f"{config['wallet_url']}/{str(id)}",
        'type': 'POST',
        'call': 'Create a new wallet with the given ID',
        'json': {
        }
    }


def response_to_logic(response):
    return response
