from matplotlib.ticker import MultipleLocator
from bank import *
import matplotlib.pyplot as plt

size = len(copy_num)   # 要模拟的取号机数量的个数
# 以下列表分别表示客户在复印时的性能指标，依次是Ws, Wq, Ls, Lq
# 其中，各个性能指标为一个列表，表示不同在复印机数量时的值
performance = [[0 for x in range(size)], [0 for x in range(size)], [0 for x in range(size)], [0 for x in range(size)]]

# 进行repeat次模拟，对结果取平均值
for x in range(repeat):
    customer_list = get_customer_list()     # 生成客户列表
    calculate_leave_number(customer_list, number_num[0])  # 计算取号机的离开时间，数量为初始值
    calculate_leave_counter(customer_list, vip_num[0], save_num[0], loan_num[0], consult_num[0])  # 计算柜台的离开时间，数量为初始值
    for i in range(size):
        # 对不同的复印机数量进行计算
        calculate_leave_copy(customer_list, copy_num[i])  # 计算复印机的离开时间
        arrive_time = []
        serve_time = []
        leave_time = []
        for customer in customer_list:
            if customer.flag_copy == 1:
                arrive_time.append(customer.t_lea_counter)
                serve_time.append(customer.t_ser_copy)
                leave_time.append(customer.t_lea_copy)
        # 获取性能指标
        performance_temp = get_performance(arrive_time, serve_time, leave_time)
        # 把每次模拟的性能指标相加
        for j in range(4):
            performance[j][i] += performance_temp[j]

# 求平均值
for i in range(size):
    for j in range(4):
        performance[j][i] = round(performance[j][i] / repeat, 4)

# 客户在不同复印机数量下的性能指标
print("copy_Ws:" + str(performance[0]))
print("copy_Wq:" + str(performance[1]))
print("copy_Ls:" + str(performance[2]))
print("copy_Lq:" + str(performance[3]))

plt.figure(figsize=(22, 5))
plt.subplot(141)
plt.gca().xaxis.set_major_locator(MultipleLocator(1))
plt.title('Ws', fontsize=15)
plt.xlabel('Number of Copy Machine', fontsize=15)
plt.ylabel('Value', fontsize=15)
plt.plot(copy_num, performance[0], color='r')

plt.subplot(142)
plt.gca().xaxis.set_major_locator(MultipleLocator(1))
plt.title('Wq', fontsize=15)
plt.xlabel('Number of Number Taking Machine', fontsize=15)
plt.ylabel('Value', fontsize=15)
plt.plot(copy_num, performance[1], color='r')

plt.subplot(143)
plt.gca().xaxis.set_major_locator(MultipleLocator(1))
plt.title('Ls', fontsize=15)
plt.xlabel('Number of Number Taking Machine', fontsize=15)
plt.ylabel('Value', fontsize=15)
plt.plot(copy_num, performance[2], color='r')

plt.subplot(144)
plt.gca().xaxis.set_major_locator(MultipleLocator(1))
plt.title('Lq', fontsize=15)
plt.xlabel('Number of Number Taking Machine', fontsize=15)
plt.ylabel('Value', fontsize=15)
plt.plot(copy_num, performance[3], color='r')

plt.show()
