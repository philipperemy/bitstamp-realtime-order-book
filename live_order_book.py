import copy
from time import sleep, time

from bitstamp.wsclient import BitstampWebsocketClient

print('Establishing the connection. Wait around 30 seconds...')
client = BitstampWebsocketClient()

sleep(10)

target_pair = 'btcusd'

base = target_pair[:3]
quote = target_pair[3:]

client.subscribe('order_book', base, quote)

sleep(10)

order_book = getattr(client, 'orderbook_{}'.format(target_pair))

last_order_book = None
last_time_seconds = time()
while True:
    new_order_book = copy.deepcopy(order_book)
    if new_order_book != last_order_book:
        print('{0:.3f}'.format(1000 * (time() - last_time_seconds)), new_order_book)
        # print('\n\n\n')
        last_order_book = new_order_book
        last_time_seconds = time()
