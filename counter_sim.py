from matplotlib.ticker import MultipleLocator
from bank import *
import matplotlib.pyplot as plt

# 要模拟的VIP柜台、存取款柜台、贷款柜台、咨询柜台数量的个数
size1 = len(vip_num)
size2 = len(save_num)
size3 = len(loan_num)
size4 = len(consult_num)
# 以下列表分别表示VIP客户、存取款客户、贷款客户、咨询客户在办理业务时的性能指标，依次是Ws, Wq, Ls, Lq
# 其中，各个性能指标为一个列表，表示不同在柜台数量时的值
vip_performance = [[0 for x in range(size1)], [0 for x in range(size1)], [0 for x in range(size1)], [0 for x in range(size1)]]
save_performance = [[0 for x in range(size2)], [0 for x in range(size2)], [0 for x in range(size2)], [0 for x in range(size2)]]
loan_performance = [[0 for x in range(size3)], [0 for x in range(size3)], [0 for x in range(size3)], [0 for x in range(size3)]]
consult_performance = [[0 for x in range(size4)], [0 for x in range(size4)], [0 for x in range(size4)], [0 for x in range(size4)]]

# 进行repeat次模拟，对结果取平均值
for x in range(repeat):
    customer_list = get_customer_list()
    calculate_leave_number(customer_list, number_num[0])  # 计算取号机的离开时间，数量为初始值
    # 对不同的VIP柜台数量进行计算，其他柜台数量为初始值
    for i in range(size1):
        calculate_leave_counter(customer_list, vip_num[i],  save_num[0], loan_num[0], consult_num[0])
        arrive_time = []
        serve_time = []
        leave_time = []
        for customer in customer_list:
            if customer.flag_vip == 1:
                arrive_time.append(customer.t_lea_number)
                serve_time.append(customer.t_ser_counter)
                leave_time.append(customer.t_lea_counter)
        vip_performance_temp = get_performance(arrive_time, serve_time, leave_time)
        for j in range(4):
            vip_performance[j][i] += vip_performance_temp[j]

    # 对不同的存取款柜台数量进行计算，其他柜台数量为初始值
    for i in range(size2):
        calculate_leave_counter(customer_list, vip_num[0],  save_num[i], loan_num[0], consult_num[0])
        arrive_time = []
        serve_time = []
        leave_time = []
        for customer in customer_list:
            if customer.flag_vip == 0 and customer.flag_counter == 1:
                arrive_time.append(customer.t_lea_number)
                serve_time.append(customer.t_ser_counter)
                leave_time.append(customer.t_lea_counter)
        save_performance_temp = get_performance(arrive_time, serve_time, leave_time)
        for j in range(4):
            save_performance[j][i] += save_performance_temp[j]

    # 对不同的贷款柜台数量进行计算，其他柜台数量为初始值
    for i in range(size3):
        calculate_leave_counter(customer_list, vip_num[0],  save_num[0], loan_num[i], consult_num[0])
        arrive_time = []
        serve_time = []
        leave_time = []
        for customer in customer_list:
            if customer.flag_vip == 0 and customer.flag_counter == 2:
                arrive_time.append(customer.t_lea_number)
                serve_time.append(customer.t_ser_counter)
                leave_time.append(customer.t_lea_counter)
        loan_performance_temp = get_performance(arrive_time, serve_time, leave_time)
        for j in range(4):
            loan_performance[j][i] += loan_performance_temp[j]

    # 对不同的咨询柜台数量进行计算，其他柜台数量为初始值
    for i in range(size4):
        calculate_leave_counter(customer_list, vip_num[0],  save_num[0], loan_num[0], consult_num[i])
        arrive_time = []
        serve_time = []
        leave_time = []
        for customer in customer_list:
            if customer.flag_vip == 0 and customer.flag_counter == 3:
                arrive_time.append(customer.t_lea_number)
                serve_time.append(customer.t_ser_counter)
                leave_time.append(customer.t_lea_counter)
        consult_performance_temp = get_performance(arrive_time, serve_time, leave_time)
        for j in range(4):
            consult_performance[j][i] += consult_performance_temp[j]

