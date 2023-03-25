import time
from .binance_ws import symbol_list_all_futures_binance
from .redis_db import *
import json


class ChartOfDencitys:

    def __init__(self, symbol):
        self.symbol = symbol
        self.future_bids = None
        self.future_asks = None
        self.best_future_bids = 0
        self.best_future_asks = 0
        self.spot_bids = None
        self.spot_asks = None
        self.best_spot_bids = 0
        self.best_spot_asks = 0
        self.update_book()
        self.nearest_density_250k = {}
        self.nearest_density_500k = {}
        self.nearest_density_750k = {}
        self.nearest_density_1m = {}

    def update_book(self):
        FUTURE_BOOK = get_redis(f'FUTURE_BOOK_{self.symbol}')
        SPOT_BOOK = get_redis(f'SPOT_BOOK_{self.symbol}')
        BEST_FUTURE = get_redis(f'FUTURE_TICKER_{self.symbol}')
        BEST_SPOT = get_redis(f'SPOT_TICKER_{self.symbol}')

        if FUTURE_BOOK:
            self.future_bids = json.loads(get_redis(f'FUTURE_BOOK_{self.symbol}')).get('bids', None)
            self.future_asks = json.loads(get_redis(f'FUTURE_BOOK_{self.symbol}')).get('asks', None)
        if SPOT_BOOK:
            self.spot_bids = json.loads(get_redis(f'SPOT_BOOK_{self.symbol}')).get('bids', None)
            self.spot_asks = json.loads(get_redis(f'SPOT_BOOK_{self.symbol}')).get('asks', None)

        if BEST_FUTURE:
            self.best_future_bids = json.loads(get_redis(f'FUTURE_TICKER_{self.symbol}')).get('b', None)
            self.best_future_asks = json.loads(get_redis(f'FUTURE_TICKER_{self.symbol}')).get('a', None)
        if BEST_SPOT:
            self.best_spot_bids = json.loads(get_redis(f'SPOT_TICKER_{self.symbol}')).get('b', None)
            self.best_spot_asks = json.loads(get_redis(f'SPOT_TICKER_{self.symbol}')).get('a', None)

    def get_dencitys_dict(self, usdt_value):
        self.update_book()
        if self.future_bids and self.future_asks and self.spot_bids and self.spot_asks:
            future_bids = list(filter(lambda x: float(x[0]) * float(x[1]) >= usdt_value, self.future_bids)) or None
            # percent_future_bids =
            future_asks = list(filter(lambda x: float(x[0]) * float(x[1]) >= usdt_value, self.future_asks)) or None
            spot_bids = list(filter(lambda x: float(x[0]) * float(x[1]) >= usdt_value, self.spot_bids)) or None
            spot_asks = list(filter(lambda x: float(x[0]) * float(x[1]) >= usdt_value, self.spot_asks)) or None

            return {'symbol': self.symbol,
                    'future_bids': future_bids,
                    'future_asks': future_asks,
                    'spot_bids': spot_bids,
                    'spot_asks': spot_asks,
                    }

    def dict_nearest_density(self, usdt_value):
        nearest_density = self.get_dencitys_dict(usdt_value)

        if isinstance(nearest_density, dict) and nearest_density.get('future_bids', None):
            price = float(nearest_density['future_bids'][0][0])
            quantity = float(nearest_density['future_bids'][0][1])
            quantity_USDT = price * quantity
            percent_to_spread = round((float(self.best_future_bids) - price) / price * 100, 1)
            nearest_density['future_bids'] = {'price': price,
                                              'quantity': quantity,
                                              'quantity_USDT': float(quantity_USDT),
                                              'percent_to_spread': percent_to_spread,
                                              }

        if isinstance(nearest_density, dict) and nearest_density.get('future_asks', None):
            price = float(nearest_density['future_asks'][0][0])
            quantity = float(nearest_density['future_asks'][0][1])
            quantity_USDT = price * quantity
            percent_to_spread = round((price - float(self.best_future_asks)) / price * 100, 1)
            nearest_density['future_asks'] = {'price': price,
                                              'quantity': quantity,
                                              'quantity_USDT': float(quantity_USDT),
                                              'percent_to_spread': percent_to_spread,
                                              }

        if isinstance(nearest_density, dict) and nearest_density.get('spot_bids', None):
            price = float(nearest_density['spot_bids'][0][0])
            quantity = float(nearest_density['spot_bids'][0][1])
            quantity_USDT = price * quantity
            percent_to_spread = round((float(self.best_spot_bids) - price) / price * 100, 1)
            nearest_density['spot_bids'] = {'price': price,
                                            'quantity': quantity,
                                            'quantity_USDT': float(quantity_USDT),
                                            'percent_to_spread': percent_to_spread,
                                            }

        if isinstance(nearest_density, dict) and nearest_density.get('spot_asks', None):
            price = float(nearest_density['spot_asks'][0][0])
            quantity = float(nearest_density['spot_asks'][0][1])
            quantity_USDT = price * quantity
            percent_to_spread = round((price - float(self.best_spot_asks)) / price * 100, 1)

            nearest_density['spot_asks'] = {'price': price,
                                            'quantity': quantity,
                                            'quantity_USDT': float(quantity_USDT),
                                            'percent_to_spread': percent_to_spread,
                                            }

        if nearest_density and usdt_value == 250000:
            self.nearest_density_250k = nearest_density
        elif nearest_density and usdt_value == 500000:
            self.nearest_density_500k = nearest_density
        elif nearest_density and usdt_value == 750000:
            self.nearest_density_750k = nearest_density
        elif nearest_density and usdt_value == 1000000:
            self.nearest_density_1m = nearest_density


INST_LIST = []

def create_instans_chartofdencitys():
    for symbol in symbol_list_all_futures_binance:
        INST_LIST.append(ChartOfDencitys(symbol))
    while True:
        for i in INST_LIST:
            i.dict_nearest_density(250000)
            i.dict_nearest_density(500000)
            i.dict_nearest_density(750000)
            i.dict_nearest_density(1000000)
        time.sleep(15)
