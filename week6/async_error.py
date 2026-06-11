import asyncio
import time

# 等待 2 秒，正常返回 "搜索结果：{query}"
async def search_web(query):
    await asyncio.sleep(2)
    return f"搜索结果：{query}"

# 等待 1 秒，模拟文件不存在，抛出 FileNotFoundError
async def read_file(filename):
        await asyncio.sleep(1)
        raise FileNotFoundError(f"{filename}不存在")

# 等待 3 秒，正常返回 "查询结果：{sql}"
async def query_database(sql):
    await asyncio.sleep(3)
    return f"查询结果：{sql}"

async def main():
    starttime = time.time()
    result = await asyncio.gather(
        search_web("查询天气"),
        read_file("查询文件"),
        query_database("查询数据库"),
        return_exceptions= True     # 出错时不崩溃，把异常作为结果返回
    )
    for r in result:
         if isinstance(r,Exception):
              print(f"失败：{r}")
         else:
              print(f"成功：{r}")
    endtime = time.time()
    print(f"总耗时：{endtime - starttime:.1f}秒")


asyncio.run(main())

