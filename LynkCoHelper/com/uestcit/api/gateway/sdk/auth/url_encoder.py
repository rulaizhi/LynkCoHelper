"""
url_encoder tools module.

Created on 5/28/2021

@author: chaisntrong
"""

import urllib
import sys


def get_encode_str(params):
    list_params = sorted(params.iteritems(), key=lambda d: d[0])
    encode_str = urllib.urlencode(list_params)

    if sys.stdin.encoding is None:
        res = urllib.quote(encode_str.decode('cp936').encode('utf8'), '')
    else:
        res = urllib.quote(encode_str.decode(sys.stdin.encoding).encode('utf8'), '')
    res = res.replace("+", "%20")
    res = res.replace("*", "%2A")
    res = res.replace("%7E", "~")
    return res
