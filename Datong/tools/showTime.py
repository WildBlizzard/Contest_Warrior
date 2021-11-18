# --- 虽有多闻 若不修行 与不闻等 如人说食 终不能饱


import time


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


def electronic_clock(input_seconds):
    """
    电子钟式显示器
    return: 时，分，秒
    """
    pre_minute, second = divmod(input_seconds, 60)
    hour, minute = divmod(pre_minute, 60)
    return hour, minute, second
