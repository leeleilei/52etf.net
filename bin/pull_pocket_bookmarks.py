'''
从pocket下载我的收藏夹信息里面标记为52etf的书签，并写入到52etf仓库文件中。
hugo模板将这些文件渲染成页面item呈现出来，效果是reddit的列表样式，并且可以进入讨论。

'''
import requests as req
import sys
import os

try:
    dest = sys.argv[1]
except IndexError:
    dest = 'content/bookmarks/'

tpl = '''---
title:  {title}
itemurl: {url}
date: {date}
tags: [文摘]
draft: false
---

{summary}
'''

# 处理时间
from datetime import (datetime, timedelta)
import pytz
china_tz = pytz.timezone("Asia/Shanghai")
today = datetime.now().astimezone(china_tz).isoformat()


# pocket 请求头
# count=20, run this every 30 minutes, so 20 is fair enough to capture all udpate

params = {
            'access_token': '04bb4c80-b441-5012-8e75-c397af',
            'consumer_key': '92001-aec2193a4a3516efe355ebfb',
            'tag': '52etf',
            'count': 20,}

# 请求地址
bookmarks_url = "https://getpocket.com/v3/get"
result = req.post(bookmarks_url, params= params)
urls = result.json()['list']

for k, item in urls.items():
    title = item['resolved_title']
    url = item['resolved_url']
    summary = item['excerpt']
    id = item['resolved_id']
    fname = os.path.abspath(os.path.join(dest, id+'.md'))

    content = tpl.format(
        title=title,
        url = url,
        summary = summary,
        date = today
    )

    import os
    if title and (not os.path.exists(fname)):
        open(fname, 'w', encoding='utf8').write(content)
        print('已保存{}'.format(title))
