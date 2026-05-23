def validate_phone(phone):
    return phone.isdigit() and len(phone) >=7 and len(phone) <=15

def format_contact(contact):
    email_format = contact["email"] if contact["email"] else "无邮箱"
    return f"{contact['name']} | {contact['phone']} | {email_format}"
