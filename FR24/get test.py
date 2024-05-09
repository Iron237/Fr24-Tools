import requests
import json
import logging



def get_flight_data():
    
    while True:
        logging.info("开始获取航班数据")
        url = f"https://data-feed.flightradar24.com/fr24.feed.api.v1.Feed/LiveFeed"
        
        # 设置代理
        proxies = {
            "http": "http://127.0.0.1:10809",
            "https": "http://127.0.0.1:10809",
        }

        # 设置User-Agent头
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
            "Content-Type": "application/grpc-web+proto"
        }
        logging.info("正在发送请求")
        response = requests.get(url, proxies=proxies, headers=headers)
        logging.info("状态码: %s", response.status_code)
        print("状态码:", response.status_code)
        
        if response.status_code == 200:
            logging.info("请求成功，正在写入响应到文件")
            print("请求成功")
            with open('response.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            logging.info("写入完成，结束获取航班数据")
            break

        else:
            logging.error("请求失败，结束获取航班数据")
            print("请求失败")
            break

get_flight_data()
