import re

def remove_comments(file_path):
    # 读取文件内容
    with open(file_path, 'r') as f:
        content = f.read()

    # 删除单行注释
    content = re.sub(r'(#.*)', '', content)

    # 删除多行注释
    content = re.sub(r'("""[\s\S]*?""")|(\'\'\'[\s\S]*?\')', '', content)

    # 写入文件
    with open(file_path, 'w') as f:
        f.write(content)

# 测试
remove_comments('noise.py')