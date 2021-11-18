# --- 虽有多闻 若不修行 与不闻等 如人说食 终不能饱


import re


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
