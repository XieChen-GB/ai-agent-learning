import ollama
import json


# ── 第一步：定义工具 
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_action_items",
            "description": "获取某人负责的代办事项",  # 关键！模型根据这段描述判断该不该调这个工具
            "parameters":{
                "type": "object",
                "properties": {
                    "assignee": {
                        "type": "string",
                        "description": "负责人姓名，例如： 张三"  # 关键！
                    }
                },
                "required": ["assignee"] # 哪些参数是必填的
            }
        }
    }
]

# ── 第二步：定义真正的工具函数
def get_action_items(assignee: str) -> str:
    # 这里用假数据模拟
    fake_db = {
    "张三": ["整理Q3报告", "联系供应商"],
    "李四": ["更新项目文档"],
    "王五": [],
    }    

    result = fake_db.get(assignee, f"无{assignee}的数据")
    return json.dumps(result, ensure_ascii=False) if isinstance(result, list) else result

# ── 第三步：第一次调用——把问题和工具列表发给模型
messages= [
    {"role": "user",
     "content": "张三负责什么？"
    }
]

response = ollama.chat(
    model = "qwen2.5:7b",
    messages = messages,
    tools = tools
)

# ── 第四步：判断模型是否想调用工具 
assistant_message = response["message"]
if assistant_message["tool_calls"]:
    tool_call = assistant_message["tool_calls"][0]
    tool_name = tool_call["function"]["name"]
    tool_args = tool_call["function"]["arguments"]

    # ── 第五步： 调用工具   
    tool_result = get_action_items(tool_args["assignee"])

    # ── 第六步：把工具结果追加进 messages
    messages.append(assistant_message)
    messages.append(
        {
            "role": "tool",
            "content": tool_result
        }
    )

    # ── 第七步：第二次调用——让模型根据  
    final_response = ollama.chat(
        model = "qwen2.5:7b",
        messages = messages
    )      

    print(final_response["message"]["content"])
else:
    print(assistant_message["content"])


