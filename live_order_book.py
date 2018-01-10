import copy
import sys
from time import sleep, time

from bitstamp.wsclient import BitstampWebsocketClient


def show_realtime_orderbook(currency_pair='btcusd'):
    print('Selected pair is {}'.format(currency_pair))
    print('Establishing the connection. Wait around 30 seconds...')
    client = BitstampWebsocketClient()

    sleep(5)

    base = currency_pair[:3]
    quote = currency_pair[3:]

    client.subscribe('order_book', base, quote)

    sleep(5)

    order_book = getattr(client, 'orderbook_{}'.format(currency_pair))

    last_order_book = None
    last_time_seconds = time()
    while True:
        new_order_book = copy.deepcopy(order_book)
        if new_order_book != last_order_book:
            print('{0:.3f}'.format(1000 * (time() - last_time_seconds)), new_order_book)
            # print('\n\n\n')
            last_order_book = new_order_book
            last_time_seconds = time()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: specify the pair as parameter: btceur, eurusd, \n' +
              'xrpusd, xrpeur, xrpbtc, ltcusd, ltceur, ltcbtc, ethusd, \n' +
              'etheur, ethbtc, bchusd, bcheur, bchbtc.')
        exit(1)
    show_realtime_orderbook(sys.argv[1])
