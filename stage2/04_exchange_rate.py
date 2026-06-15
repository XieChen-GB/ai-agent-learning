import requests
import json
import ollama

# ── 第一步：定义工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_exchange_rate",
            "description": "获取某种货币对日元的汇率，查询某货币兑换日元的汇率，传入源货币代码，例如：USD表示查询美元兑日元",
            "parameters":{
                "type": "object",
                "properties": {
                    "currency": {
                        "type": "string",
                        "description": "货币代码，例如：USD、EUR、CNY"
                    }
                },
                "required": ["currency"]
            }
        }                    
    }
]

# ── 第二步：tool function
def get_exchange_rate(currency: str) -> str:
    url = f"https://api.frankfurter.app/latest?from={currency}&to=JPY"  # f-string 把货币代码拼进URL"
    response = requests.get(url)
    data = response.json()
    rate = data["rates"]["JPY"]
    return f"1{currency} = {rate} JPY"

# ── 第三步：第一次调用——把问题和工具列表发给模型
messages = [
    {"role": "user", "content": "1美元兑换日元的汇率是多少？请查询USD对JPY的汇率"}
]

response = ollama.chat(
    model= "qwen2.5:7b",
    messages= messages,
    tools= tools
)

# ── 第四步：判断模型是否想调用工具
assistant_message = response["message"]
if assistant_message.get("tool_calls"):
    tool_call = assistant_message["tool_calls"][0]
    tool_name = tool_call["function"]["name"]
    tool_args = tool_call["function"]["arguments"]

    # ── 第五步： 调用工具
    tool_result = get_exchange_rate(tool_args["currency"])

    # ── 第六步：把工具结果追加进 messages，再发给模型
    messages.append(assistant_message)
    messages.append(
        {
            "role": "tool",
            "content": tool_result
        }
    )

    # ── 第七步：第二次调用——让模型根据结果生成最终回答 ──────
    final_response = ollama.chat(
        model= "qwen2.5:7b",
        messages= messages
    )

    print(final_response["message"]["content"])
else:
    # 模型判断不需要工具，直接回答
    print(assistant_message["content"])
