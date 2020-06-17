---
display: false
date: 2020-06-13
title:  掌握这几个概念就可以延迟放弃matplotlib作图
categories: [Python]
tags: [matplotlib]
draft: false
---

印象中放弃过这个库数次，改用了plotly和altair的html类型作图。后来发现还是matplotlib要稳定灵活，兼容Qt程序方面也是最好的。

但有几个坑可以加速新手的放弃的意愿，

## 中文字体设置
![20200613210510](https://cdn.jsdelivr.net/gh/leeleilei/leeleilei.github.io/assets/images/20200613210510.png)

看到方格子是很脑裂的事，尤其是被Python2的Unicode摩擦过的人。

Do This
```python
# 设置matplotlib正常显示中文和负号
matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus']=False     # 正常显示负号
```

或者 Do This 单独挂载字体
```python
import matplotlib.font_manager as fm
# 设置字体路径
path = '/usr/share/fonts/truetype/SimHei.ttf'
fontprop = fm.FontProperties(fname=path, size=13)
#每一个涉及font的地方，引用fontproperties
plt.title("模型结果",fontproperties=fontprop)
plt.xlabel("X值",fontproperties=fontprop)
plt.ylabel("Y值",fontproperties=fontprop)
```

## Figure

![20200613211333](https://cdn.jsdelivr.net/gh/leeleilei/leeleilei.github.io/assets/images/20200613211333.png)

这个图比较言简意赅的说明这几个关键概念的区别。Figure就是默认的一张画布。
## Axes

Axes = Axe的复数，指x,y的Axis。
有趣的是一个Figure上可以包含多个Axes，即子图的概念。

## subplot

我们见过最多的写法是 fig, ax = plt.subplot()

subplot会返回一个tuple，(fig, ax) 默认一个figure和一个axes。当然也可以初始化nrows,ncols,zlocation，例如
```python
fig, [ax1, ax2, ax3] = plt.subplot(1,3)
```

注意并没有用
```python
fig, ax1, ax2, ax3 = plot.subplot(1,3)
```
因为tuple里面是(figure, axes)的结构，axes可以是一个或者n维的list

## plot
plot()本身是个作图函数(y, x, type, label)，跟以上概念没有关联。
当用pandas直接plot时会默认创建一系列的figure和axes，仍然建议按照fig, ax的写法遵从一致性。

## ticker
axes图上x,y axis的major_ticker和minor_ticker刻度值

## label
文字标签

## 日期的处理
这个可以劝退一半以上的使用者，因为不够智能，会导致x坐标显示失真。

跟python默认的datetime函数比较像，没理解原理怎么用都难受，还要依赖外部库，可实际上datetime的处理非常好，在复杂和易用之间取得了平衡。

一句话总结起来就是

>matplotlib转换标准datetime类后才能显示在axes上。

一般的处理步骤是
1. string 转为 datetime
2. matplotlib.dates date2num 转换成matplotlib格式
3. 作图
   
附加上刻度的调整
1. 调整显示格式
    ```python
    from matplotlib.ticker import MultipleLocator, FormatStrFormatter
    xmajorLocator = MultipleLocator(20)  # 将x主刻度标签设置为20的倍数
    xmajorFormatter = FormatStrFormatter('%1.1f')  # 设置x轴标签文本的格式
    xminorLocator = MultipleLocator(5)  # 将x轴次刻度标签设置为5的倍数
    ```
2. 日期的格式
   ```python
   mdates.DateFormatter('%Y%m%d')
   ```

## 日期的合并
除了shared坐标轴外，我们通常会遇到两个数据合集，然后共享一个时间轴，例如K线和成交量，需要画两个图，但是共享一个坐标轴。

```python
sharex=True
```

另一种暴力做法是做法是使用pandas的merge功能合并连个数据集合。


## 左右坐标轴

关键的一句是

```python
ax2 = ax.twinx()
```

用ax的twinx来创建第二个副axes，其他所有的配置是一样的。


## plot函数可以引入哪些参数
最常用的是plot(x,y,'marker-line-color')

[](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.plot.html?highlight=plot#matplotlib.pyplot.plot)

## 尾声

最最重要的，我们在使用matplotlib时以实用为第一目的，样式和格式是最不重要的事情，甚至可以忽略。

再好的图，数据才是重点，呈现出来已经达到99%的目的，至于样子臭美，见鬼去吧。

掌握了以上几个关键的matplotlib概念，至少可以延期你的放弃年头大概个把月（狗头）。

