class Config:
    @staticmethod
    def test_config():
        base_api_url = 'http://127.0.0.1:5000'
        return {
            'wallet_url': f'{base_api_url}/wallet',
            'settle_url': f'{base_api_url}/settle',
            'events_url': f'{base_api_url}/events'
        }
