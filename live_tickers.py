from time import sleep

from bitstamp.wsclient import BitstampWebsocketClient

print('Establishing the connection. Wait around 30 seconds...')
client = BitstampWebsocketClient()

sleep(10)

client.subscribe_to_all_tickers()
# client.subscribe("live_trades", "btc", "eur")

# this will update client.last_price["btc"]["eur"]
# client.subscribe("order_book", "btc", "usd")  # choose either this one, for accuracy

# client.subscribe("live_orders", "eur", "usd")
# this will keep self.open_orders["eur"]["usd"] up to date, and stores open orders
# by id and by price
sleep(10)

previous_values = ''
steps = 0
while True:
    cur_value = client.get_all_tickers()
    if str(previous_values) != str(cur_value):
        previous_values = cur_value
        steps += 1
        print(steps, cur_value)  # pprint(cur_value, indent=4)
