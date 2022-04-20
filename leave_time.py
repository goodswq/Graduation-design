def caculate_leave(customer_list, number_num, vip_num, save_num, loan_num, consult_num, copy_num, card_num):
    """
    依次计算所有阶段的离开时间
    """
    calculate_leave_number(customer_list, number_num)
    calculate_leave_counter(customer_list, vip_num, save_num, loan_num, consult_num)
    calculate_leave_copy(customer_list, copy_num)
    calculate_leave_card(customer_list, card_num)
    customer_list.sort(key=lambda c: c.t_arrive)


def calculate_leave_number(customer_list, desk_num):
    """
    计算离开取号机的时间
    采用自主排队的模式，即客户会选择所有队列中人数最少的队列排队
    """
    desk_queue = [[] for i in range(desk_num)]

    for customer in customer_list:
        arrive_time = customer.t_arrive
        if customer.flag_vip == 1:
            customer.t_lea_number = arrive_time
        else:
            for queue in desk_queue:
                while len(queue) != 0 and queue[0].t_lea_number <= arrive_time:
                    queue.pop(0)
            min_queue = get_min_queue(desk_queue)
            min_queue.append(customer)
            if len(min_queue) == 1:
                customer.t_lea_number = arrive_time + customer.t_ser_number
            else:
                customer.t_lea_number = min_queue[-2].t_lea_number + customer.t_ser_number
        customer.t_leave = customer.t_lea_number


def calculate_leave_counter(customer_list, vip_desk_num, save_desk_num, lone_desk_num, consult_desk_num):
    """
    计算离开柜台的时间，分为存取款、贷款、金融咨询和VIP柜台
    柜台采用叫号模式，即客户会被安排至选择最早结束排队的柜台
    """
    vip_desk_leave = [0 for x in range(vip_desk_num)]  # 每个服务台当前顾客的离开时间
    save_desk_leave = [0 for x in range(save_desk_num)]  # 每个服务台当前顾客的离开时间
    loan_desk_leave = [0 for x in range(lone_desk_num)]  # 每个服务台当前顾客的离开时间
    consult_desk_leave = [0 for x in range(consult_desk_num)]  # 每个服务台当前顾客的离开时间
    for customer in customer_list:
        if customer.flag_vip == 1:
            vip_desk_leave.sort()
            if customer.t_lea_number > vip_desk_leave[0]:  # 到达时间＞desk_leave[0]，顾客不需要排队
                customer.t_lea_counter = customer.t_lea_number + customer.t_ser_counter
            else:  # 顾客需要排队
                customer.t_lea_counter = vip_desk_leave[0] + customer.t_ser_counter
            vip_desk_leave[0] = customer.t_lea_counter
        elif customer.flag_counter == 1:
            save_desk_leave.sort()
            if customer.t_lea_number > save_desk_leave[0]:  # 到达时间＞desk_leave[0]，顾客不需要排队
                customer.t_lea_counter = customer.t_lea_number + customer.t_ser_counter
            else:  # 顾客需要排队
                customer.t_lea_counter = save_desk_leave[0] + customer.t_ser_counter
            save_desk_leave[0] = customer.t_lea_counter
        elif customer.flag_counter == 2:
            loan_desk_leave.sort()
            if customer.t_lea_number > loan_desk_leave[0]:  # 到达时间＞desk_leave[0]，顾客不需要排队
                customer.t_lea_counter = customer.t_lea_number + customer.t_ser_counter
            else:  # 顾客需要排队
                customer.t_lea_counter = loan_desk_leave[0] + customer.t_ser_counter
            loan_desk_leave[0] = customer.t_lea_counter
        elif customer.flag_counter == 3:
            consult_desk_leave.sort()
            if customer.t_lea_number > consult_desk_leave[0]:  # 到达时间＞desk_leave[0]，顾客不需要排队
                customer.t_lea_counter = customer.t_lea_number + customer.t_ser_counter
            else:  # 顾客需要排队
                customer.t_lea_counter = consult_desk_leave[0] + customer.t_ser_counter
            consult_desk_leave[0] = customer.t_lea_counter
        customer.t_leave = customer.t_lea_counter


def calculate_leave_copy(customer_list, desk_num):
    """
    计算离开复印机的时间
    采用自主排队的模式，即客户会选择所有队列中人数最少的队列排队
    """

    # 由于可能会出现先开始办业务但后办理完的情况，t_lea_counter不一定递增，因此根据其把customer_list重新排序
    customer_list.sort(key=lambda c: c.t_lea_counter)

    desk_queue = [[] for i in range(desk_num)]
    for customer in customer_list:
        arrive_time = customer.t_lea_counter
        if customer.flag_copy == 0:
            customer.t_lea_copy = arrive_time
        else:
            for queue in desk_queue:
                while len(queue) != 0 and queue[0].t_lea_copy <= arrive_time:
                    queue.pop(0)
            min_queue = get_min_queue(desk_queue)
            min_queue.append(customer)
            if len(min_queue) == 1:
                customer.t_lea_copy = arrive_time + customer.t_ser_copy
            else:
                customer.t_lea_copy = min_queue[-2].t_lea_copy + customer.t_ser_copy
        customer.t_leave = customer.t_lea_copy


def calculate_leave_card(customer_list, desk_num):
    """
    计算离开办卡机的时间
    采用自主排队的模式，即客户会选择所有队列中人数最少的队列排队
    """

    # 由于部分人不需要复印，t_lea_copy不一定递增，因此根据其把customer_list重新排序
    customer_list.sort(key=lambda c: c.t_lea_copy)

    desk_queue = [[] for i in range(desk_num)]
    for customer in customer_list:
        arrive_time = customer.t_lea_copy
        if customer.flag_card == 0:
            customer.t_lea_card = arrive_time
        else:
            for queue in desk_queue:
                while len(queue) != 0 and queue[0].t_lea_card <= arrive_time:
                    queue.pop(0)
            min_queue = get_min_queue(desk_queue)
            min_queue.append(customer)
            if len(min_queue) == 1:
                customer.t_lea_card = arrive_time + customer.t_ser_card
            else:
                customer.t_lea_card = min_queue[-2].t_lea_card + customer.t_ser_card
        customer.t_leave = customer.t_lea_card


def get_min_queue(desk_queue):
    """
    获取各个排队队列desk_queue中，排队人数最少的队列
    """
    min_len = len(desk_queue[0])
    min_desk = 0
    for i in range(1, len(desk_queue)):
        if min_len == 0:
            break
        if len(desk_queue[i]) < min_len:
            min_len = len(desk_queue[i])
            min_desk = i

    return desk_queue[min_desk]
