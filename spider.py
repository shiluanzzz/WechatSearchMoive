# -*- coding:utf-8 -*-
# __author__ = "shitou6"
import json
import random
import time
import traceback

import wechat_tixing
from bs4 import BeautifulSoup
import requests
def main():
    date=[23,24,25,26,27,28]
    while 1:
        for day in date:
            time.sleep(2)
            url='https://maoyan.com/cinemas?movieId=248172&brandId=30053&showDate=2019-04-{}&hallType=-1&districtId=112'.format(day)
            USER_AGENTS = [
                        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
                        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
                        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
                        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
                        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
                        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
                        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
                    ]
            headers={'User-Agent':random.choice(USER_AGENTS)}
            with open('ip.json', 'r') as file:
                data = json.load(file)

            try:
                r = requests.get(url=url, headers=headers, proxies=random.choice(data))
                r.raise_for_status()
                soup=BeautifulSoup(r.text,'lxml')
                film=soup.find_all("div",class_="cinemas-list")[0]
                # print(film.text)
                if "没有找到相关结果" not in film.text:
                    print(" {} 号有票了！ ".format(day))
                    wechat_tixing.sendMessageToWechat(markName=u'石头123', message=" {} 号有票了！ ".format(day))
                    date.remove(day)
                else:
                    print(" {} 号还没有~~~".format(day))
            except:
                traceback.print_exc(file=open('error.txt','a+',encoding='utf8'))
                return None

if __name__ == '__main__':
    wechat_tixing.sendMessageToWechat(markName=u'石头123', message=" {} 号有票了！ ".format(123))
    main()