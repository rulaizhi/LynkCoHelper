"""
API_header tools module.

Created on 5/28/2021

@author: chaisntrong
"""

import requests
import json
from com.uestcit.api.gateway.sdk.util import UUIDUtil, DateUtil
from com.uestcit.api.gateway.sdk.common import constant
from com.uestcit.api.gateway.sdk.auth import md5_tool, signature_composer, sha_hmac256


class LyncoApiAuth(requests.auth.AuthBase):
    def __init__(self, app_key=None, app_secret=None):
        self.__app_key = app_key
        self.__app_secret = app_secret
        pass

    def __call__(self, request):
        
        request.headers.update(self.build_headers(request))

        return request
    
    '''
    
    '''
    def build_headers(self, request):
        header_params = list(request.headers.keys())
        headers = dict()
        headers[constant.X_CA_TIMESTAMP] = DateUtil.get_timestamp()
        headers[constant.X_CA_KEY] = self.__app_key
        headers[constant.X_CA_NONCE] = UUIDUtil.get_uuid()

        if constant.HTTP_HEADER_CONTENT_TYPE in header_params \
                and header_params[constant.HTTP_HEADER_CONTENT_TYPE]:
            headers[constant.HTTP_HEADER_CONTENT_TYPE] = request.headers[constant.HTTP_HEADER_CONTENT_TYPE]
        else:
            headers[constant.HTTP_HEADER_CONTENT_TYPE] = constant.CONTENT_TYPE_JSON

        if constant.HTTP_HEADER_ACCEPT in header_params \
                and request.headers[constant.HTTP_HEADER_ACCEPT]:
            headers[constant.HTTP_HEADER_ACCEPT] = request.headers[constant.HTTP_HEADER_ACCEPT]
        else:
            headers[constant.HTTP_HEADER_ACCEPT] = constant.CONTENT_TYPE_JSON

        if constant.POST == request.method and constant.CONTENT_TYPE_STREAM == headers[constant.HTTP_HEADER_CONTENT_TYPE]:
            headers[constant.HTTP_HEADER_CONTENT_MD5] = md5_tool.get_md5_base64_str(request.body)
            str_to_sign = signature_composer.build_sign_str(uri=request.get_url(), method=request.get_method(),
                                                            headers=headers)
        else:
            str_to_sign = signature_composer.build_sign_str(uri=request.path_url, method=request.method,
                                                            headers=headers, body=request.body)

        headers[constant.X_CA_SIGNATURE] = sha_hmac256.sign(str_to_sign, self.__app_secret)

        return headers
