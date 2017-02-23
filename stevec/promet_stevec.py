URL_PROMET = 'http://promet.si/dc/agg'

import simplejson
from urllib.request import urlopen


def fetch_promet():
    post = {
        u'Contents': [{u'ContentName': u'stevci'}],
        u'Language': u"sl_SI",
        u'Type': u'www.promet.si',
        u'Version': u'1.0'}

    d = simplejson.dumps(post, sort_keys=True)
    data = str.encode(d)
    u = urlopen(URL_PROMET, data)
    obfuscated_data = u.read()

    return obfuscated_data


def _loads(s):
    return simplejson.loads(s, use_decimal=True)


unicode_type = type(u'')
unichr_cast = chr


def deobfuscate(s):
    assert isinstance(s, unicode_type), 'Parameter is not unicode.'
    s2 = s[::2] + s[1::2][::-1]
    return ''.join((unichr_cast((255 - ord(c)) % 65536) for c in s2))


def _decode(s):
    if not isinstance(s, unicode_type):
        s = s.decode('utf-8')
    return deobfuscate(s)


def parse_promet(obfuscated_data):
    decoded = _decode(obfuscated_data)
    return decoded


data = fetch_promet()
full_json = parse_promet(data)

print(full_json)
