import json
import threading
from .redis_db import *
import logging
import time
from binance.websocket.spot.websocket_api import SpotWebsocketAPIClient
from binance_futures.um_futures import UMFutures
from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient as Client
from binance_futures.websocket.um_futures.websocket_client import UMFuturesWebsocketClient



def all_futures_binance():
    """
    Api futures binance.
    :return: set to redis db list of dict coins's data
    """
    um_futures_client = UMFutures()
    res = um_futures_client.exchange_info()
    # print(res['symbols'])
    all_futures_symbols = []
    for i in res['symbols']:
        # print(i)
        if i['status'] == 'TRADING' and i['contractType'] == 'PERPETUAL' and i['underlyingType'] == 'COIN':
            all_futures_symbols.append(i)

    set_redis(name='all_futures_binance', value=all_futures_symbols)
#
#
symbol_list_all_futures_binance = [i['symbol'] for i in json.loads(get_redis('all_futures_binance'))]


def future_book_ticker_stream(*symbols):

    def message_handler(message):
        symbol = message.get("s", False)
        if symbol:
            name = 'FUTURE_TICKER_' + symbol
            set_redis(name=name, value=json.dumps(message))

            # print('future_book_ticker_stream', name, json.dumps(message))


    my_client = UMFuturesWebsocketClient()
    my_client.start()
    n = 1
    for symbol in symbols:
        my_client.book_ticker(
            id=n,
            callback=message_handler,
            symbol=symbol,
        )
        n +=1
        time.sleep(0.3)


def spot_symbol_ticker_streams(*symbols):

    def message_handler(_, message):

        # print(message)
        symbol = json.loads(message).get("s", False)
        if symbol:
            name = 'SPOT_TICKER_' + symbol
            set_redis(name=name, value=message)

            # print('spot_symbol_ticker_streams', name, message)

    my_client = Client(on_message=message_handler)


    for symbol in symbols:

        my_client.ticker(symbol=symbol)
        time.sleep(1)




def ws_api_futures_order_book_500(*symbols):
    """
    Websocket api futures binance.
    :param symbols: list of symbols
    :return: set to redis db order book binance futures
    """

    while True:
        um_futures_client = UMFutures()
        # for i in '12345':

        for symbol in symbols:
            order_book = um_futures_client.depth(symbol, **{"limit": 500})
            name = f'FUTURE_BOOK_{symbol}'
            set_redis(name=name, value=order_book)
            time.sleep(1)
            print(name, order_book)
        time.sleep(60)
        #     time.sleep(1)
        #     print(um_futures_client.__dict__)

def ws_api_spot_order_book_500(*symbols: list):
    """
    Websocket api spot binance.
    :param symbols: list of symbols
    :return: set to redis db order book binance spot
    """

    def on_close(_):
        logging.info("Do custom stuff when connection is closed")

    def on_ping(_):
        logging.info("ping")

    def on_pong(_):
        logging.info("pong")

    def message_handler(_, message):

        message = json.loads(message)
        # print(message)
        # print(message['rateLimits'])
        symbol = message['id']
        name = f'SPOT_BOOK_{symbol}'
        order_book = message["result"]
        set_redis(name=name, value=order_book)

        print(name, order_book)



    while True:
        my_client = SpotWebsocketAPIClient(on_message=message_handler,
                                           on_close=on_close,)
                                           # on_ping=on_ping,
                                           # on_pong=on_pong, )
        print('START ws_api_spot_order_book_500')
        for i in symbols:
            my_client.order_book(symbol=i, limit=500, id=i)

            time.sleep(1)
        my_client.stop()
        print('STOP ws_api_spot_order_book_500')
        time.sleep(120)



def start_api_ws():
    threading.Thread(target=future_book_ticker_stream, args=symbol_list_all_futures_binance).start()
    threading.Thread(target=spot_symbol_ticker_streams, args=symbol_list_all_futures_binance).start()
    threading.Thread(target=ws_api_futures_order_book_500, args=symbol_list_all_futures_binance).start()
    threading.Thread(target=ws_api_spot_order_book_500, args=symbol_list_all_futures_binance).start()
