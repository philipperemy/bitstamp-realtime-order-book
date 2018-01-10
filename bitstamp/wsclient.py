import json
from threading import Lock

import pusherclientb as pusherclient
import requests

PAIRS = ['btcusd', 'btceur', 'eurusd', 'xrpusd', 'xrpeur',
         'xrpbtc', 'ltcusd', 'ltceur', 'ltcbtc',
         'ethusd', 'etheur', 'ethbtc', 'bchusd',
         'bcheur', 'bchbtc']


def clean_empty(d):
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [v for v in (clean_empty(v) for v in d) if v]
    return {k: v for k, v in ((k, clean_empty(v)) for k, v in d.items()) if v}


# def update_dictionary(d1, d2):
#     dd = defaultdict(list)
#     for d in (d1, d2):
#         for key, value in d.items():
#             dd[key].append(value)
#     return dd

def update_dictionary(base_dict, update_dict):
    for key, value in update_dict.items():
        if key not in base_dict:
            base_dict[key] = update_dict[key]
        else:
            base_dict[key] = {**base_dict[key], **update_dict[key]}
    return base_dict


def merge_all(*args):
    result = {}
    for arg in args:
        none_arg = clean_empty(arg)
        result = update_dictionary(result, none_arg)
    return result


def generate_response_template():
    response = {}
    for pair in PAIRS:
        base = pair[:3]
        quote = pair[3:]

        if base not in response:
            response[base] = {}
        response[base][quote] = None
    return response


