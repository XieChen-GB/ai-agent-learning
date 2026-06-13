def log_call(fun):
    print("A：log_call 开始执行")
    def wrapper():                    # 这一行被执行了——但执行的含义是"创建函数对象"
        print("C：wrapper 的函数体执行了")
        fun()
    print("B：wrapper 已经定义完，但 C 没有被打印")
    return wrapper

@log_call                             # 程序启动时触发 log_call(say_hello)
def say_hello():
    print("你好")

print("====分隔线====")
say_hello()