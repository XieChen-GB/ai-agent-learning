# 第一步 写出工具列表和初始状态字典

# 模拟要依次执行的工具列表
tools = ["transcribe", "summarize", "send_email"]

# 初始状态字典：任务进度看板
agent_state = {
    "completed_tools": [],   # 已成功完成的工具 初始值为空
    "current_step": None,    # 当前要执行的工具
    "retry_count": 0,        # 失败重试次数
    "last_error": None       # 最近一次错误信息
}

print(agent_state)

# 第二步 模拟工具执行用的被调用函数
def  run_tool(tool_name: str) -> str:
    if tool_name == "send_email":
        raise Exception("网络超时")
    else:
        return f"{tool_name}执行成功"
    
# 第三部 执行逻辑
for tool in tools:
    agent_state["current_step"]= tool       # 标记当前正在执行哪个工具
    agent_state["retry_count"] = 0          # 每个新工具开始前，重试次数清零

    # 最多尝试 3 次（1 次正常 + 2 次重试）
    while agent_state["retry_count"] < 3:
        try:
            response = run_tool(tool)
            agent_state["completed_tools"].append(tool)
            break
        except Exception as e:
            agent_state["last_error"] = str(e)
            agent_state["retry_count"] += 1
            if agent_state["retry_count"] == 3:
                print(f"{tool}最终失败， 跳过")
            else:
                print(f"{tool} 第 {agent_state['retry_count']} 次重试")

print(agent_state)


