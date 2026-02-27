import string

BASE62 = string.ascii_letters+string.digits


def encode_base62(num:int)->str:
    if num == 0:
        return BASE62[0]
    res = ""
    while num:
        num,rem = divmod(num,62)
        res = BASE62[rem] + res
    return res