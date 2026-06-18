"""
用环境变量的方式读取 .env 里的 GEMINI_API_KEY（复用今天学的写法）
创建 Client 对象
准备至少 3 条客户反馈文字（自己编几句真实点的，比如"东西用了两天就坏了，太差了""希望能增加夜间模式""客服态度特别好，解决问题很快"）
对每一条反馈，调用 generate_content，在 Prompt 里要求模型只回答"投诉"、"建议"或"表扬"三个词中的一个（这是在用之前阶段2.1学过的"输出格式控制"技巧，今天复习一下）
把每条反馈的原文和模型给出的分类结果一起打印出来
用 response.text 取出结果，不要打印整个 response 对象
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 加载 .env 文件里的环境变量
load_dotenv()

# 取出GEMINI_API_KEY, 定义client
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# 客户反馈
feedbacks = [
    "包装破损严重，里面的产品也有划痕，这是第二次遇到这种问题了。",
    "如果能增加多设备同步功能就太好了，现在每次切换电脑都要重新登录很麻烦。",
    "退货流程比想象中顺利很多，客服全程跟进，三天就拿到退款了，很满意。",
    "用了一周，电池续航明显不如宣传的那么久，有点失望。",
    "界面设计很简洁，新手也能很快上手，体验不错。",
    "能不能出一个深色模式？晚上用眼睛有点累。"
]

# 用google.genai中的types子模块定义提示词 Prompt
config = types.GenerateContentConfig(system_instruction="你是一个客户反馈分类助手。"
                                                        "只回答以下三个词中的一个：投诉、建议、表扬。不要输出任何其他文字。")

# 调用模型并输出结果
for feedback in feedbacks:
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=feedback,
        config=config
    )
    print(feedback)
    print(response.text)
    print()