#!/usr/bin/python3

import requests
from com.uestcit.api.gateway.sdk import lynco_api_auth as authsdk

class lynkco_app_request():
    """接口请求封装类"""
    def __init__(self, app_key, app_secret):
        self.__host = 'https://app-services.lynkco.com.cn'
        self.__app_key = app_key
        self.__app_secret = app_secret
        self.__lynco_api_auth = authsdk.LyncoApiAuth(app_key = self.__app_key, app_secret = self.__app_secret)
        pass

    def login(self, username, password):
        """APP端登录"""
        params = { 'deviceType': 'ANDROID', 'username': username, 'password': password }
        response = requests.post(self.__host + '/auth/login/login', params = params, data = {}, auth = self.__lynco_api_auth, proxies = {});
        return response.json()
       
    def member_info(self, token, userid):
        """APP端获取用户信息（CO币余额等信息）"""
        params = { 'id': userid }
        headers = { 'token': token }
        response = requests.get(self.__host + '/app/member/service/memberInFo', params = params, data = {}, auth = self.__lynco_api_auth, proxies = {}, headers = headers);
        return response.json()

    def get_co_by_share(self, token, userid):
        """APP端每日分享获取5Co币，每天可以操作3次"""
        params = { 'accountId': userid, 'type': 3 }
        headers = { 'token': token }
        response = requests.post(self.__host + '/app/v1/task/reporting', params = params, data = {}, auth = self.__lynco_api_auth, proxies = {}, headers = headers);
        return response.json()