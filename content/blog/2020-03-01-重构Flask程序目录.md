---
date: 2020-03-01
title:  重构Flask目录
categories: [Python]
tags: [Python]
draft: false
---

# 摘要
随着在已有程序上扩充功能，模板、视图等文件会越来越多，给管理和命名空间带来不少麻烦。本文介绍了如何重构已有的程序目录，使她更适应于中型flask应用开发，为功能扩展做好准备。

# 原结构和缺陷
下图是现在的目录结构，主程序是app.py包含Flask初始化信息，views.py是视图，forms.py是表单，models是数据库模型，对少量页面应用来说，这种结构非常实用。一但我们想要扩展出注册登录、用户信息、通知管理、PE分析等等，这些功能都会压缩进views等文件中，每种功能的路由命名、资源管理堆叠在一个文件里，给管理带来难度。而且下次开发类似应用时，如果想复用之前的代码，需要花不少的精力去分离d代码、重新测试，不够plugin&play。

```
arbitrage/
    app/
    ├── static/
    |   |-- logo.png
    ├── templates/
    |   |-- taoli.html
    |   |-- base.html
    ├── app.py
    ├── config.py
    └── models.py
    └── views.py
    └── forms.py
```

# 引入Blueprint和新目录
Blueprint是Flask自带的资源管理插件，官网介绍是“A blueprint defines a collection of views, templates, static files and other elements that can be applied to an application”。它可以自定义一组视图、模板、静态文件等插入应用到一个程序中，可以将大型程序分割成小模块管理，每个模块都有自己对应的一组资源文件，真正可拔插，给开发、程序升级、复用代码带来很大便利。

# 目录方案1：功能视角划分
当程序不是那么大型时，可以从实用角度出发，仅在资源文件内部区分模块，各模块公用一个templates/static/views/forms/models文件/文件夹。

```
yourapp/
    __init__.py
    static/
    templates/
        home/
        control_panel/
        admin/
    views/
        __init__.py
        home.py
        control_panel.py
        admin.py
    models.py
```

# 目录方案2
另一个方案是彻底模块化，每一个模块都有自己对应的资源文件目录，完整的可插拔设计。虽然看上去有重复，但真的好用。我们将采用这种方式去重构。

```
yourapp/
    __init__.py
    admin/
        __init__.py
        views.py
        static/
        templates/
    home/
        __init__.py
        views.py
        static/
        templates/
    control_panel/
        __init__.py
        views.py
        static/
        templates/
    models.py
```    

# 重构方法
## 保持不动的文件
1. app/目录同等级的文件是运行环境配置，完全不动
1. app/内部 __init__.py 是初始化文件，位置不动，初始化需要更改为blueprint类型
1. app/内按照模块新建目录:taoli/,admin/,login/,home/,pe/等模块
1. 每个子目录内，新建static/, templates/, forms.py, views.py ，形成完整的应用目录
1. 模块较多时，可以再将模块单独放进modules/
1. app/__init__.py同级别可以放置templates/static/views.py/models.py/forms.py共享的资源
示例结构
```
yourapp/
    __init__.py
    admin/
        __init__.py
        views.py
        forms.py
        static/
        templates/
    home/
        __init__.py
        views.py
        forms.py
        static/
        templates/
    control_panel/
        __init__.py
        views.py
        forms.py
        static/
        templates/
    models.py
```
> models.py 由于管理数据库模型较少，可以公用一个，当程序规模足够大时可以进一步分离。

# Blueprint是怎样被引入和管理app的
app/__init__.py是Flask初始化文件，里面会注册Blueprint类

```
from app.views import taoli
app.register_blueprint(taoli.bp)
```

在模块初始化文件app/taoli/views/__init__.py（更大型应用会再分离views成一个个独立文件）或者模块views.py文件（中性应用直接用一个views）中，将初始化Blueprint类，并添加路由前缀，由于我们使用class类型的路由，所以使用Blueprint的add_url_rule代替Flask类。

```
from flask import Blueprint
bp = Blueprint('taoli', __name__, url_prefix='/taoli')
bp.add_url_rule('/', view_func=List.as_view('taoli_list'))
bp.add_url_rule('/top/', view_func=Top.as_view('taoli_top'))
bp.add_url_rule('/update/', view_func=Pull.as_view('taoli_update'))
```

完整的路径是: wsgi.py -> app/ -> app/__init__.py -> modules/views.py -> blueprint -> class views


# 当我们扩展已有功能时
由于引入了blueprint，views中的路径是相对路径，不需要再考虑前缀（有blueprint提前注册过了），可以在每一个模块内的views/forms扩充功能和路由，然后单独测试，也可以容易嵌入到其他程序中。

# 当我们扩展功能模块时
app/下新建模块目录以及static/templates/等资源文件，并注册blueprint，该模块就作为独立模块被引入程序，跟其他目录没有依赖关系。

# 最终的目录结构

```
├── README.md
├── app
│   ├── __init__.py
│   ├── models.py
│   ├── modules
│   │   ├── __init__.py
│   │   ├── _etf
│   │   │   └── views.py
│   │   ├── _fundamental
│   │   ├── _grid
│   │   │   └── views.py
│   │   ├── _longrun
│   │   │   └── views.py
│   │   ├── _pe
│   │   ├── _sbrotation
│   │   ├── _taoli
│   │   │   ├── static
│   │   │   ├── templates
│   │   │   │   ├── index.html
│   │   │   │   └── layout.html
│   │   │   └── views.py
│   │   ├── _targetmarket
│   │   │   └── views.py
│   │   ├── admin
│   │   ├── home
│   │   ├── login
│   │   ├── notify
│   │   │   ├── forms.py
│   │   │   ├── models.py
│   │   │   └── views.py
│   │   └── profile
│   ├── static
│   │   ├── logo.png
│   │   └── style.css
│   ├── templates
│   │   ├── base.html
│   │   └── layout.html
│   ├── utils.py
│   └── views.py
├── config.py
├── requirements.txt
└── wsgi.py

24 directories, 46 files

```

    