class BitstampWebsocketClient(object):
    def __init__(self, *args, **kwargs):
        self.key = 'de504dc5763aeef9ff52'  # Bitstamp pusher key.
        self.channels = {}
        self.messages = {'live_trades': ['trade'],
                         'order_book': ['data'],
                         'diff_order_book': ['data'],
                         'live_orders': ['order_created',
                                         'order_changed',
                                         'order_deleted']}
        self.lock = Lock()
        for channel in self.messages.keys():
            self.channels[channel] = []
            for pair in PAIRS:
                self.channels[channel + '_' + pair] = []

        self.lastprice_btcusd = generate_response_template()
        self.lastprice_btceur = generate_response_template()
        self.lastprice_eurusd = generate_response_template()
        self.lastprice_xrpusd = generate_response_template()
        self.lastprice_xrpeur = generate_response_template()
        self.lastprice_xrpbtc = generate_response_template()
        self.lastprice_ltcusd = generate_response_template()
        self.lastprice_ltceur = generate_response_template()
        self.lastprice_ltcbtc = generate_response_template()
        self.lastprice_ethusd = generate_response_template()
        self.lastprice_etheur = generate_response_template()
        self.lastprice_ethbtc = generate_response_template()
        self.lastprice_bchusd = generate_response_template()
        self.lastprice_bcheur = generate_response_template()
        self.lastprice_bchbtc = generate_response_template()

        self.orderbook_btcusd = generate_response_template()
        self.orderbook_btceur = generate_response_template()
        self.orderbook_eurusd = generate_response_template()
        self.orderbook_xrpusd = generate_response_template()
        self.orderbook_xrpeur = generate_response_template()
        self.orderbook_xrpbtc = generate_response_template()
        self.orderbook_ltcusd = generate_response_template()
        self.orderbook_ltceur = generate_response_template()
        self.orderbook_ltcbtc = generate_response_template()
        self.orderbook_ethusd = generate_response_template()
        self.orderbook_etheur = generate_response_template()
        self.orderbook_ethbtc = generate_response_template()
        self.orderbook_bchusd = generate_response_template()
        self.orderbook_bcheur = generate_response_template()
        self.orderbook_bchbtc = generate_response_template()

        self.openorders = generate_response_template()
        for base in self.openorders.keys():
            for quote in self.openorders[base].keys():
                self.openorders[base][quote] = {'price': {},
                                                'id': {}}
        self.pusher = pusherclient.Pusher(self.key)
        self.pusher.connect()

    def subscribe_to_all_tickers(self):
        for pair in PAIRS:
            base = pair[:3]
            quote = pair[3:]
            self.subscribe('live_trades', base, quote)

    def subscribe(self, stream, base, quote):
        print('-> subscribe({0}, {1}, {2})'.format(stream, base, quote))
        fullstream = stream + '_' + base + quote
        if base + quote != 'btcusd':  # special case for BTC/USD
            subscription_code = stream + '_' + base + quote
        else:
            subscription_code = stream
        print('Subscribed to {}'.format(subscription_code))
        self.channels[subscription_code].append(self.pusher.subscribe(subscription_code))
        for event in self.channels[subscription_code]:
            for message in self.messages[stream]:
                print('bind({0}, {1})'.format(message, getattr(self, fullstream)))
                event.bind(message,
                           getattr(self, fullstream),
                           kwargs={'base': base,
                                   'quote': quote,
                                   'messagetype': message},
                           decode_json=True)
        if stream == 'diff_order_book':
            orderbook = json.loads(requests.get(  # TODO base quote here
                'https://www.bitstamp.net/api/order_book/'))
            self.orderbook_btceur[base][quote] = orderbook

    def live_trades_btcusd(self, message, base=None, quote=None, *args, **kwargs):
        self.lastprice_btcusd[base][quote] = str(message['price'])

    def live_trades_btceur(self, message, base=None, quote=None, *args, **kwargs):
        self.lastprice_btceur[base][quote] = str(message['price'])

    def live_trades_eurusd(self, message, base=None, quote=None, *args, **kwargs):
        self.lastprice_eurusd[base][quote] = str(message['price'])

    def live_trades_xrpusd(self, message, base=None, quote=None, *args, **kwargs):
        self.lastprice_xrpusd[base][quote] = str(message['price'])

    def live_trades_xrpeur(self, message, base=None, quote=None, *args, **kwargs):
        self.lastprice_xrpeur[base][quote] = str(message['price'])

    def live_trades_xrpbtc(self, message, base=None, quote=None, *args, **kwargs):
        self.lastprice_xrpbtc[base][quote] = str(message['price'])

    def live_trades_ltcusd(self, message, base=None, quote=None, *args, **kwargs):
        self.lastprice_ltcusd[base][quote] = str(message['price'])

    def live_trades_ltceur(self, message, base=None, quote=None, *args, **kwargs):
        self.lastprice_ltceur[base][quote] = str(message['price'])

    def live_trades_ltcbtc(self, message, base=None, quote=None, *args, **kwargs):
        self.lastprice_ltcbtc[base][quote] = str(message['price'])

    def live_trades_ethusd(self, message, base=None, quote=None, *args, **kwargs):
        self.lastprice_ethusd[base][quote] = str(message['price'])

    def live_trades_etheur(self, message, base=None, quote=None, *args, **kwargs):
        self.lastprice_etheur[base][quote] = str(message['price'])

    def live_trades_ethbtc(self, message, base=None, quote=None, *args, **kwargs):
        self.lastprice_ethbtc[base][quote] = str(message['price'])

    def live_trades_bchusd(self, message, base=None, quote=None, *args, **kwargs):
        self.lastprice_bchusd[base][quote] = str(message['price'])

    def live_trades_bcheur(self, message, base=None, quote=None, *args, **kwargs):
        self.lastprice_bcheur[base][quote] = str(message['price'])

    def live_trades_bchbtc(self, message, base=None, quote=None, *args, **kwargs):
        self.lastprice_bchbtc[base][quote] = str(message['price'])

    def get_all_tickers(self):
        return merge_all(self.lastprice_btcusd,
                         self.lastprice_btceur,
                         self.lastprice_eurusd,
                         self.lastprice_xrpusd,
                         self.lastprice_xrpeur,
                         self.lastprice_xrpbtc,
                         self.lastprice_ltcusd,
                         self.lastprice_ltceur,
                         self.lastprice_ltcbtc,
                         self.lastprice_ethusd,
                         self.lastprice_etheur,
                         self.lastprice_ethbtc,
                         self.lastprice_bchusd,
                         self.lastprice_bcheur,
                         self.lastprice_bchbtc)

    def order_book_btcusd(self, message, base=None, quote=None, *args, **kwargs):
        self.orderbook_btcusd[base][quote] = message

    def order_book_btceur(self, message, base=None, quote=None, *args, **kwargs):
        self.orderbook_btceur[base][quote] = message

    def order_book_eurusd(self, message, base=None, quote=None, *args, **kwargs):
        self.orderbook_eurusd[base][quote] = message

    def order_book_xrpusd(self, message, base=None, quote=None, *args, **kwargs):
        self.orderbook_xrpusd[base][quote] = message

    def order_book_xrpeur(self, message, base=None, quote=None, *args, **kwargs):
        self.orderbook_xrpeur[base][quote] = message

    def order_book_xrpbtc(self, message, base=None, quote=None, *args, **kwargs):
        self.orderbook_xrpbtc[base][quote] = message

    def order_book_ltcusd(self, message, base=None, quote=None, *args, **kwargs):
        self.orderbook_ltcusd[base][quote] = message

    def order_book_ltceur(self, message, base=None, quote=None, *args, **kwargs):
        self.orderbook_ltceur[base][quote] = message

    def order_book_ltcbtc(self, message, base=None, quote=None, *args, **kwargs):
        self.orderbook_ltcbtc[base][quote] = message

    def order_book_ethusd(self, message, base=None, quote=None, *args, **kwargs):
        self.orderbook_ethusd[base][quote] = message

    def order_book_etheur(self, message, base=None, quote=None, *args, **kwargs):
        self.orderbook_etheur[base][quote] = message

    def order_book_ethbtc(self, message, base=None, quote=None, *args, **kwargs):
        self.orderbook_ethbtc[base][quote] = message

    def order_book_bchusd(self, message, base=None, quote=None, *args, **kwargs):
        self.orderbook_bchusd[base][quote] = message

    def order_book_bcheur(self, message, base=None, quote=None, *args, **kwargs):
        self.orderbook_bcheur[base][quote] = message

    def order_book_bchbtc(self, message, base=None, quote=None, *args, **kwargs):
        self.orderbook_bchbtc[base][quote] = message

    def diff_order_book(self, message, base=None, quote=None, *args, **kwargs):
        '''data:
           bids, asks'''
        self.diffmessage = message
        todo = '''implement a dict that has the price as index, and the side
                  and size as attribute, and copy the logic from the example
                  at bitstamp.net/websocket'''

    def live_orders(self, message, base=None, quote=None, messagetype=None,
                    *args, **kwargs):
        '''order_created, order_changed, order_deleted:
           id, amount, price, order_type, datetime'''
        message['price'] = str(message['price'])
        if messagetype == 'order_created':
            if message['price'] not in self.openorders[base][quote]['price']:
                self.openorders[base][quote]['price'][message['price']] = []
            self.openorders[base][quote]['price'][message['price']].append(
                message)
            self.openorders[base][quote]['id'][message['id']] = message
        if messagetype == 'order_changed':
            self.openorders[base][quote]['id'][message['id']] = message
            i = 0
            for order in self.openorders[base][quote]['price'][
                message['price']]:
                if order['id'] == message['id']:
                    self.openorders[base][quote]['price'][
                        message['price']][i] = message
                i += 1
                # self.open_orders[base][quote]['price']
        if messagetype == 'order_deleted':
            try:
                del self.openorders[base][quote]['id'][message['id']]
            except KeyError:
                pass
            try:
                i = 0
                for order in self.openorders[base][quote]['price'][
                    message['price']]:
                    if order['id'] == message['id']:
                        del self.openorders[base][quote]['price'][
                            message['price']][i]
                    i += 1
            except KeyError:
                pass
