import ollama
import json

response = ollama.chat(
    model= "qwen2.5:7b",
    messages=[
        {
            "role": "system",
            "content": """
                你是一个信息提取助手。你的输出必须是且只是一个合法的 JSON 对象，不要有任何其他文字、解释或 markdown 代码块标记。
                输出格式如下：
                {
                    "summary": "会议内容一句话总结",
                    "decisions": ["决定事项1"],
                    "action_items": [
                        {"task": "任务", "owner": "负责人", "deadline": "截止时间"}
                    ]
                }    
            """
        },
        {
            "role": "user",
            "content": "本次季度复盘会议由总经理主持。销售总监李红汇报Q3业绩同比增长18%，超出预期目标。会议决定将Q4销售目标上调至2000万，由李红负责制定详细计划，需在10月15日前提交。技术部张工提出系统稳定性问题，决定在本月底前完成服务器扩容，运维团队负责执行。市场部的推广预算是否增加还在讨论中，下次会议再定。"

        }
    ]
)

raw_output = response["message"]["content"]
print("模型原始JSON输出")
print(raw_output)

try:
    result = json.loads(raw_output)    # 把 JSON 字符串转成 Python 字典
    print("会议总结:", result["summary"])
    print("决定事项：", result["decisions"])
    print("代办事项：", result["action_items"])
except json.JSONDecodeError as e:
    print(e)

