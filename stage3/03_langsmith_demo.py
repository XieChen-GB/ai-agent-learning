# 读取 .env 文件里的环境变量
from dotenv import load_dotenv

# LangChain 对 Ollama 的封装，提供标准化的 .invoke() 接口
from langchain_ollama import ChatOllama

# 把 .env 里的 LANGSMITH_TRACING、LANGSMITH_API_KEY、LANGSMITH_PROJECT 加载到环境变量中
# LangSmith 会自动检测这些变量，发现 TRACING=true 就开始记录
load_dotenv()

# 创建模型实例, ChatOllama 走 LangChain 的标准接口，LangSmith 能自动捕捉它的调用
llm = ChatOllama(model="qwen2.5:7b")

# .invoke() 是 LangChain 所有组件统一的调用方法
# 传入字符串，内部自动包装成 messages 格式发给 Ollama，拿到结果后包装成 LangChain 的响应对象返回
response = llm.invoke("用一句话解释什么是RAG")

# response 是 AIMessage 对象，.content 属性取纯文本内容
print(response.content)