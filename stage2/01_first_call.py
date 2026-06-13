import ollama

messages = [
    {
        "role": "system",
        "content": "你是一个会议助手，回答要简洁。"
    },
    {
        "role": "user",
        "content": "帮我总结一下这句话：销售额增长了23%"
    }    
]

response = ollama.chat(
    model ="qwen2.5:7b",
    messages = messages
)

print(response["message"]["content"])