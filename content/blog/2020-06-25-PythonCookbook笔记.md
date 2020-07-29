#! https://zhuanlan.zhihu.com/p/158765587
---
title:  "PythonCookbook笔记"
date: 2020-06-25T10:53:40+08:00
tags: [Python,笔记]
comment: true
---

**转载请注明微*信公众号：结丹记事本儿，关注有惊喜哦！**

Python Cookbook是一本类参考书，非常适合作为案头参考。

不用很全面深入的掌握，但需要知道这些更pythonic的用法，合适的时候尝试去用，代码就会越来越好。

## 数据结构和算法
1. *args, var = [1,2,3,4] 变长展开赋值
2. heapq.nlargest, nsmallest接收key作为排序对象
3. heqpq.heappush, heappop可以实现优先级压入栈和提取
4. collection.defaultdict(list),创建对应多值的k,v 对
5. d1.keys() - d2.keys(), -是集合操作，健集合支持-&|+等集合操作
6. 用命名切片 s1 = slice(12,30), string1[s1]，让代码更具可读性
7. 统计次数, collections.Counter, Counter.most_commont(3)
8. 对字典排序，输入keys=lambda x: x['key']，其实可以简化为operator.itemgetter('key1', 'key2' ... )
9. 对class类型排序，sorted(key=lambda u: ...) 在lambda中定义排序的字段 或者 operator.attrgetter
10. itertools.groupby对dict进行分组
11. 复杂的过滤时采用filter(func, values), func中定义true时保留的value
12. 创建一个字典的子集，用到keys的集合操作 {key:prices[key] for key in prices.keys() & tech.keys() }
13. 通过下标名称访问tuple和list，相比较于于class，更简洁, collections.namedtuple('Subscriber', ['addr', 'joined'])
14. 合并两个字典, collections.ChainMap, 或者使用dict.update方法，还记得class.__dict__.update(attr)吗？


