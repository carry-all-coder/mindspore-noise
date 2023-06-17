import re
import os

# 定义一个函数，用于读取文件内容并去除注释
def remove_comments(file_path):
    # 读取文件内容
    with open(file_path, "r") as f:
        content = f.read()

    # 去除单行注释
    content = re.sub(r"^\s*#.*?$", "", content, flags=re.MULTILINE)

    # 去除多行注释
    content = re.sub(r"^\s*'''.*?'''", "", content, flags=re.MULTILINE|re.DOTALL)
    content = re.sub(r'^\s*""".*?"""', "", content, flags=re.MULTILINE|re.DOTALL)

    # 将去除注释后的内容写回原文件
    with open(file_path, "w") as f:
        f.write(content)

    # 返回文件路径，方便输出提示信息
    return file_path

# 示例：删除文件中的注释并输出结果
file_path = "phase_noise.py"
result_path = remove_comments(file_path)
print("注释已删除并保存到文件：", os.path.abspath(result_path))