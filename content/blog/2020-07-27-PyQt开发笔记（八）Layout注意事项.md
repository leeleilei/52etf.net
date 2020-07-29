---
layout: post
title:  "PyQt开发笔记（八）Layout注意事项"
date: 2020-07-27
categories: [Python]
tags: [PyQt, PySide2, Python]
---

Layout类是界面布局的骨架，这个骨架遵循着一些默认行为规则。

如果不清楚这些默认行为，就会很容易放弃Qt，因为界面程序通常出现一些奇怪的现象，比如在主界面外，多次弹出对话框，界面不显示组件等等。

## 界面加载

可以直接使用Designer生成的ui文件，通过QUiTool中的QUiLoader来直接加载显示界面，继承自QMainWindow类。

也可以使用Pyside-uic来生成py文件后导入使用。

ui文件加载的QMainWindow也可以放置到parent widget内，达到界面GUI加载ui的效果。**这个效果的最重要的是**将界面组件化了，可以单独修改某一部分的界面内容，最后拼装起来。

单独组件也可以配合css设置界面风格，达到更好的管理方式。

其他加载参考：https://stackoverflow.com/questions/27603350/how-do-i-load-children-from-ui-file-in-pyside

## 界面组件的引用

导入py文件方式下，遵循uic生成的文件格式，通常是再次wrap一下，基类就是designer生成时的组件类型。

比如designer选择的组件是diaglog，则外层wrapper最好也是QDialog（当然也可以是相似Widget，因为基类都是Widget）。

而后在wrapper中直接setupUI调用ui文件的生成方法。

避免直接修改py文件的方式来编程，因为修改后，如果再次修改ui重新生成，则修改的自定义方法等都会丢失覆盖。

如果是直接使用ui文件，则更加方便，wrapper中加载UI后，可以通过self.ui属性访问所有的widget，或者通过findChildren/findChild方式来搜索Widget

综上，通常的做法都是不修改ui或者py，重新编写view视图py，在里面定义行为和信号，这样view和ui就有效的分离。

## 界面的Layout规则

所有的Container都有默认的Layout, 例如groupbox, frame等。

想要显示子widget，父widget必须有layout。

root window比较特别要有一个centralWidget，所以手工撸码需要自定义很多必要的类，
```
widget
setCentralWidget(widget)
layout
widget.setLayout(layout)
layout.addWidget(其他子组件)
```

如果发现某些个子组件widget不能正常显示到界面，又没有报错，那么一定是手工Layout出了问题。

没有找到从ui文件引用Layout的方法，可以直接在view视图中创建。

## 如何解决窗口一闪而过

在加载ui文件时，没有报错，窗口一闪而过后推出。

仔细检查代码会发现，UI被加载时出现在类的方法内，比如
```
def create_win():
    ui = QUiLoader.load(xx)
    ui.show()
```

创建本身是成功的，但因为在子方法内，ui属于namespace的局部变量，方法执行后变量销毁，所有窗口消失。

正确的做法是，将ui挂到类属性中和类保持同存亡
```
def create_win():
    self.ui = QUiLoader.load(xx)
    self.ui.show()
```

## 总结

界面显示和布局并不复杂，但不掌握基本的行为，会让初学者抓狂。

尤其是上面的第二和第四条，理解了这两条基本上就掌握了Qt的Layout布局方法。

