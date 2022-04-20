def get_performance(arrive_time, serve_time, leave_time):
    """
     计算平均逗留时间Ws、平均排队时间Wq、平均顾客人数Ls、平均排队队长Lq
     :param arrive_time: 到达时间列表
     :param serve_time: 服务时间列表
     :param leave_time: 离开时间列表
     :return: 返回一个列表，分别是Ws, Wq, Ls, Lq
     """
    total_num = len(arrive_time)  # 模拟总人数

    if total_num == 0:
        return [0, 0, 0, 0]
    # 计算平均逗留时间
    total_Ws = 0
    for i in range(total_num):
        total_Ws += leave_time[i] - arrive_time[i]
    Ws = total_Ws / total_num

    # 计算平均排队时间
    total_Wq = 0
    for i in range(total_num):
        total_Wq += leave_time[i] - arrive_time[i] - serve_time[i]
    Wq = total_Wq / total_num

    total_time = int(leave_time[-1]) + 1  # 模拟总时长

    # 计算平均排队队长
    a = 0  # arrive_time的指针
    b = 0  # serve_start的指针
    queue_length = 0  # 每个时刻的队长
    total_Lq = 0  # 每个时刻队长的总和
    serve_start = [leave_time[i] - serve_time[i] for i in range(total_num)]  # 每位顾客结束排队开始服务的时间
    arrive_time.sort()
    serve_start.sort()
    for time in range(total_time):
        while a < total_num and time >= arrive_time[a]:
            # 当前时刻>=arrive_time[a]，表示这一秒内有顾客到达，则队长+1，且指针后移一位
            # 当a到达arrive_time的末尾，或者arrive_time[a]不在这一秒内，循环结束
            queue_length += 1
            a += 1
        while b < total_num and time >= serve_start[b]:
            # 当前时刻>=serve_start[a]，表示这一秒内有顾客结束排队，则队长-1
            # 当b到达serve_start的末尾，或者serve_start[b]不在这一秒内，循环结束
            queue_length -= 1
            b += 1
        total_Lq += queue_length
    Lq = total_Lq / total_time  # 计算平均值

    # 计算平均顾客人数
    leave_time.sort()  # 把离开时间队列升序排序
    a = 0  # arrive_time的指针
    b = 0  # leave_time的指针
    customer_moment = 0  # 每个时刻的顾客人数
    total_Ls = 0  # 每个时刻顾客人数的总和
    for time in range(total_time):
        while a < total_num and time >= arrive_time[a]:
            customer_moment += 1
            a += 1
        while b < total_num and time >= leave_time[b]:
            customer_moment -= 1
            b += 1
        total_Ls += customer_moment
    Ls = total_Ls / total_time

    return [Ws, Wq, Ls, Lq]
