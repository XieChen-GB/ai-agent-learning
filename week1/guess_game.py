# 猜数字游戏 
import random
number = random.randint(1,100)
while True:
    try:
        guess = int(input("请输入数字："))
    except ValueError:
        print("请输入数字，不能输入文字")
        continue
    if number == guess:
        print("猜对了")
        break
    elif number > guess:
        print("猜小了")
    else:
        print("猜大了")

