from terra_sdk.exceptions import LCDResponseError

from terrakg import logger

# Logging
from terrakg.client import ClientContainer

logger = logger.get_logger(__name__)


class Rates:
    """
    Access the most recent rates.
    """
    def __init__(self, client: ClientContainer):
        self.client = client

    def get_token_quote_and_fees(self, token_contract: str, pair: str, amount: int = 1000000, reverse: bool = False):
        """
        Returns the price for `amount` of the token `pair` (exchange is included in pair).
        Set `reverse` to true to get the inverse price.
        """
        desc, action, result_key = ("reverse_simulation", "ask_asset", "offer_amount") if reverse else (
            "simulation", "offer_asset", "return_amount")

        query_msg = {
            desc: {
                action: {
                    "amount": str(amount),
                    "info": {"token": {
                        "contract_addr": token_contract
                    }
                    }
                }
            }
        }

        try:
            result = self.client.lcd_client.wasm.contract_query(pair, query_msg)
            return result[result_key], result['commission_amount']
        except LCDResponseError as e:
            logger.warning(f"Issue with price query: {e}")
            return None
