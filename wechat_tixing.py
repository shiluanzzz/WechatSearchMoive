# =*= coding:utf=8 =*=
# __author__ = "shitou6"
import traceback
import time
import itchat
# 登录微信
import threading
import xinfulanhai


import logging
logger=logging.getLogger(__name__) # 设置日志名称
logger.setLevel(logging.INFO) #设置日志打印等级
handler=logging.FileHandler("log.txt") # 创建日志文件
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')# 设置日志的打印格式
handler.setFormatter(formatter) #
logger.addHandler(handler)

def sendMessageToWechat(markName=u'石头', message=u'已经处理完毕'):
    '''
    markName: 微信备注的名字
    message: 要发送的内容
    eg: sendMessageToWechat(markName=u'鹏举',message=u'已经处理完毕')
    '''
    # 想给谁发信息，先查找到这个朋友
    users = itchat.search_friends(name=markName)
    if users:
        # 找到UserName
        userName = users[0]['UserName']
        itchat.send(message, toUserName=userName)
    else:
        print('通讯录中无此人')

def send_message_to_filehelper(word):
    itchat.send('{}'.format(word), toUserName='filehelper')

def auto_find_vip_movies():
    AutoSendFlag=0
    count = 1
    # 自动检测有没有新的vip电影场次 每10分钟自动检测一次
    origin_data = xinfulanhai.find_vip_movie()
    file = open("count.txt", 'w', encoding="utf8")
    while 1:
        now_data = xinfulanhai.find_vip_movie()
        if origin_data == now_data:
            if AutoSendFlag:
                send_message_to_filehelper("没有检测到会员电影场次变化 QAQ")
                file.write(count)
                count += 1
        else:
            message = "****检测到会员电影场次变化****+\n"
            for each in now_data:
                message += each
                message += "\n"
            message += "****打印完毕****"
            send_message_to_filehelper(message)

        origin_data = now_data
        now_data = None
        time.sleep(10 * 60)


@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    # if msg.actualNickName=="石头":
    if 1:
        try:
            if "1" in msg.text:
                flag = 1
                try:
                    name = str(msg.text).split(" ")[1]
                except:
                    logger.error(traceback.format_exc())
                    logger.error(traceback.format_exc())
                    flag = 0
                try:
                    count=str(msg.text).split(" ")[2]
                    count=int(count)+1
                except:
                    logger.error(traceback.format_exc())
                    count=5
                if flag:
                    string = ""
                    string += ("包含关键字 {} 的电影:\n".format(name))
                    message = xinfulanhai.find_movie(name)
                    if message:
                        for each in message:
                            keyyy = ""
                            count-=1
                            if count>0:
                                for key in each.keys():
                                    string = string + '时间:' + key + '\n=======================\n'
                                    keyyy = key
                                for values in each[keyyy]:
                                    string = string + values + "\n"

                                string += "======================="
                                string += '\n'
                    else:
                        string += "没有查询到相关电影  QAQ!"
                    send_message_to_filehelper(string)
                else:
                    send_message_to_filehelper("正确查询方式 序号+电影名称")
            elif "2" == msg.text or "会员" in msg.text:
                message = xinfulanhai.find_vip_movie()
                send_message_to_filehelper("正在查询会员场电影信息")
                send_message_to_filehelper("\n============================================\n".join(message))
            elif "3" in msg.text:
                mess = xinfulanhai.get_all_movie_names()
                send_message_to_filehelper(mess)
            elif "4" in msg.text:
                flag = 1
                try:
                    word = msg.text.split(" ")[1]
                except:
                    logger.error(traceback.format_exc())
                    flag = 0
                if flag:
                    info = xinfulanhai.get_movies_info(word)
                    if info:
                        mess = "电影:{}\n********\n类型:{}\n********\n简介：{}\n********\n".format(info['name'],
                                                                                            info['other'],
                                                                                            info['jianjie'])
                        mess += "以下为评论：\n********\n"
                        for each in info['comments']:
                            mess += each
                            mess += "\n=======================\n"
                        send_message_to_filehelper(mess)
                    else:
                        send_message_to_filehelper("没有查询到相关简介QAQ")
                else:
                    send_message_to_filehelper("正确查询方式 序号+电影名称")
            else:
                mess4 = "1. 查询电影档期\n" \
                        "2. 查询会员场信息\n" \
                        "3. 查询所有电影\n" \
                        "4. 查询电影评分\n"
                send_message_to_filehelper(mess4)
        except:
            error_message = traceback.format_exc()
            send_message_to_filehelper(error_message)


itchat.auto_login(enableCmdQR=2, hotReload=True)  # enableCmdQR在终端或命令行中为True,在notebook中为=1

t1 = threading.Thread(target=itchat.run)
t2 = threading.Thread(target=auto_find_vip_movies)
t1.start()
t2.start()
