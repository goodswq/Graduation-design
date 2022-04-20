from matplotlib.ticker import MultipleLocator
from bank import *
import matplotlib.pyplot as plt

size = len(number_num)   # 要模拟的取号机数量的个数
# 以下列表分别表示客户在取号时的性能指标，依次是Ws, Wq, Ls, Lq
# 其中，各个性能指标为一个列表，表示不同在取号机数量时的值
performance = [[0 for x in range(size)], [0 for x in range(size)], [0 for x in range(size)], [0 for x in range(size)]]

# 进行repeat次模拟，对结果取平均值
for x in range(repeat):
    customer_list = get_customer_list()     # 生成客户列表
    for i in range(size):
        # 对不同的取号机数量进行计算
        calculate_leave_number(customer_list, number_num[i])    # 计算取号机的离开时间
        arrive_time = []
        serve_time = []
        leave_time = []
        for customer in customer_list:
            if customer.flag_vip == 0:
                arrive_time.append(customer.t_arrive)
                serve_time.append(customer.t_ser_number)
                leave_time.append(customer.t_lea_number)
        # 获取性能指标
        performance_temp = get_performance(arrive_time, serve_time, leave_time)
        # 把每次模拟的性能指标相加
        for j in range(4):
            performance[j][i] += performance_temp[j]

# 求平均值
for i in range(size):
    for j in range(4):
        performance[j][i] = round(performance[j][i] / repeat, 4)

# 客户在不同取号机数量下的性能指标
print("number_Ws:" + str(performance[0]))
print("number_Wq:" + str(performance[1]))
print("number_Ls:" + str(performance[2]))
print("number_Lq:" + str(performance[3]))

plt.figure(figsize=(22, 5))
plt.subplot(141)
plt.gca().xaxis.set_major_locator(MultipleLocator(1))
plt.title('Ws', fontsize=15)
plt.xlabel('Number of Number Taking Machine', fontsize=15)
plt.ylabel('Value', fontsize=15)
plt.plot(number_num, performance[0], color='r')

plt.subplot(142)
plt.gca().xaxis.set_major_locator(MultipleLocator(1))
plt.title('Wq', fontsize=15)
plt.xlabel('Number of Number Taking Machine', fontsize=15)
plt.ylabel('Value', fontsize=15)
plt.plot(number_num, performance[1], color='r')

plt.subplot(143)
plt.gca().xaxis.set_major_locator(MultipleLocator(1))
plt.title('Ls', fontsize=15)
plt.xlabel('Number of Number Taking Machine', fontsize=15)
plt.ylabel('Value', fontsize=15)
plt.plot(number_num, performance[2], color='r')

plt.subplot(144)
plt.gca().xaxis.set_major_locator(MultipleLocator(1))
plt.title('Lq', fontsize=15)
plt.xlabel('Number of Number Taking Machine', fontsize=15)
plt.ylabel('Value', fontsize=15)
plt.plot(number_num, performance[3], color='r')

plt.show()


