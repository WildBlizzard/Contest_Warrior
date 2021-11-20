# --- 虽有多闻 若不修行 与不闻等 如人说食 终不能饱


import os
import re
import sys
import time
import random
from math import floor
sys.dont_write_bytecode = True


class RightHand:

    @staticmethod
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

    @staticmethod
    def vegetable_cutter(pre_list, pre_size):
        """
        拆分列表
        pre_list: 传入列表
        pre_size: 期待拆分值
        return: 拆分后的列表
        """
        if pre_size < 1: pre_size = 1
        return [pre_list[i:i+pre_size] for i in range(0, len(pre_list), pre_size)]

    @staticmethod
    def customize_cut_list(da_list, cut_num=3):
        """
        想要的拆分列表
        da_list: 传入列表
        cut_num: 想切成几份，必须大于2
        return: 切好的列表
        """
        if cut_num < 3: cut_num = 3
        in_data = RightHand.data_arrangement(da_list, cut_num)
        if floor(len(in_data[1])/cut_num) == 1 : pass
        else:
            new_r = RightHand.vegetable_cutter(in_data[1], floor(len(in_data[1])/(cut_num - 2)))
            lmr = [in_data[0]]
            for item in new_r: lmr.append(item)
            if len(new_r) != cut_num - 2: in_data[2].extend(lmr.pop())
            lmr.append(in_data[2])
            return lmr
        return in_data

    @staticmethod
    def make_dirs(input_path):
        """
        判断路径是否完整，否则创建对应文件夹，完整路径
        input_path: 输入路径
        return: None
        """
        if not os.path.exists(input_path): os.makedirs(input_path)

    @staticmethod
    def complete_it(open_file_path, save_file_path, index_num, addition=''):
        """
        创建输出路径
        open_file_path: 完整输入路径子路径及文件
        save_file_path: 初始输出路径
        index_num: 初始输入路径长度定位值
        addition: 额外增补路径，默认空
        return: 完整输出路径，子文件夹路径
        """
        # 获取下级目录路径信息，若无则只返回系统分隔符
        end_path = (os.path.split(open_file_path)[0][index_num:]) + os.sep
        # 组合完整输出路径
        final_output = save_file_path + end_path + addition + os.sep
        # 创建输出路径
        RightHand.make_dirs(final_output)
        return final_output, end_path

    @staticmethod
    def through_full_path(origin_path):
        """
        遍历路径，让步产出完整体
        origin_path: 输入路径
        yield: 完整路径
        """
        for root, dirs, files in os.walk(origin_path):
            for name in files: yield os.path.join(root, name)

    @staticmethod
    def get_order_list(input_list, symbol='/', sign_splt='-'):
        """
        获取一个有序的路径列表，文件名需类似此形态：'xxx-1.xxx'，
        input_list: 输入路径（无序）
        symbol: 当前运行系统文件夹分隔符 (已无效，无需输入)
        sign_splt: 以何标识拆分文件名，以区分，默认为 '-'，可变更
        return: 有序路径
        """
        compare_one = [item for item in sorted(RightHand.through_full_path(input_list))]
        compare_two = [int(os.path.split(item)[-1].split('.')[0].split(sign_splt)[-1])
                        for item in sorted(RightHand.through_full_path(input_list))]
        ziplist = zip(compare_one, compare_two)
        return [item[0] for item in sorted([(k, v) for k, v in ziplist], key=lambda x:x[1])]

    @staticmethod
    def get_the_filename(input_path, index_num, extension):
        """
        创建自定义路径末尾文件名及格式
        input_path: 输入路径
        index_num: 路径长度定位值
        extension: 文件扩展名
        return: 想要的文件名
        """
        return '{}.{}'.format(((input_path[index_num:].split(os.sep)[-1]).split('.')[0]), extension)

    @staticmethod
    def random_s():
        """
        获得随机英文加数字组合的字符串
        return: 随机字符串
        """
        str_s = ['' + chr(random.randrange(97, 123)) for i in range(4)]
        str_n = ['' + str(random.randrange(0, 10)) for i in range(3)]
        return ''.join(str_s + str_n)

    @staticmethod
    def out(rule, inp_str):
        """
        正则输出
        rule 正则表达式
        return 筛后字符串
        """
        if not rule: return ''
        regex = re.compile(rule, re.S)
        result_re = regex.findall(inp_str)
        if not result_re: return ''
        elif type(result_re[0]) is str:
            return ''.join(result_re)
        return ','.join(result_re[0])

    @staticmethod
    def calculate_time(func):
        """
        计时装饰器
        """
        def wrapper(*args, **kwargs):
            start_spot = time.perf_counter()
            func(*args, **kwargs)
            final_time = time.perf_counter() - start_spot
            # print('Process "%s" takes %.2f seconds' % (func.__name__, final_time / 60))
            print('It took %.2f seconds' % final_time)

        return wrapper

    @staticmethod
    def electronic_clock(input_seconds):
        """
        电子钟式显示器
        return: 时，分，秒
        """
        pre_minute, second = divmod(input_seconds, 60)
        hour, minute = divmod(pre_minute, 60)
        return hour, minute, second
