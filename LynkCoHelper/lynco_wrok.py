#!/usr/bin/python3

import threading
import time
import base64
from lynkco_app_request import lynkco_app_request
from com.uestcit.api.gateway.sdk.auth.aes import aes as AES

class lynco_wrok(threading.Thread):
    """新开线程处理任务"""
    def __init__(self, config, account):
        # 初始化线程
        threading.Thread.__init__(self)
        # 缓存配置信息
        self.config = config
        # 缓存账户信息
        self.account = account
        # 缓存APPKEY(因为存储的是base64后的值，所以需要base64解码一次)
        self.app_key = base64.b64decode(self.config['api_geteway']['app_key']).decode('utf-8')
        # 缓存APPSECRET(因为存储的是base64后的值，所以需要base64解码一次)
        self.app_secret = base64.b64decode(self.config['api_geteway']['app_secret']).decode('utf-8')
        # 缓存AESKEY(因为存储的是两次base64后的值，所以需要base64解码两次)
        self.aes_key = base64.b64decode(base64.b64decode(self.config['aes_key']).decode('utf-8')).decode('utf-8')
        self.AES = AES(self.aes_key)
        self.lynkco_app_request = lynkco_app_request(self.app_key, self.app_secret)
        
    def run(self):
        """线程开始的方法"""
        print ("开始执行用户：" + self.account['username'] + "的任务 " + time.strftime('%Y-%m-%d %H:%M:%S'))
        self.app_action()
        print ("用户任务执行完成：" + self.account['username'] + "的任务 " + time.strftime('%Y-%m-%d %H:%M:%S'))

    def app_action(self):
        """App端操作流程"""
        # 先进行登录（不需要缓存RefreshToken进行刷新操作，每次执行都是用登录接口皆可，后续可以根据实际情况进行缓存优化）
        response = self.lynkco_app_request.login(self.account['username'], self.AES.encrypt(self.account['password']))
        if response['code'] != 'success':
            print("APP端操作用户：" + self.account['username'] + "失败，登录失败" + time.strftime('%Y-%m-%d %H:%M:%S'))
            return False
        self.userinfo = response['data']

        # 先获取用户信息，打印用户余额
        response = self.lynkco_app_request.member_info(self.userinfo['centerTokenDto']['token'], self.userinfo['centerUserInfoDto']['id'])
        if response['code'] != 'success':
            print("APP端操作前用户：" + self.account['username'] + "获取用户信息失败 " + time.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            self.member_info = response['data']
            print("APP端操作前用户：" + self.account['username'] + "当前Co币余额为：" + self.member_info['point'] + " " + time.strftime('%Y-%m-%d %H:%M:%S'))

        # 执行3次分享操作
        for i in range(3):
            response = self.lynkco_app_request.get_co_by_share(self.userinfo['centerTokenDto']['token'], self.userinfo['centerUserInfoDto']['id'])
            # 执行分享后稍等1秒再执行下一次
            time.sleep(1)

        # 重新获取用户信息，打印用户余额
        response = self.lynkco_app_request.member_info(self.userinfo['centerTokenDto']['token'], self.userinfo['centerUserInfoDto']['id'])
        if response['code'] != 'success':
            print("APP端操作后用户：" + self.account['username'] + "获取用户信息失败 " + time.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            self.member_info = response['data']
            print("APP端操作后用户：" + self.account['username'] + "当前Co币余额为：" + self.member_info['point'] + " " + time.strftime('%Y-%m-%d %H:%M:%S'))

        print("APP端操作用户：" + self.account['username'] + "完成" + time.strftime('%Y-%m-%d %H:%M:%S'))
        return True