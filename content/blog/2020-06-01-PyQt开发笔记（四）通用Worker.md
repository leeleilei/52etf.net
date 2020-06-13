---
display: false
title: "PyQt开发笔记（四）通用的Worker"
categories: [Python]
tags: [多线程,PyQt, PySide2]
date: 2020-06-01
---

## 线程通信

概念很大，但比较容易理解。

GUI程序的核心在于交互，界面上的元素互动交互，例如鼠标移动，打飞机游戏跟着滚动，其他物品躲避。

其次是用户和界面直接的交互，比如输入一些信息、点击按钮。

这些交互被封装到QApplication主进程，其实也是有滞后的，不过循环非常快，用户感知不到明显滞后和卡顿。

当我们用了线程之后，由于是耗时操作，开始和结束时的互动就存在明显滞后。

总之，为了解决线程通信Qt的方案是捕捉信号后触发，就是Signal和Slot的概念，可以用在主线程（界面）和子线程之间，也可以用在所有线程之间。

学Qt必须要掌握的一个基本概念，理解了Signal和Slot就基本理解了Qt程序设计的基本思路。

Signal的本质是产生信号，信号的作用是继续下一步的动作（Slot），可以使任何动作，这样就将元素连接了起来。

绑定信号和Slot，用的是Signal.connect(slot_function)，普通的函数不是Slot函数，只有内置的Slot可以访问（例如点击、关闭、内容改变等等）。

但PyQt中提供了强大的Slot装饰器，可以将任何函数和类包装秤Slot。

```
@Slot()
def slot_me():
  print('i am ordinary slotted function')
```


## 通用的线程对象

多线程是如此的常见，而信号和槽位无处不在，我实在想不出Qt为什么不直接包装一个通用的对象。

既然没有，我们设计一个。底稿是，

```
class WorkerSignal(QObject):
    #一个进程结束通常有三个返回值，是否成功、报错、结果
    #注意Signal只能以QObject创建
    prog = Signal(int)
    done = Signal()
    error = Signal(tuple)
    result = Signal(QObject)
    
class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
    #我们的Worker接受任何操作
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignal()
        
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
         except:
            #捕捉到错误
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            #如果没有处罚exception，则发射结果
            self.signals.result.emit(result)
        finally:
            #无论如何告诉别人自己结束了，附带发射一波
            self.signals.done.emit()
```

通过以上的Worker和Signal设计，我们就有了一个通用的Worker可以接受任何苦力劳动，并且劳动时及时告诉老板干的怎么样。

在主线程或者其他线程中，捕捉到signal后，可以绑定signal触发下一个Slot，这个世界就被连接了起来，产生无限的可能。

## 尾声
通过理解线程的概念，可以知道Qt世界是怎么连接起来的。就像Linux设计这算，Do it right, Do it once一样，虽然功能很小，但一个PIPE |连接符，把整个Unix的文件访问输入输出全部连接了起来。 Qt的Signal和Slot也是类似的设计，简单有效。

