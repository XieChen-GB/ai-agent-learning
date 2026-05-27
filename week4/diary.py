import json
import datetime

def load_diary(file = "diary.json"):
    try:
        with open(file, "r", encoding="utf-8") as f:
            diary_json = json.load(f)
            return diary_json
    except FileNotFoundError:
        print("还没有日记，快来写第一篇吧！")
        return []
    except json.JSONDecodeError as e:
        print(f"文件损坏请手动检查{file}：{e}")
        exit()  # 直接退出程序，防止数据被覆盖

def save_diary(notes, file = "diary.json"):
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(notes, f, ensure_ascii=False, indent=2)
    except PermissionError as e:
        print(f"无法写入：{e}")

def write_note(notes):
    title = input("请输入日记标题：")
    content = input("写日记吧：")
    id_int = len(notes) + 1
    date_str = str(datetime.date.today())
    notes.append({"id": id_int, "date": date_str, "title": title, "content": content})

def show_all(notes):
    """
    notes = [
            {"id": 1, "date": "2025-01-15", "title": "...", "content": "..."},
            {"id": 2, "date": "2025-01-16", "title": "...", "content": "..."}
    ]
    """
    for diary in notes:
        print(f"ID: {diary['id']}, 日期: {diary['date']}, 标题: {diary['title']}")

def show_one(notes):
    try:
        num = int(input("请输入日记编号："))
    except ValueError:
        print("请输入有效的数字编号")
        return
    if not (1 <= num <= len(notes)):
        print(f"编号超出范围，当前共有{len(notes)}篇日记")
        return
    print(notes[num-1])

def main():
    notes = load_diary()

    while True:
        print("\n=== 我的日记本 ===")
        print("1. 写新日记")
        print("2. 查看所有日记")
        print("3. 查看某篇日记")
        print("4. 退出")

        choice = input("请选择：")

        if choice == "1":
            write_note(notes)
            save_diary(notes)
        elif choice == "2":
            show_all(notes)
        elif choice ==  "3":
            show_one(notes)
        elif choice == "4":
            break
        else:
            print("无效输入，请重新选择")

main()
