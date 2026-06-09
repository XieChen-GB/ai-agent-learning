async def call_api(name, seconds):
    pass

# 不加 await，直接调用
result = call_api("天气查询", 2)
print(type(result))   # <class 'coroutine'>
print(result)         # <coroutine object call_api at 0x...>