# 练习：交互式会议纪要检索系统
import ollama
import chromadb
import json
import os

# ---------- 配置 ----------
EMBED_MODEL = "shaw/dmeta-embedding-zh"    # 中文专用 embedding 模型
CHAT_MODEL = "qwen2.5:7b"                 # 对话生成模型

# 读取JSON文件
script_dir = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(script_dir, "meeting_data.json")

def load_data(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("文件格式错误")
        return []
    
meetings = load_data(filepath)

# 创建一个向量库客户端（这里用内存模式，程序结束数据不保留，先跑通流程用）
client = chromadb.EphemeralClient()

# 创建一个集合collection（议纪要向量数据库）
collection = client.get_or_create_collection("meeting_notes")

# 把每篇文档转成向量，存进collection
doc_id = 0
for meeting in meetings:
    embed = ollama.embed(model=EMBED_MODEL, input=meeting).embeddings[0]
    collection.add(ids=[f"doc{doc_id}"], embeddings=[embed],documents=[meeting])
    doc_id += 1
print (f"已存入{doc_id}条文档")


while True:
    user_input = input("输入要问的问题/quit退出: ")
    # 如果输入空格则跳过下面代码，返回到while
    if not user_input.strip():
        continue

    if user_input.strip().lower() == "quit":
        break

    # 用户输入转成向量
    user_input_embed =  ollama.embed(model=EMBED_MODEL,input=user_input).embeddings[0]
    
    # collection里搜索最相似的2条记录
    query_embed = collection.query(query_embeddings=[user_input_embed], n_results=2)
    
    # 取出匹配到的原文
    matched_meeting_note = query_embed["documents"][0]
    print("检索到的文档:", matched_meeting_note)
    
    # 把原文+问题一起发给对话模型，让它基于这份资料回答
    response = ollama.chat(model=CHAT_MODEL, messages=[
        {"role": "system", "content": "请只根据下面提供的资料回答问题，不要编造资料之外的内容。"},
        {"role": "user", "content": f"问题：{user_input}\n资料：{matched_meeting_note}"}  
    ])
    
    # 打印LLM的回答
    print(response.message.content)
                             
                             
                             
                             
                    





    