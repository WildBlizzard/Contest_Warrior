# --- 虽有多闻 若不修行 与不闻等 如人说食 终不能饱


import random


def random_s():
    """
    获得随机英文加数字组合的字符串
    return: 随机字符串
    """
    str_s = ['' + chr(random.randrange(97, 123)) for i in range(4)]
    str_n = ['' + str(random.randrange(0, 10)) for i in range(3)]
    return ''.join(str_s + str_n)
