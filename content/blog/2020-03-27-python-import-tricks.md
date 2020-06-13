---
display: false
title: "Note of Python import "
categories: [IT]
tags: [Python]
date: 2020-03-27
---
# Python Import

[TOC]

## 摘要
本文总结了Python import的方式和错误根因，用一句话总结：无论是相对(.././...)还是绝对路径(.间隔）导入，都取决于调用文件的命名空间是否存在，如果存在则可以引用，如果不存在则报错。

在少量文件小程序开发时，是直接运行module文件的形式，可以直接导入名字。在包开发时，要注意采用包的概念去导入本地模块。

## 假设目录结构是这样子
```
foo1
    │  bar1..py
    │  bar2.py
    │  __init__.py
    │
    └─foo2
            bar1.py
            bar2.py
            __init__.py
	|-- main.py
```

## 常见导入方式
以下几种写法从语法角度讲都正确，但从导入场景讲**有一些是不正确的**。

```
import foo
import foo.bar
from foo import bar
from foo import bar, baz
from foo import *
from foo import bar as fizz
from .foo import bar
foo = __import__("foo")
reload(foo)
```

当你被import折磨的欲仙欲死时，先要理解使用场景。就是说不同的调用方式（作为package、作为module文件、作为shell、作为Python3 -m 参数调用）创造出的namesapce（命名空间是不同的）。

#### 作为独立文件(module) 被使用
类似于在Python shell中执行导入，例如
```bash
$ Python3 bar1.py
$ Python3
> import bar1.py
```

此时，bar1.py虽然位于foo1 package内，但解释器直接调用bar1.py，故foo1命名空间（package）是不存在的，以下import是正确的
```
# main.py
import foo1
from foo1 import bar1
from foo1 import *
from foo1 import bar as fizz
# bar1.py
import bar2
from bar2 import object
from bar2 import *
from bar2 import object as object_new_name
```
以下写法是错误的，因为解释器执行时，foo1的namespace不存在。
```
#bar1.py
import .bar2 #不存在同级命名空间和父空间
import foo1.bar2 #不存在
from foo1 import bar2
```
#### 作为包或者包的一部分（子包、模块）被调用
例如main.py中导入了foo1, foo1.py导入了bar1, bar1又导入了bar2，甚至引入foo1的对象。这种方式就是作为包被连续调用，因为并没有被shell直接调用执行。此时，以下看似正确的写法就是错误的
```
# bar1.py
import bar2 #报错，提示bar2不存在，正确写法是import foo1.bar2 or import .bar2
```
以下是正确的
```
# main.py
import foo1
#bar1.py
from . import bar2
import .bar2
from .bar2 import object
import foo1.foo2.bar1 # 可以直接调用，因为foo1 namespace存在
from foo1.foo2 import bar1 #
from . import foo2.bar1
# foo2/bar1.py
from .. import bar1, bar2
```
#### 仅仅 import package
package被import后，默认只有package.__init__的初始化对象被import，其下属所有module, sub-package都没有被import，所以下面写法也会报错
```
# main.py
import foo1
foo1.bar1 #报错，因为默认module不被import，除非在foo1的__init__.py显性import
foo1.bar1.object(paras) #报错，因为bar1没有被import

```

## 相对和绝对import
当命名空间存在时，使用绝对路径和相对路径都可以，各有优劣；但当不存在时（比如直接运行模块文件、shell解释器导入），会报错。

