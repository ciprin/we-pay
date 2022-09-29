from web.config import Config

config = Config.test_config()


def logic_to_request(wallet_id, type, iban, amount):
    return {
        'url': f"{config['settle_url']}",
        'type': 'POST',
        'call': 'Initiate either a pay-in or pay-out for a given wallet.',
        'json': {
            'wallet_id': wallet_id,
            'type': type,
            'iban': iban,
            'amount': str(amount)
        }
    }


def response_to_logic(response):
    return response
