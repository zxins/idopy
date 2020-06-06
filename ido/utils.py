import time


def uniqid(prefix=''):
    """ 生成唯一ID """
    return prefix + hex(int(time.time()))[2:10] + hex(int(time.time() * 1000000) % 0x100000)[2:7]


def timestamp():
    """ 10位数字时间戳 """
    return int(time.time())


def strftime(stamp):
    local_time = time.localtime(stamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", local_time)
