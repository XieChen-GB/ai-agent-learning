class Contact:
    # 属性：name（姓名）、phone（电话）、email（邮箱，默认为空字符串 ""）
    def __init__(self, name, phone, email=""):
       self.name = name
       self.phone = phone
       self.email = email

    def __repr__(self):
        return (
            f"(name={self.name}, "
            f"phone={self.phone}, "
            f"email={self.email})"
        )

class VIPContact(Contact):
    def __init__(self, name, phone, company, email=""):
        super().__init__(name, phone, email)
        self.company = company

    def __repr__(self):
        return (
            f"(name={self.name}, "
            f"phone={self.phone}, "
            f"company={self.company}, "
            f"email={self.email})"
        )
class ContactBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, contact):
        self.contacts.append(contact)

    def find_by_name(self, name):
        for contact in self.contacts:
            if contact.name == name:
                return contact
        return None
    def delete_by_name(self, name):
        contact = self.find_by_name(name)
        if contact is None:
            return False
        self.contacts.remove(contact)
        return True

    def list_all(self):
        if not self.contacts:
            print("通讯录为空")
            return
        for contact in self.contacts:
            print(contact)

def main():
    book = ContactBook()

    # 普通联系人
    c1 = Contact("张三", "138-0000-0001", "zhang@example.com")
    c2 = Contact("李四", "138-0000-0002")          # email 用默认值
    c3 = Contact("王五", "138-0000-0003", "wang@example.com")

    # VIP联系人
    v1 = VIPContact("赵六", "138-0000-0004", "Anthropic", "zhao@anthropic.com")
    v2 = VIPContact("田七", "138-0000-0005", "Google")   # email 用默认值

    # 添加
    book.add_contact(c1)
    book.add_contact(c2)
    book.add_contact(c3)
    book.add_contact(v1)
    book.add_contact(v2)

    # 列出全部
    print("=== 全部联系人 ===")
    book.list_all()

    # 查找
    print("\n=== 查找 ===")
    result = book.find_by_name("赵六") # 找到，输出 VIPContact 信息
    print(result)    
    result = book.find_by_name("不存在")
    print(result)                          # 输出 None

    # 删除
    print("\n=== 删除后 ===")
    book.delete_by_name("李四")
    book.list_all()

main()


