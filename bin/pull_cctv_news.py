import sys
import jiagu

dest = sys.argv[1]

KEYS = "国债 债券 养老 红利 消费 5G 科技 一带一路 稳健 湾区 消费价格 通信 医疗 创业板 证券 新能源 汽车 医药 龙头 金融 人工智能 传媒 国企改革 军工 房地产 半导体 原油".split(' ')
KEYS.extend('航空 海运 交运 保险 公用 农牧 制造 券商 化工 医疗 贸易 安防 建材 房地产 旅游 金属 服务 机械 材料 民航 机场 水泥 水运 汽车 港口 煤炭 物流 环保 电信 电力 电子 石油 船舶 装修 装饰 设备 金属 通讯 酒店 银行 公路'.split(' '))
KEYS.extend('货币 利率 准备金 央行 国债 股市 政策 房地产 房产 贸易战 关税 原油 局势'.split(' '))
    

#date
from datetime import datetime, timedelta
yesterday = datetime.today() - timedelta(days=1)
yesterday = yesterday.strftime('%Y-%m-%d')
today = datetime.today().strftime('%Y-%m-%d')

#init tushare
import tushare as ts
TOKEN = '2ecdcdc049841ad3c28d13653925f79d41da86fe73dd49f5897f1ec4'
ts.set_token(TOKEN)
pro = ts.pro_api()
news = pro.cctv_news(date=yesterday.replace('-',''))


#title
title = 'CCTV新闻联播摘要{date}'.format(date=yesterday)

#content
import jiagu
reports = []
for text in news.iloc[:,2].to_list():
    reports.append(''.join(jiagu.summarize(text,2)))
content = '\r\n\r\n'.join(reports)


# keywords
text = ''.join(news.iloc[:,2].to_list())
text_keywords = jiagu.keywords(text, 7) # 关键词
text_keywords = [x for x in text_keywords if len(x)>=2]

# extend the keywords
eco_keywords = []
for k in KEYS:
    if k in content:
        eco_keywords.append(k)


#黑体强调关键字
for k in text_keywords:
    content = content.replace(k, '<span style="border-bottom:4px solid #E32636;">'+k+'</span>')

for k in eco_keywords:
    content = content.replace(k, '<span style="border-bottom:4px solid orange;">'+k+'</span>')

text_keywords.extend(eco_keywords)
keywords = ','.join(text_keywords)

tpl = '''
---
title: {title}
date: {date}
tags: [CCTV, 新闻, {keywords}]
draft: false
---
{content}
'''

md = tpl.format(
    title=title,
    date=today,
    keywords=keywords,
    content=content
)

import os.path
open(os.path.abspath(dest+title+'.md'), 'w', encoding='utf8').write(md)
