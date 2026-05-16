user_input = "这是我第一次写Python代码"
if len(user_input) > 500:
    print("输入过长，请缩短后重试")
elif len(user_input) == 0:
    print("输入为空")
else: 
   print(f"✅输入合法，共{len(user_input)}字，正在处理...")

for i in range(5):
   print(user_input[i])
