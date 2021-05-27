# -*- coding:utf-8 -*-
#  Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# coding=utf-8

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
