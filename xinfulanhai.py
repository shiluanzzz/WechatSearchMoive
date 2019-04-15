# -*- coding:utf-8 -*-
# __author__ = "shitou6"
import json
import random
import time
import traceback

from bs4 import BeautifulSoup
import requests
import logging
logger=logging.getLogger(__name__) # 设置日志名称
logger.setLevel(logging.INFO) #设置日志打印等级
handler=logging.FileHandler("log.txt") # 创建日志文件
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')# 设置日志的打印格式
handler.setFormatter(formatter) #
logger.addHandler(handler)

def find_all_movies():
    movies_date = {}
    vip_days = []
    url = 'https://maoyan.com/cinema/12916?poi=4267320'
    USER_AGENTS = [
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
    ]
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    with open('ip.json', 'r') as file:
        data = json.load(file)
    try:
        r = requests.get(url=url, headers=headers, proxies=random.choice(data))
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'lxml')

        movies_id_list = soup.find('div', class_="movie-list").find_all("div", class_="movie")

        movies = soup.find_all('div', class_='show-list')
        for each in movies:  # 遍历每个电影
            dates = each.find('div', class_="show-date").find_all('span', class_="date-item")
            movie_name = (each.find('h3', class_="movie-name").get_text())
            movies_date.setdefault(movie_name, {})

            movie_info = {
                "info": str(each.find("div", class_="movie-desc").text).replace("\n", " "),
                "movie_id": movies_id_list[movies.index(each)]["data-movieid"]
            }
            movies_date[movie_name]['movie_info'] = movie_info
            plist = list(each.find_all('div', class_='plist-container'))
            movies_date[movie_name].setdefault("movies_day", [])
            for each_p in plist:  # 遍历每一天
                try:
                    movies_day = ("{}日".format(dates[plist.index(each_p)].get_text()))
                    temp_dict = {movies_day: []}
                    dangqi = each_p.find('tbody').find_all('tr')
                    for each_tr in dangqi:  # 遍历每一天的每一个档期
                        things = each_tr.find_all('td')
                        begin_time = things[0].find('span', class_='begin-time').get_text()
                        end_time = str(things[0].find('span', class_='end-time').get_text()).replace("散场", "")
                        banben = things[1].get_text()
                        ting = things[2].get_text().split('-')[0]
                        print_str = (
                            "开场：{}，结束：{}，类型：{}，大厅：{}".format(begin_time, end_time, banben, ting).replace("\n", ""))
                        # print(print_str)
                        temp_dict[movies_day].append(print_str)
                        if begin_time == "18:00":
                            vip_days.append("{} : {}, {}".format(movie_name, movies_day, print_str))
                    movies_date[movie_name]["movies_day"].append(temp_dict)
                except:
                    logger.error(traceback.format_exc())
                    pass

        movies_date.setdefault('vip', vip_days)
    except:
        logger.error(traceback.format_exc())
        file = open('error.html', 'w', encoding='utf8')
        file.write(r.text)
    return movies_date

def pretty_dict(my_dict):  # 美观打印
    # 利用json的打印 友好打印字典等结构。备用
    print(json.dumps(my_dict, ensure_ascii=False, indent=1))

def get_all_movie_names():
    data = find_all_movies()
    message = "全部电影：\n=======================\n"
    for key in data.keys():
        message += key
        message += '\n'
    return message



def func(ddd):
    data = ddd
    func_meun = """
    1.查看当前所有电影
    2.搜索电影档期
    3.搜索会员档期
    """
    print(func_meun)
    while 1:
        num = int(input("请输入数字："))
        if num == 1:
            for key in data.keys():
                print(key)
        if num == 2:
            movies_name = input("请输入电影名称")
            for key in data.keys():
                if movies_name in key or movies_name == key:
                    dd = data[key]
                    pretty_dict(dd)
        if num == 3:
            pretty_dict(data['vip'])

        flag = input("是否继续：是（Y/y）")
        if flag == 'y' or flag == 'Y':
            pass
        else:
            break
    pass

def find_movie(movie_name):
    data = find_all_movies()
    for key in data.keys():
        if movie_name in key or movie_name == key:
            dd = data[key]['movies_day']
            return dd
    return None

def find_vip_movie():
    data = find_all_movies()
    return data['vip']

def write_json():
    data = find_all_movies()
    file = open("data.json", "w", encoding='utf8')
    json.dump(data, file, ensure_ascii=False)

def get_movies_info(word):
    data = find_all_movies()
    if data:
        for keys in data.keys():
            if word in keys:
                return get_movies_info_by_id(data[keys]['movie_info']['movie_id'])
    else:
        return None



def get_movies_info_by_id(movid_id):  # 爬取电影的简介，评论等。
    url = 'https://maoyan.com/films/' + movid_id
    USER_AGENTS = [
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
    ]
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    with open('ip.json', 'r') as file:
        data = json.load(file)
    try:
        r = requests.get(url=url, headers=headers, proxies=random.choice(data))
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'lxml')
        movie_info1 = soup.find("div", class_="movie-brief-container")
        name = movie_info1.find('h3', class_="name").get_text()
        other = movie_info1.find('ul').text.replace('\n', " ")
        jianjie = soup.find('div', class_="mod-content").text
        comments_list = []
        comments = soup.find_all('li', class_="comment-container")
        for each in comments:
            comments_list.append(each.find('div', class_="comment-content").get_text())
        info = {"name": name,
                "other": other,
                "jianjie": jianjie,
                "comments": comments_list}
        return info
    except:
        logger.error(traceback.format_exc())
        return None


if __name__ == '__main__':
    # pretty_dict(find_vip_movie())

    # write_json()
    print(get_movies_info("调音"))
