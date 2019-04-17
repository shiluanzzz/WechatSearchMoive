# -*- coding:utf-8 -*-
# __author__ = "shitou6"
import random
import time

from bs4 import BeautifulSoup

from AutoRequests import GetUrlContent


def do_url(url):
    try:
        a = GetUrlContent(url)
        soup = BeautifulSoup(a, "lxml")
        old_text = soup.find("p", class_="desc").text.replace(" ", "")
    except:
        old_text = " "
    for each in range(20):
        time.sleep(random.randint(1, 10))
        print("正在随机访问第", each + 1, "次")
        tt = GetUrlContent(url)
    a = GetUrlContent(url)
    try:
        soup = BeautifulSoup(a, "lxml")
        new_text = soup.find("p", class_="desc").text.replace(" ", "")
        string = (old_text, "\n\n\n", new_text)
    except:
        string = "not find this element"
    return string


if __name__ == '__main__':
    url = "https://www.maimemo.com/share/page/?uid=4203881&pid=3615f6f176cc44f53b7169a0f47e0ce3"
    do_url(url)
