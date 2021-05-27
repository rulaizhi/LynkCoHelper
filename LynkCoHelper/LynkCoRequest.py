import requests
from com.uestcit.api.gateway.sdk import lynco_api_auth as authsdk

class LynkCoRequest():
    """接口请求封装类"""
    def __init__(self):
        self.__host = 'https://app-services.lynkco.com.cn'
        self.__app_key = '203760416'
        self.__app_secret = 'e1msl9aqd101gfcjpo873hrs5jg752og'
        self.__lynco_api_auth = authsdk.LyncoApiAuth(app_key = self.__app_key, app_secret = self.__app_secret)
        pass

    '''
    方法调用
    '''
    def test(self, username, password):
        # path = "?deviceType=ANDROID&password=a8c86b560495280621e587f4a7dfcdb7&username=15208110902"
        params = { 'deviceType': 'ANDROID', 'username': username, 'password': password }
        response = requests.post(self.__host + '/auth/login/login', params = params, data = {}, auth = self.__lynco_api_auth, proxies = {});
        print(response.json())
       