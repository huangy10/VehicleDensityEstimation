# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math, random
# 需要安装的库：Numpy和Matplotlib，推荐直接Anaconda
fig, axes1 = plt.subplots()
# 设置坐标轴长度
axes1.set_ylim(0, 1.4)
axes1.set_xlim(0, 1*np.pi/0.01)
# 设置初始x、y数值数组
xdata = np.arange(0, 2*np.pi, 0.01)
ydata = np.sin(xdata)
# 获得线条
line, = axes1.plot(xdata)
# 毛刺倍率，从0开始增长，offset越大毛刺越大
offset = 0.0

#因为update的参数是调用函数data_gen,所以第一个默认参数不能是framenum
def update(data):
    global offset
    line.set_ydata(data)
    return line,
# 每次生成10个随机数据
# 每次变化整幅图的话，yield一个整图就行了
def data_gen():
    global offset
    while True:
        length = float(len(xdata))
        for i in range(len(xdata)):
            ydata[i]=math.sin(xdata[i])+0.2
            if i>length/18.0 and i<(length*2.7/6.0):
                ydata[i]+=offset*(random.random()-0.5)
        offset += 0.05
        #可以设置offset的最大值
        if offset>=0.5:
           offset=0.0
        yield ydata
# 配置完毕，开始播放
ani = animation.FuncAnimation(fig, update, data_gen, interval=800, repeat=True)
plt.show()