import random

duration = 18000      # 生成客户持续时间(s)
lmd = 0.0082        # 客户的平均到达率
mu_number = 0.1      # 取号机的平均服务速率
mu_save = 0.0032     # 存取款业务的平均服务速率
mu_loan = 0.00072     # 贷款业务的平均服务速率
mu_consult = 0.00045  # 金融咨询业务的平均服务速率
mu_copy = 0.0333     # 复印的平均服务速率
mu_card = 0.0167     # 办卡的平均服务速率
rate_vip = 0.02      # VIP客户的概率
rate_save = 0.53     # 存取款客户的概率
rate_loan = 0.22     # 贷款客户的概率
rate_consult = 0.25  # 金融咨询客户的概率
rate_copy = 0.3      # 需要复印的概率
rate_card = 0.2      # 需要办卡的概率


class Customer(object):
    flag_vip = 0            # 0表示普通客户，1表示VIP客户
    flag_counter = 1        # 1表示存取款业务，2表示贷款业务，3表示金融咨询业务
    flag_copy = 0           # 0表示不需要复印，1表示需要复印
    flag_card = 0           # 0表示不需要办卡，1表示需要办卡
    t_arrive = 0.00         # 到达时间
    t_lea_number = 0.00     # 离开取号机的时间
    t_lea_counter = 0.00    # 离开柜台的时间
    t_lea_copy = 0.00       # 离开复印机的时间
    t_lea_card = 0.00       # 离开自助办卡机的时间
    t_leave = 0.00          # 离开银行的时间
    t_ser_number = 0.00     # 取号所需的时间
    t_ser_counter = 0.00    # 办理业务所需的时间
    t_ser_copy = 0.00       # 复印所需的时间
    t_ser_card = 0.00       # 办卡所需的时间


def get_customer_list():
    """
    生成客户（Customer类）的列表
    """
    customer_list = []
    now_time = 0    # 当前时间
    while now_time < duration:
        customer = Customer()
        # 生成到达时间
        customer.t_arrive = now_time
        now_time += random.expovariate(lmd)

        # 生成客户类型及取号时间
        if random.random() < rate_vip:
            customer.flag_vip = 1
            customer.t_ser_number = 0.00
        else:
            customer.flag_vip = 0
            customer.t_ser_number = 1 / mu_number
        # 生成办理业务类型以及办理业务时间
        counter = random.random()
        if counter < rate_save:
            customer.flag_counter = 1
            customer.t_ser_counter = random.expovariate(mu_save)
        elif counter < rate_save + rate_loan:
            customer.flag_counter = 2
            customer.t_ser_counter = random.expovariate(mu_loan)
        else:
            customer.flag_counter = 3
            customer.t_ser_counter = random.expovariate(mu_consult)
        if customer.flag_vip == 0:  # 只有普通用户才可能需要自己进行复印和办卡
            # 生成是否复印及复印时间
            if random.random() < rate_copy:   # 复印的概率为30%
                customer.flag_copy = 1
                customer.t_ser_copy = 1 / mu_copy
            # 生成是否办卡及办卡时间
            if random.random() < rate_card:   # 办卡的概率为20%
                customer.flag_card = 1
                customer.t_ser_card = 1 / mu_card
        customer_list.append(customer)  # 往列表中加入这个客户
    return customer_list
