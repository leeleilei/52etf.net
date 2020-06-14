
#nginx docker
#docker run --name 52etf -p 80:80 -v /home/ali/52etf/:/usr/share/nginx/html:ro -v /home/ali/52etf_wexin/:/home/ali/52etf_wexin -d 52etf
#run this within in docker

import werobot

robot = werobot.WeRoBot(token='IloVeY0UjEssica1314')

keywords = {
    '当前支持的功能关键字如下':'\r\n',
    '新闻联播 或者 xwlb': '',
    '十年': '中国十年期国债收益率',
    #'全PE': 'A股等权重PE',
    #'全PB': 'A股等权重PB',
    #'输入沪深指数代码': '获取指数PE/PB分位',
}

import re
@robot.filter(re.compile("帮助"))
@robot.filter(re.compile("help", re.IGNORECASE))
def echo(message):
    return '\r\n'.join([k+': '+v for k,v in keywords.items()])


from datetime import datetime
from werobot.replies import ArticlesReply, Article
import requests

import re
@robot.filter(re.compile("新闻联播"))
@robot.filter(re.compile("xwlb", re.IGNORECASE))
def echo(message):
    reply = ArticlesReply(message=message)
    article = Article(
        title="每日新闻联播",
        description="摘要浓缩版",
        img="http://www.xinhuanet.com/video/titlepic/121059/1210599238_1588230029264_title0h.png",
        url="http://52etf.net/tags/%E6%96%B0%E9%97%BB%E8%81%94%E6%92%AD/",
    )
    reply.add_article(article)
    return reply


import re
@robot.filter(re.compile("十年"))
def echo(message):
    reply = ArticlesReply(message=message)
    article = Article(
        title="中国十年期国债收益率",
        description="精华实时更新数据",
        img="http://www.xinhuanet.com/english/2020-01/14/138702456_15789582423401n.jpg",
        url="http://52etf.net/images/cn10ybond.png",
    )
    article1 = Article(
        title="中国十年期国债收益率",
        description="精华实时更新数据",
        img="http://www.xinhuanet.com/english/2020-01/14/138702456_15789582423401n.jpg",
        url="http://52etf.net/dash/",
    )    
    reply.add_article(article)
    reply.add_article(article1)
    return reply


import os
robot.config['HOST'] = '127.0.0.1'
robot.config['PORT'] = 8080
robot.config['APP_ID'] = os.environ['APP_ID']
robot.config['APP_SECRET'] = os.environ['APP_SECRET']
robot.config['ENCODING_AES_KEY'] = os.environ['ENCODING_AES_KEY']
robot.run()
