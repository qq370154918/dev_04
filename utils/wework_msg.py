# -*- coding: utf-8 -*-
# @Time : 2020/9/17 14:29
# @Author : liang
# @Site : 
# @File : wework_msg.py
# @Software: PyCharm
import requests
import json
url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ad80a983-17f3-47e3-a3da-aadd55427811"
class WeWork_Send_Msg():

    # 文本类型消息
    def send_txt(self):
        headers = {"Content-Type": "text/plain"}
        #李晓良测试企业微信
        send_url = url
        send_data = {
            "msgtype": "text",  # 消息类型，此时固定为text
            "text": {
                "content": "深圳今日天气：32度，暴雨",  # 文本内容，最长不超过2048个字节，必须是utf8编码
                "mentioned_list": ["@all"],
                # userid的列表，提醒群中的指定成员(@某个成员)，@all表示提醒所有人，如果开发者获取不到userid，可以使用mentioned_mobile_list
                "mentioned_mobile_list": ["13163750276"]  # 手机号列表，提醒手机号对应的群成员(@某个成员)，@all表示提醒所有人
            }
        }

        res = requests.post(url=send_url, headers=headers, json=send_data)
        print(res.text)


    def send_markdown(self):
        headers = {"Content-Type": "text/plain"}
        send_url = url
        send_data = {
            "msgtype": "markdown",  # 消息类型，此时固定为markdown
            "markdown": {
                "content": "# **提醒！实时新增用户反馈**<font color=\"warning\">**123例**</font>\n" +  # 标题 （支持1至6级标题，注意#与文字中间要有空格）
                           "#### **请相关同事注意，及时跟进！**\n" +  # 加粗：**需要加粗的字**
                           "> 类型：<font color=\"info\">用户反馈</font> \n" +  # 引用：> 需要引用的文字
                           "> 普通用户反馈：<font color=\"warning\">117例</font> \n" +  # 字体颜色(只支持3种内置颜色)
                           "> VIP用户反馈：<font color=\"comment\">6例</font> \n"  # 绿色：info、灰色：comment、橙红：warning
                           "[这是一个链接](http://work.weixin.qq.com/api/doc)"
            }
        }

        res = requests.post(url=send_url, headers=headers, json=send_data)
        print(res.text)

    # 图文类型消息
    def send_text_img(self):
        headers = {"Content-Type": "text/plain"}
        send_url = url
        send_data = {
            "msgtype": "news",  # 消息类型，此时固定为news
            "news": {
                "articles": [  # 图文消息，一个图文消息支持1到8条图文
                    {
                        "title": "中秋节礼品领取",  # 标题，不超过128个字节，超过会自动截断
                        "description": "今年中秋节公司有豪礼相送",  # 描述，不超过512个字节，超过会自动截断
                        "url": "www.baidu.com",  # 点击后跳转的链接。
                        "picurl": "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
                        # 图文消息的图片链接，支持JPG、PNG格式，较好的效果为大图 1068*455，小图150*150。
                    },
                    {
                        "title": "简书 - 小啊小狼",  # 标题，不超过128个字节，超过会自动截断
                        "description": "这里是描述信息",  # 描述，不超过512个字节，超过会自动截断
                        "url": "https://www.jianshu.com/u/4e23be34d51d",  # 点击后跳转的链接。
                        "picurl": "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
                        # 图文消息的图片链接，支持JPG、PNG格式，较好的效果为大图 1068*455，小图150*150。
                    }
                ]
            }
        }

        res = requests.post(url=send_url, headers=headers, json=send_data)
        print(res.text)

if __name__ == '__main__':
    # WeWork_Send_Msg().send_markdown()
    # WeWork_Send_Msg().send_txt()
    WeWork_Send_Msg().send_text_img()