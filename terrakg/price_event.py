import datetime
import time

from terrakg.client import ClientContainer
from terrakg.kg import KG
from terrakg.rates import Rates

from terrakg import logger


logger = logger.get_logger(__name__)


class PriceEvent:
    def __init__(self) -> None:
        self.client = ClientContainer(lcd_url="https://lcd.terra.dev", chain_id='columbus-5')
        self.rates = Rates(self.client)
        self.kg = KG()

    def listen(self, wait_time: int = 2):
        opportunities = self.kg.get_swap_opportunities()

        while True:
            event = list()
            for opp in opportunities:
                s_t_rate_result = self.rates.get_token_quote_and_fees(opp.contract, opp.pair, reverse=True)
                t_s_rate_result = self.rates.get_token_quote_and_fees(opp.contract, opp.pair)

                if s_t_rate_result is None or t_s_rate_result is None:
                    # Something went wrong with query, skip this iteration
                    yield None

                s_t_rate = 1000000 / int(s_t_rate_result[0])
                t_s_rate = int(t_s_rate_result[0]) / 1000000
                s_t_ratio = (s_t_rate - 1) * 100
                t_s_ratio = (t_s_rate - 1) * 100

                event.append({
                    "s_t_rate": s_t_rate,
                    "t_s_rate": t_s_rate,
                    "s_t_ratio": s_t_ratio,
                    "t_s_ratio": t_s_ratio,
                    "target": opp.target,
                    "dex": opp.dex,
                    "timestamp": datetime.datetime.now()
                })
            yield event
            time.sleep(wait_time)


if __name__ == "__main__":
    pe = PriceEvent()
    print("Printing 3 current price events...")
    for i, es in enumerate(pe.listen()):
        if i > 2:
            print("\nExiting...")
            break
        print(f"\n{i + 1}. at {es[0]['timestamp']}")
        for e in es:
            print(f"Luna -> {e['target']} rate at {e['dex']}: {e['s_t_rate']}")
            print(f"{e['target']} -> Luna rate at {e['dex']}: {e['t_s_rate']}")
