def process_text(text,fun):
    return fun(text)

def to_upper(t):
    return t.upper()

def add_brackets(t):
    return f"【{t}】"

print(process_text("abcdefg", to_upper))

print(process_text("abcdefg", add_brackets))