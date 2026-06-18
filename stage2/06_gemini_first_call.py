import os
from dotenv import load_dotenv
from google import genai

# 加载 .env 文件里的环境变量
load_dotenv()

# 取出 Key
api_key = os.getenv("GEMINI_API_KEY")

# 创建一个 Client 对象，传入 Key，这个对象代表"一次和 Gemini 服务器的连接"
client = genai.Client(api_key = api_key)

# 通过 client 对象的 models 属性，调用 generate_content 方法
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="帮我总结这段会议记录：本季度销售额同比增长23%，主要驱动来自亚太区新客户拓展。"
               "市场部提出下季度预算需要增加15%用于线上推广。产品团队反馈新功能上线后用户反馈积极，"
               "但服务器负载在高峰期出现延迟，技术团队计划下周完成扩容。"
)

print(response)

print(response.text)