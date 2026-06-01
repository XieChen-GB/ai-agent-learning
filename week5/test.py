class ChatAgent:
    # __init__ 是构造方法，创建对象时自动调用
    # self 代表"这个对象自己"，相当于 Java 的 this
    # name 和 model 是创建时传入的参数
    # model="qwen2.5:7b" 是默认参数：不传 model 时自动用这个值

    def __init__(self, name, model="qwen2.5:7b"):
        self.name = name
        self.model = model
        self.memory = []  # memory 不从外部传入，直接初始化为空列表
                          # 用来存储对话历史
    
    # 普通方法：添加一条消息到记忆
    # role 是角色（"user" 或 "assistant"），content 是消息内容
    def add_message(self, role, content): 
        # 把消息以字典形式追加到 memory 列表
        self.memory.append({"role": role, "content": content}) 
    
    # 普通方法：返回完整的对话历史
    def get_history(self):
        return self.memory

    # __repr__ 是特殊方法，定义对象的"官方字符串表示"
    # 当你 print(agent) 或在终端直接输入 agent 时，Python 调用它
    def __repr__(self):
        return f"ChatAgent(name={self.name}, message={len(self.memory)})"

    # 优先调用（如需启用，取消注释）
    # def __str__(self):
    #     return f"{self.name}, {len(self.memory)}"

class MeetingAgent(ChatAgent):
    def __init__(self, name):
        super().__init__(name)
        self.action_items = []
    
    def add_action_item(self, assignee, task, deadline):
        item = {
            "assignee": assignee,
            "task": task,
            "deadline": deadline
        }
        self.action_items.append(item)

    def get_action_items(self):
        return self.action_items
    
    def __repr__(self):
        return (f"MeetingAgent(name={self.name},"  
                f"message={len(self.memory)}"
                f"actions={len(self.action_items)})"
                )
    



def main():
    meeting_bot = MeetingAgent("会议助手")
    meeting_bot.add_message("user", "请记录今天的决议")
    meeting_bot.add_action_item("张三", "准备Q3报告", "2025-06-15")
    meeting_bot.add_action_item("李四", "联系客户跟进", "2025-06-10")

    print(meeting_bot)
    print(meeting_bot.get_action_items())
    print(meeting_bot.get_history())
    print(meeting_bot)



main()
    