# 求平均值
for j in range(4):
    for i in range(size1):
        vip_performance[j][i] = round(vip_performance[j][i] / repeat, 4)
    for i in range(size2):
        save_performance[j][i] = round(save_performance[j][i] / repeat, 4)
    for i in range(size3):
        loan_performance[j][i] = round(loan_performance[j][i] / repeat, 4)
    for i in range(size4):
        consult_performance[j][i] = round(consult_performance[j][i] / repeat, 4)

# VIP客户在不同VIP柜台数量下的性能指标
print("vip_counter_Ws:" + str(vip_performance[0]))
print("vip_counter_Wq:" + str(vip_performance[1]))
print("vip_counter_Ls:" + str(vip_performance[2]))
print("vip_counter_Lq:" + str(vip_performance[3]))
# 存取款客户在不同存取款柜台数量下的性能指标
print("save_counter_Ws:" + str(save_performance[0]))
print("save_counter_Wq:" + str(save_performance[1]))
print("save_counter_Ls:" + str(save_performance[2]))
print("save_counter_Lq:" + str(save_performance[3]))
# 贷款客户在不同贷款柜台数量下的性能指标
print("loan_counter_Ws:" + str(loan_performance[0]))
print("loan_counter_Wq:" + str(loan_performance[1]))
print("loan_counter_Ls:" + str(loan_performance[2]))
print("loan_counter_Lq:" + str(loan_performance[3]))
# 咨询客户在不同咨询柜台数量下的性能指标
print("consult_counter_Ws:" + str(consult_performance[0]))
print("consult_counter_Wq:" + str(consult_performance[1]))
print("consult_counter_Ls:" + str(consult_performance[2]))
print("consult_counter_Lq:" + str(consult_performance[3]))

plt.figure(figsize=(22, 5))
plt.subplot(141)
plt.gca().xaxis.set_major_locator(MultipleLocator(1))
plt.title('Ws', fontsize=15)
plt.xlabel('Number of Counter', fontsize=15)
plt.ylabel('Value', fontsize=15)
plt.plot(vip_num, vip_performance[0], color='k', label='vip')
plt.plot(save_num, save_performance[0], color='r', label='save')
plt.plot(loan_num, loan_performance[0], color='g', label='loan')
plt.plot(consult_num, consult_performance[0], color='b', label='consult')
plt.legend(loc="upper right",  prop={'size': 10})

plt.subplot(142)
plt.gca().xaxis.set_major_locator(MultipleLocator(1))
plt.title('Wq', fontsize=15)
plt.xlabel('Number of Counter', fontsize=15)
plt.ylabel('Value', fontsize=15)
plt.plot(vip_num, vip_performance[1], color='k', label='vip')
plt.plot(save_num, save_performance[1], color='r', label='save')
plt.plot(loan_num, loan_performance[1], color='g', label='loan')
plt.plot(consult_num, consult_performance[1], color='b', label='consult')
plt.legend(loc="upper right",  prop={'size': 10})

plt.subplot(143)
plt.gca().xaxis.set_major_locator(MultipleLocator(1))
plt.title('Ls', fontsize=15)
plt.xlabel('Number of Counter', fontsize=15)
plt.ylabel('Value', fontsize=15)
plt.plot(vip_num, vip_performance[2], color='k', label='vip')
plt.plot(save_num, save_performance[2], color='r', label='save')
plt.plot(loan_num, loan_performance[2], color='g', label='loan')
plt.plot(consult_num, consult_performance[2], color='b', label='consult')
plt.legend(loc="upper right",  prop={'size': 10})

plt.subplot(144)
plt.gca().xaxis.set_major_locator(MultipleLocator(1))
plt.title('Lq', fontsize=15)
plt.xlabel('Number of Counter', fontsize=15)
plt.ylabel('Value', fontsize=15)
plt.plot(vip_num, vip_performance[3], color='k', label='vip')
plt.plot(save_num, save_performance[3], color='r', label='save')
plt.plot(loan_num, loan_performance[3], color='g', label='loan')
plt.plot(consult_num, consult_performance[3], color='b', label='consult')
plt.legend(loc="upper right",  prop={'size': 10})

plt.show()
