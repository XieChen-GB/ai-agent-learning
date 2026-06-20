# 阶段3 模块1：RAG 基础流程
import chromadb    # 向量数据库    
import ollama

# ---------- 配置 ----------
EMBED_MODEL = "shaw/dmeta-embedding-zh"    # 中文专用 embedding 模型
CHAT_MODEL = "qwen2.5:7b"                 # 对话生成模型

# 1. 创建一个向量库客户端（这里用内存模式，程序结束数据不保留，先跑通流程用）
client = chromadb.EphemeralClient()

# 2. 创建一个集合（collection），可以理解成"一张专门存会议纪要向量的表"
collection = client.create_collection("meeting_notes")

# 3. 准备几篇会议纪要原文（实际场景会从文件读入，这里先手写几条演示）
documents = [
    # 销售/业绩
    "Q3 销售额同比增长 23%，主要来自亚太区",
    "北美市场连续两个月未达销售目标，需要调整策略",
    "年度营收预计突破 5000 万，较去年增长 15%",
    # 技术
    "技术团队完成了登录模块的重构，下周开始测试",
    "后端 API 响应时间从 800ms 优化到 200ms",
    "数据库迁移计划定在下月第一周执行",
    # 人事
    "新入职 3 名前端工程师，下周一正式报到",
    "年度绩效考核将在 12 月进行，各部门提前准备材料",
    "李经理申请调岗至产品部，已获上级批准",
    # 市场
    "市场部计划在 11 月举办新品发布会",
    "竞品公司上周发布了类似产品，定价比我们低 20%",
    "品牌合作方案已提交给三家候选供应商",
    # 财务
    "本季度研发预算使用率为 78%，剩余资金可支撑到年底",
    "差旅费报销流程从下月起改为线上审批",
    # 运营
    "客服团队上月平均响应时间缩短至 30 秒",
]

# 4. 把每篇文档转成向量，存进collection
doc_id = 0
for doc in documents:
    embed = ollama.embed(model=EMBED_MODEL, input=doc).embeddings[0]
    collection.add(ids=[f"doc{doc_id}"], embeddings=[embed], documents=[doc])
    doc_id += 1
print(f"已存入 {doc_id} 条文档")

# 5. 用户提问
question = "公司业绩怎么样"

# 6. 问题转成向量（同一个embedding模型，否则两边数字空间不一致，无法比较距离）
question_embed = ollama.embed(model=EMBED_MODEL, input=question).embeddings[0]

# 7. 在collection里搜索最相似的2条记录
result = collection.query(query_embeddings=[question_embed],n_results=2)

# 8. 取出匹配到的原文
matched_docs = result["documents"][0]
print("检索到的文档:", matched_docs)

# 9. 把原文+问题一起发给对话模型，让它基于这份资料回答
response = ollama.chat(model=CHAT_MODEL, messages=[
    {"role": "system", "content": "请只根据下面提供的资料回答问题，不要编造资料之外的内容。"},
    {"role": "user", "content": f"资料： {matched_docs}\n\n问题：{question}"}
])

print(response.message.content)