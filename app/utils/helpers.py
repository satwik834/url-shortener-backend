def encode_base62(num: int) -> str:
    if num == 0:
        return "0"
    
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base62 = []
    
    while num > 0:
        num, rem = divmod(num, 62)
        base62.append(chars[rem])
        
    return "".join(reversed(base62))
