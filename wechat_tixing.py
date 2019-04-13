# -*- coding:utf-8 -*-
# __author__ = "shitou6"
import traceback
import time
import itchat
#登录微信
import threading
import xinfulanhai

AutoSendFlag=0

def sendMessageToWechat(markName=u'石头',message=u'已经处理完毕'):
    '''
    markName: 微信备注的名字
    message: 要发送的内容
    eg: sendMessageToWechat(markName=u'鹏举',message=u'已经处理完毕')
    '''
    #想给谁发信息，先查找到这个朋友
    users = itchat.search_friends(name=markName)
    if users:
        #找到UserName
        userName = users[0]['UserName']
        itchat.send(message,toUserName = userName)
    else:
        print('通讯录中无此人')

def send_message_to_filehelper(word):
    itchat.send('{}'.format(word), toUserName='filehelper')

def test():
    count=1
    while count<10:
        time.sleep(1)
        send_message_to_filehelper('{}'.format(str(count)))
        count+=1

def auto_find_vip_movies():
    # 自动检测有没有新的vip电影场次 每10分钟自动检测一次
    origin_data=xinfulanhai.find_vip_movie()

    while 1:
        now_data = xinfulanhai.find_vip_movie()
        if origin_data==now_data:
            if AutoSendFlag:
                send_message_to_filehelper("没有检测到会员电影场次变化 QAQ")
        else:
            message="****检测到会员电影场次变化****+\n"
            for each in origin_data:
                message+=each
                message+="\n"
            message+="****打印完毕****"
            send_message_to_filehelper(message)

        origin_data = now_data
        now_data = None
        time.sleep(10 * 60)

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    try:
        if "查询电影" in msg.text:
            string=""
            name=str(msg.text).split(" ")[1]
            string+=("正在查询包含关键字 {} 的电影:\n".format(name))
            message=xinfulanhai.find_movie(name)
            if message:
                for each in message.keys():
                    string=string+'时间:'+each.replace("|","")+'\n'
                    for each2 in message[each]:
                        string=string+each2+"\n"
                    string+="============"
                    string+='\n'
            else:
                string+="没有查询到相关电影  QAQ!"
            send_message_to_filehelper(string)
        if "查询会员场" == msg.text:
            message = xinfulanhai.find_vip_movie()
            send_message_to_filehelper("正在查询会员场电影信息")
            send_message_to_filehelper("\n------\n".join(message))
        if msg.text=="更改flag":
            send_message_to_filehelper("更改成功！")

        if "功能列表查询" in msg.text:
            mess="""
            1.查询电影 + 电影名: 查询该电影的排挡（默认显示3天）
            2.查询会员场 : 打印会员优惠信息
            3.没有3...
            """
            send_message_to_filehelper(mess)
    except:
        error_message=traceback.format_exc()
        send_message_to_filehelper(error_message)



itchat.auto_login(enableCmdQR=2,hotReload=True)#enableCmdQR在终端或命令行中为True,在notebook中为-1


t1=threading.Thread(target=itchat.run)
t2=threading.Thread(target=auto_find_vip_movies)
t1.start()
t2.start()