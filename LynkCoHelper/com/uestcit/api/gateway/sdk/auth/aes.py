"""
AES tools module.

Created on 5/28/2021

@author: chaisntrong
"""
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms
from Crypto.Cipher import AES
import base64
from binascii import b2a_hex, a2b_hex  

class aes():
    def __init__(self, key):
        key = key.encode('utf-8')
        self.cryptor = AES.new(key, AES.MODE_CBC, key)

    def encrypt(self, text):
        #这里密钥key 长度必须为16（AES-128）
        text = text.encode('utf-8')
        text = self.pkcs7_padding(text)
        ciphertext = self.cryptor.encrypt(text) 
        return b2a_hex(ciphertext).decode().lower()

    def decrypt(self, text):
        plain_text = self.cryptor.decrypt(a2b_hex(text))
        # return plain_text.rstrip('\0')
        return bytes.decode(plain_text).rstrip("\x01").\
            rstrip("\x02").rstrip("\x03").rstrip("\x04").rstrip("\x05").\
            rstrip("\x06").rstrip("\x07").rstrip("\x08").rstrip("\x09").\
            rstrip("\x0a").rstrip("\x0b").rstrip("\x0c").rstrip("\x0d").\
            rstrip("\x0e").rstrip("\x0f").rstrip("\x10")

    @staticmethod
    def pkcs7_padding(data):
        if not isinstance(data, bytes):
            data = data.encode()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        return padded_data

    @staticmethod
    def pkcs7_unpadding(padded_data):
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        data = unpadder.update(padded_data)
        try:
            uppadded_data = data + unpadder.finalize()
        except ValueError:
            raise Exception('无效的加密信息!')
        else:
            return uppadded_data