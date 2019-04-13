# -*- coding:utf-8 -*-
# __author__ = "shitou6"
import traceback

import itchat
#登录微信

import xinfulanhai
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
    except:
        error_message=traceback.format_exc()
        send_message_to_filehelper(error_message)


itchat.auto_login(enableCmdQR=False,hotReload=True)#enableCmdQR在终端或命令行中为True,在notebook中为-1

itchat.run()