contact_list = [
    {"name" : "张三", "phone" : "090-1111-1111", "email" : "zhang@example.com"},
    {"name" : "李四", "phone" : "090-2222-2222", "email" : "li@example.com"},
    {"name" : "王五", "phone" : "090-3333-3333", "email" : "wang@example.com"}
]

# 打印所有联系人
for record in contact_list:
    print(f"姓名： {record['name']} | 电话： {record['phone']} | 邮件： {record['email']}")

# 添加联系人
contact_list.append({"name" : "谢晨", "phone" : "070-1234-5678", "email" : "xie@example.com"})

# 查找练习人
find_people = "谢晨"
for record in contact_list:
    if record["name"] ==  find_people:
        print(f"找到 {record['name']} | 电话： {record['phone']} | email: {record['email']}")
        break

# 删除王五
contact_list = [record for record in contact_list if record["name"] != "王五"]    

# 打印所有邮件（列表推导式）
emails = [record["email"] for record in contact_list]
print(emails)