## 字符串
1. 匹配文件名，可以用re.match，但更简便的是fnmatch.fnmatch, fnmatchcase
2. 简单的匹配，'' in ''', find(), replace, startwith, endwith (不建议切片)
3. re匹配换行符，可以用\n，推荐用re.DOTALL表示匹配任意字符包括换行
4. 对字符串批量的替换，正确姿势是translate(map_dict),
5. 对其字符串,ljust, rjust, center, format(:>10, :<10>)等
6. 用join来替代+连接符，+会创建对象并删除，开支很大
7. 替换html tag，html.escape()
8. 关于文本解析的关键字是PyParsing, Ply, BNF, EBNF，类似一个数据解析器，读取固定格式

## 数字和时间

1. 浮点金融计算请用decimal模块
2. 复数complex(2,4) or (2-4j), 运算用cmatch, sin/cos/exp
3. 分数用fractions.Fraction
4. random.choice, sample(vlaues, N), .shuffle(values), randomint(start, end), radom()浮点数. random随机并不是真随机，因为有seed指示，可以用ssl.RAND_bytes()来获取
5. 时间函数datetime, timedelta, pytz.TimeZone, astimezone

## 迭代和生成器

1. yield 和 iter用来创建函数和类的迭代，节约开支
2. 反响迭代reversed()和__reversed__()
3. 迭代器的切片，itertools.islice(c, startN, endN)
4. 跳过一些行，文件操作中非常常用itertools.dropwhile(lambda line: line.startwith('#'), f)
5. chain，简单的sequence合并链接，开支很小，输出是一个迭代器
6. 生成器是python的一个优良特性，原则上来说每个for循环的地方都可以优化generator
7. yieldfrom 递归生成器
8. heapq.merge(seq1, seq2) 递归合并的序列，开支非常小
9. 迭代器替代while无限循环，非常pythonic的用法, for chunk in iter(lambda: f.read(10), b''), iter用一个callable和结尾，创建一个可结束的（退出机制）的迭代器

**转载请注明微*信公众号：结丹记事本儿，关注有惊喜哦！**

## 文件
1. print('hi', file=f) 可以将输出重定向，更轻量级的logger
2. print(a, b, c, spe=',', end='\n')
3. open(fname, 'xt'), x表示不存在时才创建文件，否则报错
4. 固定长度读取迭代, iter(functools.patial(fp, SIZE))

## 编码
1. import csv, 用NamedTuple来访问 NamedTuple('row', *headers), row = Row(*line) or csv.DictReader(fp)
2. bin2ascii.b2a_hex, a2b_hex, base64.encode, decode, 
3. 二进制数据的读取和写入暂时跳过，应用场景比较少，上次还是在解析爱立信设备的数据文件，可以自己开发解码文件
4. type元类的cls, metaclass, getattr, setattr 动态的和子类、instance互动

## 函数
1. python3.x中加入了类型检查和函数注解，支持渐进式检查，可以用在基础的类型检查上，比如关键参数和输出。同时可以学习较复杂的类型检查。
2. partial(func, arg), 用来修正func的接受缺失的参数的个数
3. 闭包和回调函数,用decoration解决更优雅

## 类
4. __repr__, __str__ 方法
5. __enter__, __exit__ 让一个类支持with上下文语法
6. __slots__ = ['year', 'month', 'day'] 用来节约大量的开支，
7. __handler, _handler 首选后者，除非想进一步隐藏和禁止instance覆盖。 handler_ 用来避免方法重叠
8. @property.getter, .setter, deleter, @property
9. super()表示父类的方法，通常初始化时会super().__init__ 确保父类初始化成功
10. collections中有大量的抽象数据结构和操作集合
11. getattr(cls, 'name')(*args, **kwargs) ，也可以operator.methodcaller('name', *args)(cls)
12. points.sort(key=operator.methodcaller('distance', 0, 0)), 变相的实现了多次执行对象的方法
13. 观察者模式: class基类实现通用的handler，来执行getattr；子类中定义getattr的具体实现，相当于对自身做了抽象，利用父类去提炼了共性handler。避免了判断handler name然后去执行，节省了if/else，从而直接去掉用，出错用raise捕捉
14. 让类支持eq、gt、lt、or、ge，使用functools.total_ordering + 其中一个，便能简化
15. 


## 元编程
1. 操控函数和类的源代码，使用装饰器、类装饰器、元类、签名对象、反射、exec
2. class handler, @classmethod, @staticmethod区别: 前者是实例的方法，第一个参数是self实例，中间是__new__/__init__之前的方法代表class本身，第一个参数必须指定为cls代表类自身，用作初始化前的类本身和环境参数的交互判断，或者逆向想要绕过__init__方法；由于发生在__init__前所以只能够调用其他的@classmethod（实例方法还未来得及实例化）；@staticmethod返回的永远是一个cls的函数（可以理解为class的私有函数，不会实例化，不会被重写，但可以改写为@classmethod). @classmethod增加实例化的判断，比如被基类、还是子类，可以调用子类的@classmethod。https://www.zhihu.com/question/20021164， https://zhuanlan.zhihu.com/p/28010894
3. functools.wraps 来保留decorator的元信息 def decor(func): @wraps(func) def wrapper(*args, **kwargs): return func(*args, *kwargs) return wrapper.
4. 如果decorator接受参数输入，因为@decorator, func() = decorator(func) = decorator(x,y,z)(func), 故decorator(x,y,z) 必须是一个decorator，所以要在上例3的基础上外层再包装一个decorator， return 内层实际的decorator
5. 带可选参数的decorator, 在函数章节的一个特性 decorator(func=None, *, arg1=xx, arg2=xx): if func=None return partial(decorator, arg1=xx, arg2=xx, arg3=xx)，对参数进行了截断处理，返回函数本身，然后再次运行一次。
6. @classmethod @normal_decorator @staticmethod的顺序有要求，meta method放置在外层，因为不能被实例化被调用，只能调用别人或者其他meta method
7. 类的调用：实例化、__new__/@classmethod、@staticmethod，也就是除了第一种之外，还有两种访问。或者禁止第一种，强制要求第二三种访问。
8. 捕捉类属性创建的顺序, __prepare__ 在类被创建之前进行检查，__setitem__进行设置和报错
9. 给元类添加可选参数，需要了解类创建的所有步骤，__new__, __init__初始化时强制类型参数 __new__(cls, name, bases, *, arg1=xx, arg2=xx) ...
10. 用函数生成函数，自定义函数名和handler，类似class工厂模式。对类进行再次抽象。types.new_class(cls_name, (bases), {'metaclass': abc.ABCMeta, lambda ns: ns.update(cls_dict)})
11. 看cookbook的样例能感觉到生产代码对逻辑的抽象层次非常的高，高到变量名字都失去了场景意义，而作为一个通用的组件。问题本身就是对场景的抽象。
12. from contextlib import contextmanager用来快速装饰一个含有yield的函数或者类，替代__entry__ , __exit__ 方法

## 模块和包
1. module或者__init__中的__all__ 用来限定导入命名控件的集合，有些时候可以屏蔽掉不必要的变量
2. 读取package中的一些数据 data = pkgutil.get_data(__package__, 'somedata.dat')
3. sys.path.extend，可以临时解决开发包不能被import的现象
4. 通过字符串导入包, importlib.import_module('math') 类似动态创建类type.new_class(cls, name, bases, *, arg1=x...)
5. 整体来看，理解了命名控件和__init__原理，就基本解决了99的导入问题

**转载请注明微*信公众号：结丹记事本儿，关注有惊喜哦！**

## 网络
1. ipaddress处理一些关于IP地址的运算，可以用作开发小工具
2. hmac.new 来用签字一个hash和digest
## 并发
1. 原始的多线程创建，但要注意LOCK/q方法都不是线程安全的，没有互斥和琐机制，容易导入读写混乱。
2. 最贱的写法是用Queen来共享一个对象读写，同时用with xx.lock() 来控制敏感共享数据读写
3. concurrent.PoolThreadExecutor用来创建一个pool.map(func, values)

整体比较适合有经验的中级开发者，越往后越抽象，尤其是函数和类、元类、线程章节，属于高级内容。

值得一段时间练习后反复阅读。

