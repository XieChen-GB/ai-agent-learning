"""
Stage 4 第一个文件：验证 Claude API 连通性
用 Haiku 模型发一条最简单的消息，确认 API Key 和网络都没问题
"""

import os
from dotenv import load_dotenv  # 用来读取同目录下的 .env 文件，把里面的 ANTHROPIC_API_KEY 加载成环境变量
import anthropic    # 是官方 SDK，等下用它建 client、调 Haiku 模型

load_dotenv()

# 创建 Anthropic 客户端, 自动从环境变量 ANTHROPIC_API_KEY Key
client = anthropic.Anthropic()

# 调用 Claude Haiku 4.5
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=2000,
    messages=[
        {"role": "user", "content": "用一句话介绍一下你自己"}
    ]
)

print("模型回复：", response.content[0].text)

print(f"输入 token： {response.usage.input_tokens}")
print(f"输出 token： {response.usage.output_tokens}")