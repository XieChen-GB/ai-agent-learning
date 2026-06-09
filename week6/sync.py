import time

# 模拟一个需要等待的操作（比如调用 AI API）
def call_api(name, seconds):
    print(f"开始调用 {name}")
    time.sleep(seconds)        # 模拟等待，CPU 在此期间什么都不做
    print(f"{name} 完成")
    return f"{name} 的结果"

def main():
    start = time.time()

    result1 = call_api("天气查询", 2)
    result2 = call_api("新闻搜索", 3)
    result3 = call_api("日历读取", 1)

    end = time.time()
    print(f"总耗时：{end - start:.1f} 秒")
    print([result1, result2, result3])

main()