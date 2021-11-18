# --- 虽有多闻 若不修行 与不闻等 如人说食 终不能饱


from math import floor


def data_arrangement(ori_list, ori_num):
    """
    数据整理
    ori_list: 传入列表
    ori_num: 拆分块基础数量
    return: 传入列表三大件
    """
    one_index = int(len(ori_list) // ori_num)
    three_index = -int(len(ori_list) // ori_num)
    left = ori_list[None:int(one_index)]
    mid = ori_list[int(one_index):int(three_index)]
    right = ori_list[int(three_index):None]
    return left, mid, right


def vegetable_cutter(pre_list, pre_size):
    """
    拆分列表
    pre_list: 传入列表
    pre_size: 期待拆分值
    return: 拆分后的列表
    """
    if pre_size < 1: pre_size = 1
    return [pre_list[i:i+pre_size] for i in range(0, len(pre_list), pre_size)]


def customize_cut_list(da_list, cut_num=3):
    """
    想要的拆分列表
    da_list: 传入列表
    cut_num: 想切成几份，必须大于2
    return: 切好的列表
    """
    if cut_num < 3: cut_num = 3
    in_data = data_arrangement(da_list, cut_num)
    if floor(len(in_data[1])/cut_num) == 1 : pass
    else:
        new_r = vegetable_cutter(in_data[1], floor(len(in_data[1])/(cut_num - 2)))
        lmr = [in_data[0]]
        for item in new_r: lmr.append(item)
        if len(new_r) != cut_num - 2: in_data[2].extend(lmr.pop())
        lmr.append(in_data[2])
        return lmr
    return in_data
