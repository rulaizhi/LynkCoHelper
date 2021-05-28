"""
SHA256 tools module.

Created on 5/28/2021

@author: chaisntrong
"""

import hmac
import hashlib
import base64


def sign(source, secret):
    h = hmac.new(bytes(secret, encoding='utf-8'), bytes(source, encoding='utf-8'), hashlib.sha256)
    signature = base64.b64encode(h.digest())
    return str(signature, encoding='utf-8')


