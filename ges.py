import copy
from time import sleep, time

from bitstamp.wsclient import BitstampWebsocketClient

print('Establishing the connection. Wait around 30 seconds...')
client = BitstampWebsocketClient()

sleep(10)

# this will update client.lastprice["btc"]["eur"]
client.subscribe("order_book", "btc", "usd")  # choose either this one, for accuracy

sleep(10)

last_order_book = None
last_time_seconds = 0
while True:
    new_order_book = copy.deepcopy(client.order_book)
    if new_order_book != last_order_book:
        print('{0:.3f}'.format(1000 * (time() - last_time_seconds)), new_order_book)
        print('\n\n\n')
        last_order_book = new_order_book
        last_time_seconds = time()
