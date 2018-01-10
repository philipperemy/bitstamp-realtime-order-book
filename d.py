d = {'btc': {'usd': None, 'eur': '11759.09'}, 'eur': {'usd': None}, 'xrp': {'usd': None, 'eur': None, 'btc': None},
     'ltc': {'usd': None, 'eur': None, 'btc': None}, 'eth': {'usd': None, 'eur': None, 'btc': None},
     'bch': {'usd': None, 'eur': None, 'btc': None}}
e = {'btc': {'usd': None, 'eur': None}, 'eur': {'usd': None}, 'xrp': {'usd': None, 'eur': None, 'btc': None},
     'ltc': {'usd': None, 'eur': None, 'btc': None}, 'eth': {'usd': '1359.33', 'eur': None, 'btc': None},
     'bch': {'usd': None, 'eur': None, 'btc': None}}


def clean_empty(d):
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [v for v in (clean_empty(v) for v in d) if v]
    return {k: v for k, v in ((k, clean_empty(v)) for k, v in d.items()) if v}


def merge(a, b):
    result = {}
    a_no_none = dict((k, v) for k, v in a.items() if v is not None)
    b_no_none = dict((k, v) for k, v in b.items() if v is not None)
    result.update(a_no_none)
    result.update(b_no_none)
    return result


def merge_all(*args):
    result = {}
    for arg in args:
        none_arg = clean_empty(arg)
        result.update(none_arg)
    return result


print(merge_all(d, e))
