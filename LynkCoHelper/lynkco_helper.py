#!/usr/bin/python3

import sys
import os
import json
from lynco_wrok import lynco_wrok

def main():
    # 加载应用配置
    config = json.load(open(sys.path[0] + '/config.json'))
    # 加载账号配置
    account_list = json.load(open(sys.path[0] + '/account.json'))
    # 定义线程数组
    threads = []
    # 遍历账号列表，每个账号开启一个线程进行处理
    for account in account_list:
        # 实例化
        thread = lynco_wrok(config, account)
        # 保存到线程数组
        threads.append(thread)
        # 运行线程
        thread.start()

    # 遍历线程数组，调用join方法等待线程执行完成后再退出程序
    for thread in threads:
        thread.join()
    print('执行完成')

if __name__ == '__main__':
    main()