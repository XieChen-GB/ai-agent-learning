import ollama

messages = [
    {
        "role": "system",
        "content": "你是一个会议助手，回答要简洁。"
    },
]

while True:
    user_message = input("请输入/输入quit退出:")
    if user_message == "quit":
        break
    else:
        messages.append({"role": "user", "content": user_message})
        response = ollama.chat(
            model="qwen2.5:7b",
            messages=messages
        )
        print(response["message"]["content"]) 
        messages.append({"role": "assistant", "content": response["message"]["content"]})
        

 