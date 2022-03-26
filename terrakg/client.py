from terra_sdk.client.lcd import LCDClient


class ClientContainer:

    def __init__(self, lcd_url: str = 'https://bombay-lcd.terra.dev',
                 chain_id: str = 'bombay-12'):
        self.lcd_url = lcd_url
        self.chain_id = chain_id
        self.lcd_client = LCDClient(chain_id=chain_id, url=lcd_url)
