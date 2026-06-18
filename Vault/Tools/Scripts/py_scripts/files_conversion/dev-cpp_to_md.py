import os

def read_cpp(path):
    # Dev-C++ 默认 GBK
    try:
        with open(path, "r", encoding="gbk") as f:
            return f.read()
    except:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except:
            return ""

def merge_cpp_to_one_md(src_dir):
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    output_file = os.path.join(desktop, "all_cpp_merged.md")

    with open(output_file, "w", encoding="utf-8") as out:
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                if file.endswith(".cpp"):
                    cpp_path = os.path.join(root, file)

                    code = read_cpp(cpp_path)
                    if not code:
                        continue

                    # 文件分隔
                    out.write(f"\n# 文件: {file}\n")
                    out.write(f"路径: {cpp_path}\n\n")

                    out.write("```cpp\n")
                    out.write(code)
                    out.write("\n```\n")

    print("完成：已生成单个 md 文件到桌面")


if __name__ == "__main__":
    src_directory = r"F:\C++Note\basic C++\template"#双引号内填写cpp文件的文件夹路径
    merge_cpp_to_one_md(src_directory)