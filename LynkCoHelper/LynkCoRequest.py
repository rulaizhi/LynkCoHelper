import requests
from com.uestcit.api.gateway.sdk import lynco_api_auth as authsdk

class LynkCoRequest():
    """接口请求封装类"""

    '''
    方法调用
    '''
    def test(self):
        host = "https://app-services.lynkco.com.cn"
        path = "/auth/login/login?deviceType=ANDROID&password=a8c86b560495280621e587f4a7dfcdb7&username=15208110902"
        response = requests.post(host + path, data = {}, auth = authsdk.LyncoApiAuth(app_key="203760416", app_secret="e1msl9aqd101gfcjpo873hrs5jg752og"));
        print(response.json())
       