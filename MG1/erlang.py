import random
import matplotlib.pyplot as plt
import numpy as np
from performance_indicators import *


def simulate(customer_num, lmd, mu, k):
    """
    模拟排队（k阶Erlang分布）
    :param customer_num: 顾客总人数
    :param lmd: 平均到达率（人/秒）
    :param mu: 平均服务速率（人/秒）
    :param k: k阶Erlang分布
    :return: 返回一个列表，分别是Ws, Wq, Ls, Lq
    """

    # 生成每个顾客的到达时间
    arrive_time = [0]
    for i in range(1, customer_num):
        arrive_time.append(arrive_time[-1] + random.expovariate(lmd))

    # 生成每个顾客的服务时间
    serve_time = []
    # Erlang分布
    for i in range(customer_num):
        series = 0
        for j in range(k):
            series += random.expovariate(mu)
        serve_time.append(1 / k * series)

    # 计算每个顾客的离开时间
    leave_time = [0 for x in range(customer_num)]
    leave_time[0] = arrive_time[0] + serve_time[0]  # 第一个顾客
    for i in range(1, customer_num):
        if arrive_time[i] > leave_time[i-1]:    # 到达时间＞上一个顾客的离开时间，顾客不需要排队
            leave_time[i] = arrive_time[i] + serve_time[i]
        else:    # 顾客需要排队
            leave_time[i] = leave_time[i-1] + serve_time[i]

    # 返回性能指标Ws, Wq, Ls, Lq
    return get_performance(arrive_time, serve_time, leave_time)


def draw_chart(title, data, theoretical, repeat, color):
    """
    绘制折线图
    :param title: 标题
    :param data: 绘制的数据
    :param theoretical: 理论值
    :param repeat: 重复次数，即x轴范围
    :param color: 折线颜色
    """
    x = [i for i in range(1, repeat+1)]  # 点的横坐标
    plt.plot(x, data, '-', color=color)  # 折线
    plt.plot(x, [theoretical for i in range(1, repeat+1)], '-', color='k')  # 平均值的横线
    plt.xticks(size=15)
    plt.yticks(size=15)
    plt.xlabel("Repeat num", fontsize=15)  # 横坐标名字
    plt.ylabel("Value", fontsize=15)  # 纵坐标名字
    plt.title(title, fontsize=15)  # 标题


def theoretical(lmd, mu, k):
    """
    计算理论值
    :param lmd: 平均到达率（人/秒）
    :param mu: 平均服务速率（人/秒）
    :param k: k阶Erlang分布
    :return : 返回一个列表，分别是Ws, Wq, Ls, Lq的理论值
    """
    # Erlang分布
    Ws = ((1+k)*lmd) / (2*k*mu*(mu-lmd)) + 1/mu
    Wq = ((1+k)*lmd) / (2*k*mu*(mu-lmd))
    Ls = ((1+k)*lmd*lmd) / (2*k*mu*(mu-lmd)) + lmd/mu
    Lq = ((1+k)*lmd*lmd) / (2*k*mu*(mu-lmd))

    return [round(Ws, 4), round(Wq, 4), round(Ls, 4), round(Lq, 4)]


repeat = 50  # 模拟重复次数
customer_num = 1000     # 模拟总人数
lmd = 0.3   # 平均到达率
mu = 0.6    # 平均服务速率
k = 3       # Erlang分布阶数
result_list = [[], [], [], []]  # 存储每一次模拟的结果
for i in range(repeat):
    temp = simulate(customer_num, lmd, mu, k)
    for i in range(4):
        result_list[i].append(temp[i])

mean_list = []  # 存储平均值
for i in range(4):
    mean_list.append(round(np.mean(result_list[i]), 4))

theoretical_list = theoretical(lmd, mu, k)
print("-theoretical--simulation-")
print("Ws: " + str(theoretical_list[0]) + "    " + str(mean_list[0]))
print("Wq: " + str(theoretical_list[1]) + "    " + str(mean_list[1]))
print("Ls: " + str(theoretical_list[2]) + "    " + str(mean_list[2]))
print("Lq: " + str(theoretical_list[3]) + "    " + str(mean_list[3]))

plt.figure(figsize=(22, 5))
plt.subplot(141)
draw_chart("Distrabution for Ws", result_list[0], theoretical_list[0], repeat, 'r')
plt.subplot(142)
draw_chart("Distrabution for Wq", result_list[1], theoretical_list[1], repeat, 'y')
plt.subplot(143)
draw_chart("Distrabution for Ls", result_list[2], theoretical_list[2], repeat, 'g')
plt.subplot(144)
draw_chart("Distrabution for Lq", result_list[3], theoretical_list[3], repeat, 'b')
plt.show()
