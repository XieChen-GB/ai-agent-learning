from utils import validate_phone, format_contact

def display_menu():
    print("========== 联系人管理 ==========")
    print("1. 添加联系人")
    print("2. 查找联系人")
    print("3. 显示全部联系人")
    print("4. 删除联系人")
    print("5. 退出")

def main():
    """
    contacts = [
        {"name": "Charlie", "phone": "09012345678", "email": "charlie@example.com"},
        {"name": "Bob", "phone": "08098765432", "email": ""}
]
    """
    contacts = []

    while True:
        display_menu()
        choice = input("请选择1-5: ")
        if choice == "1":   # 添加联系人
            name = input("输入姓名：")
            phone = input("输入电话号码：")
            if not validate_phone(phone):
                print("电话号码格式不对，请重新输入")
                continue
            email = input("输入邮箱：")
            contacts.append({"name": name,"phone": phone, "email": email})
            print("添加成功")

        elif choice == "2": # 查找联系人
            find_name = input("输入查找人姓名：").lower()
            results = [c for c in contacts if find_name in c["name"].lower()]
            if len(results) ==0:
                print("未找到相关联系人")
            else:
                for i, member in enumerate(results):
                    print(f"{i+1} {format_contact(member)}")


        elif choice == "3":   # 显示全部联系人
            if len(contacts) == 0:
                print("暂无联系人")
            else:
                for i in range(len(contacts)):
                    print(f"{i+1}. {format_contact(contacts[i])}")
        elif choice == "4":     # 删除联系人
            if len(contacts) == 0:
                print("暂无联系人")
                continue
            for i, numer in enumerate(contacts):
                print(f"{i+1} {format_contact(numer)}")
            del_member_name = input("输入要删除联系人编号：")
            index = int(del_member_name)
            if 0 < index <= len(contacts):
                confirm = input(f"确认删除{contacts[index - 1]['name']} 吗？（y/n)")
            else:
                print("输入号码不存在")
                continue
            if confirm == "y":
                del contacts[index - 1]
                print("已删除")
            else:
                print("未删除")
        elif choice == "5":
            break
        else:
            print("无效选项，请重新输入")
                


                        



main()