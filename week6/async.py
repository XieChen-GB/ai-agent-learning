# 异步
import asyncio
import time

# async def：声明这是一个异步函数
async def call_api(name, seconds):
   print(f"开始调用{name}")
   await asyncio.sleep(seconds) # 异步等待：等待期间 CPU 可以去做别的事
   print(f"{name} 完成")
   return f"{name} 的结果"

async def main():
   start = time.time()

   # asyncio.gather()：同时启动多个异步任务，等全部完成后统一返回
   start = time.time()

   results = await asyncio.gather(
      call_api("天气查询", 2),
      call_api("新闻搜索", 3),
      call_api("日历读取", 1)
   )

   end = time.time()
   print(f"总耗时: {end - start:.1f}秒")
   print(results)
   print(type(results))

asyncio.run(main())
