# 目标：用 LangSmith 追踪带工具调用的 Agent，并记录评估指标

import json                                     # 读取 meeting_data.json
import time                                     # 计算耗时
from pathlib import Path                        # 现代的路径处理工具，比字符串拼路径更安全
from dotenv import load_dotenv                  # 从 .env 文件加载环境变量

from langchain_ollama import ChatOllama
from langchain_core.tools import tool           # 把函数变成 LangChain 工具的装饰器 @tool
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage       # 表示消息类

from langsmith.run_helpers import traceable     # 让函数的调用被 LangSmith 追踪的装饰器


# ── 第一步：加载环境变量 ──────────────────────────────────────────
# 把 .env 里的 LANGSMITH_TRACING、LANGSMITH_API_KEY、LANGSMITH_PROJECT 加载到环境变量中
# LangSmith 会自动检测这些变量，发现 TRACING=true 就开始记录
load_dotenv()

# 定义fuzzy_match 只要 keyword 里有任意 2 个字连续出现在记录里，就算命中
def fuzzy_match(keyword: str, text: str) -> bool:
    # 如果关键词本身很短（2字以内），直接用原来的子串匹配
    if len(keyword) <= 2:
        return keyword in text
    # 关键词较长时，检查里面任意连续2字是否出现在text里
    for i in range(len(keyword) -  1):
        if keyword[i:i+2] in text:
            return True
    return False
    


# ── 第二步：定义工具 ──────────────────────────────────────────────
# @tool 是装饰器，作用是告诉 LangChain：这个函数是一个可供 Agent 调用的工具
# LangChain 会读取函数名、参数、docstring，生成工具描述传给模型
@tool
def search_meeting_data(keyword: str) -> str:
    """
    在会议记录中搜索包含关键词的条目。
    keyword: 要搜索的关键词，例如"销售额"、"融资"
    """

    data_path = Path(__file__).parent/"meeting_data.json"
    # Path(__file__).parent 取出当前脚本所在的目录
    # / "meeting_data.json" 拼接文件名，得到完整路径
    
    try:
        with open(data_path, "r", encoding="utf-8") as f:   # 读取 JSON 文件
        
            record = json.load(f)   # records 是一个列表，每个元素是一条会议记录字符串
            
            # 遍历所有记录，找出包含 keyword 的条目
            results = [r for r in record if fuzzy_match(keyword,r)]
            
            if not results:     # results 为空
               return f"没有找到包含'{keyword}'的会议记录"
            
            # 作用是用指定的连接符(这里是\n)把列表里的元素拼成一个字符串
            return "\n".join(results) 
                   
    except Exception as e:
        return f"读取文件失败：{e}"

# ── 第三步：初始化模型，绑定工具 ──────────────────────────────────
# ChatOllama：用本地 Ollama 运行的聊天模型
# model 参数指定模型名，temperature=0 让输出更稳定（减少随机性）
llm = ChatOllama(model="qwen2.5:7b", temperature=0)

# bind_tools：把工具列表注册给模型
# 注册后，模型在推理时会知道"我可以调用 search_meeting_data 这个工具"
llm_with_tools = llm.bind_tools([search_meeting_data])



# ── 第四步：定义带追踪的 Agent 运行函数 ──────────────────────────
# @traceable 装饰器：让这个函数的每次调用都被 LangSmith 记录成一个 Trace
# name 参数是这个 Trace 在 LangSmith 网页上显示的名称
# @traceable用于LangSmith平台   把函数的调用过程记录到追踪系统
@traceable(name="meeting-agent-evaluation")
def run_agent(question:str, expected_keyword:str) -> dict:
    """
    运行一次 Agent, 并返回评估结果。
    question: 用户的问题
    expected_keyword: 期望出现在最终回答里的关键词，用于判断回答是否相关
    """
    start_time = time.time()    # 记录开始时间

    # 第一次调用：把用户问题发给模型
    # HumanMessage 是 LangChain 表示用户消息的标准类
    messages: list[BaseMessage] = []
    messages.append(HumanMessage(content=question))
    response = llm_with_tools.invoke(messages)     # 用户问题发给模型，模型的回答返回给response
    messages.append(response)   # 加入模型的回复（含工具调用请求）

    # 检查模型是否决定调用工具
    # response.tool_calls 是一个列表，模型决定调用工具时这里会有内容
    # 模型会根据messages的内容回答，当判断要调用tool时，
    # 它会用tool_calls返回要调用tool的信息，这里是search_meeting_data
    tool_called = len(getattr(response, "tool_calls", [])) > 0
    tool_results = []
    search_found_results = True

    if tool_called: #tool_calls不为空 = 模型有调用tool的请求时
        # 遍历模型请求的每一个工具调用
        for tc in response.tool_calls:
            tool_name = tc["name"]    #工具名称，本练习就是 "search_meeting_data"
            tool_args = tc["args"]    # 工具参数，例如 {"keyword": "销售额"}

            print(f" → 模型调用工具： {tool_name}, 参数：{tool_args}")

            # 实际执行工具，search_meeting_data.invoke 是 LangChain 工具的标准调用方式
            # result里是tool返回的结果
            result = search_meeting_data.invoke(tool_args)
            tool_results.append(result)
            print(f"  → 工具返回：{result[:50]}...") # 只打印前 50 个字符

            # 检查result里是否包含 没有找到  的词
            if result.startswith("没有找到"):
                search_found_results = False

        # 把工具结果加入消息历史
        for i,tc in enumerate(response.tool_calls):
            messages.append(ToolMessage(content=tool_results[i], 
                                        tool_call_id = tc["id"]))

        # 第二次调用模型，这次模型拿到了工具结果，生成最终回答
        final_response = llm_with_tools.invoke(messages)
        final_answer = final_response.content
    else:
        # 模型没有调用工具，直接用第一次的回答作为最终答案
        final_answer = response.content
    

    # 总耗时，保留两位小数
    elapsed = round(time.time() - start_time, 2)

    # 判断回答是否包含期望关键词
    answer_relevant = expected_keyword in final_answer # answer_relevant的值是True or False

    # 整理评估结果
    evaluation = {
        "question": question,
        "tool_called": tool_called,  # 工具是否被调用 True or False
        "search_found_results": search_found_results,
        "answer_relevant": answer_relevant,
        "elapsed_second": elapsed,
        "final_answer": final_answer,
    }
    return evaluation


# ── 第五步：运行测试 ──────────────────────────────────────────────
if __name__ == "__main__":
    # 三个测试问题，每个附带一个期望出现在回答里的关键词
    test_case =[
        {"question": "公司的销售额增长情况如何？", "expected_keyword": "销售额"},
        {"question": "技术团队最近有什么问题？",    "expected_keyword": "宕机"},
        {"question": "融资计划是什么？",           "expected_keyword": "融资"},
    ]

    print("=" * 50)
    print("测试".center(50,"="))
    for this_case in test_case:
        print(f"\n问题：{this_case['question']}")
        result = run_agent(this_case["question"], this_case["expected_keyword"])

        print(f"  工具调用：{result['tool_called']}")
        print(f"  搜索命中：{result['search_found_results']}") 
        print(f"  回答相关：{result['answer_relevant']}")
        print(f"  耗时：{result['elapsed_second']}秒")
        print(f"  回答：{result['final_answer'][:80]}...")

    
          
        