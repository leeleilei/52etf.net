---
display: false
date: 2020-06-11
title:  用Python提取新闻联播摘要和关键字
categories: [Python]
tags: [摘要,CCTV,jieba,jiagu]
draft: false
---

![20200612110411](https://cdn.jsdelivr.net/gh/leeleilei/leeleilei.github.io/assets/images/20200612110411.png)

对一个业余投资爱好者来说，看新闻联播可比什么K线布林小道要有意义的多，传说会看新闻联播能少走十年弯路，我是深信不疑啊。

但我们不愿意蹲点看视频，还是文字报道读起来快，如果能有个摘要那就更好了，要是能有关键字提取，还能回顾一段时间的关键字，那岂不是时间轴都有了，啧啧，完美掌握国家政策趋势。

## 内容
由于是给hugo静态网站添加内容，按照hugo模板生成一个文件即可。

文件内容主要有两部分组成

1. 今日关键字：由全天报道的所有内容自动生成，选取今日最佳关键字。另外针对投资领域，我们把指数名称、板块和行业等也做了关键字整理，如果发现这些关键字，也做高亮提示
2. 新闻摘要：每篇报道的内容文字可能比较多，我们提取最关键的两句

新闻源采用tushare的新闻联播接口。

中文的分词和摘要采用jiagu。

## 运行环境

Github全家桶的Action功能（真香啊），可以完整打开一个docker进程。

1. 定时运行Python脚本拉取新闻数据
2. Hugo生成静态文件
3. 提交repo
  
![20200612110507](https://cdn.jsdelivr.net/gh/leeleilei/leeleilei.github.io/assets/images/20200612110507.png)

~~## 网站内容自动更新~~

~~本地定时git pull，启动docker运行hugo生成内容。~~


## 关键代码

获取新闻
```
author:公众号：结丹记事本儿
TOKEN = 'xxxx9841ad3c28d1xxx1da86fe73xxx1ec4'
import tushare as ts

ts.set_token(TOKEN)
pro = ts.pro_api()
news = pro.cctv_news(date='20200610')
```

元数据处理
```
#date
from datetime import datetime, timedelta
yesterday = datetime.today() - timedelta(days=1)
yesterday = yesterday.strftime('%Y-%m-%d')
today = datetime.today().strftime('%Y-%m-%d')

#title
title = 'CCTV新闻联播摘要{date}'.format(date=yesterday)

# keywords
text = ''.join(news.iloc[:,2].to_list())
keywords = jiagu.keywords(text, 7) # 关键词
keywords = [x for x in keywords if len(x)>=2]
keywords = ','.join(keywords)

#content
import jiagu
reports = []
for text in news.iloc[:,2].to_list():
    reports.append(''.join(jiagu.summarize(text,2)))

content = '\r\n\r\n'.join(reports)

#强调关键字
keys = keywords.split(',')
for k in keys:
    content = content.replace(k, '<span >'+k+'</span>')

for k in KEYS:
    content = content.replace(k, '<span style="border-bottom:4px solid oceanblue;">'+k+'</span>')
```

**模板写入文件**
```
tpl = '''

---
title:  {title}
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

open(title+'.md', 'w').write(md)
```

**Github ci文件**

主要用到hugo, git的一些镜像配置，可以在github的market上搜索。

```
# This workflow will install Python dependencies, run tests and lint with a single version of Python
# For more information see: https://help.github.com/actions/language-and-framework-guides/using-python-with-github-actions

name: 更新新闻联播

on:
#  push:
#    branches: [ master ]
#  pull_request:
#    branches: [ master ]
  schedule:
    - cron: '*/3 * * * *'
  watch:
    types: started      

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python 3.8
        uses: actions/setup-python@v2
        with:
          python-version: 3.8

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install tushare jiagu 
          if [ -f bin/requirements.txt ]; then pip install -r bin/requirements.txt; fi

      - name: pull yesterday cctv news
        run: |
          # stop the build if there are Python syntax errors or undefined names
          python3 bin/pull_cctv_news.py 'content/news/'


      - uses: EndBug/add-and-commit@v4
        with:
          add: '.'
          force: true
          author_name: 52etf.net
          author_email: admin@52etf.net
          message: "日更一卒"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - uses: actions/checkout@v2
        with:
          submodules: true  # Fetch Hugo themes (true OR recursive)
          fetch-depth: 0    # Fetch all history for .GitInfo and .Lastmod

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: 'latest'
          # extended: true

      - name: Build
        run: hugo --minify

      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          PUBLISH_BRANCH: gh-pages
          publish_dir: ./public


```

## 远端服务器配置

仅仅需要在cron中添加一个git pull的每分钟更新任务

gh-pages是action模板里的配置，需要切换到对应gh-pages分支
为了避免本地文件污染，同步前git reset先自毁本地更新

```
*/1 * * * * cd /home/ali/52etf;git checkout gh-pages;git fetch --all;git reset --hard origin/gh-pages;git pull
```

本地docker服务，nginx映射52etf的目录（对应远端git分支gh-pages内容）
```
docker run --name 52etf-nginx -p 80:80 -v /home/ali/52etf/:/usr/share/nginx/html:ro -d nginx
```

## 尾声

用Github提供的Action服务，可以一条龙编译部署新闻联播采集脚本。远端服务器只需要同步编译后的内容即可。

静态网站返璞归真，无论效率、SEO还是内容管理上都很有优势。如果采用动态后台Python开发，甚至现在流行的前端React开发，都达不到这个效果。React更多用在前端存在交互频繁的网页甚至小型app上比较占优势。

每种技术都有一定局限性，挑选场景合适的工具才是最合适的方案。

可以是一种混合模式
1. 后端Python FastApi
2. 网站静态hugo
3. 部分动态内容js来控制
4. 对于单页面交互网页，或者复杂的交互应用用React
5. 手机app可以用React（如果互动频繁）


