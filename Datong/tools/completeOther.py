# --- 虽有多闻 若不修行 与不闻等 如人说食 终不能饱


import os


def make_dirs(input_path):
    """
    判断路径是否完整，否则创建对应文件夹，完整路径
    input_path: 输入路径
    return: None
    """
    if not os.path.exists(input_path): os.makedirs(input_path)


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
    make_dirs(final_output)
    return final_output, end_path