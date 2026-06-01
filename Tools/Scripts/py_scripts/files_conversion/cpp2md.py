import sys
from pathlib import Path


def read_cpp(file_path):
    try:
        return file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return file_path.read_text(encoding="gbk")


def cpp_to_md(cpp_file, output_dir):
    code = read_cpp(cpp_file)

    md_content = (
        f"# {cpp_file.stem}\n\n"
        "```cpp\n"
        f"{code}\n"
        "```\n"
    )

    md_file = output_dir / f"{cpp_file.stem}.md"
    md_file.write_text(md_content, encoding="utf-8")

    print(f"已生成: {md_file.name}")


if len(sys.argv) != 2:
    print("用法:")
    print("python cpp2md.py <cpp文件或文件夹>")
    sys.exit(1)

target = Path(sys.argv[1])

if not target.exists():
    print("路径不存在")
    sys.exit(1)

desktop = Path.home() / "Desktop"
output_dir = desktop / "cpp2md_output"
output_dir.mkdir(exist_ok=True)

# 单文件
if target.is_file():

    if target.suffix.lower() != ".cpp":
        print("不是cpp文件")
        sys.exit(1)

    cpp_to_md(target, output_dir)

# 文件夹
elif target.is_dir():

    cpp_files = list(target.glob("*.cpp"))

    if not cpp_files:
        print("该目录下没有cpp文件")
        sys.exit(1)

    for cpp_file in cpp_files:
        cpp_to_md(cpp_file, output_dir)

    print(f"\n共转换 {len(cpp_files)} 个文件")

else:
    print("未知路径类型")