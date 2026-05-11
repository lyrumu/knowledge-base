#定义常量 名称一般用大写
PI = 3.1415926
NAME = "hth"
#__all__ : Python内置变量 用于控制“*”导入模块时导入哪些功能
#__all__ = ["separator","separator1"]
#函数
def separator():
    print("- "*20)
def separator1():
    print("+ "*20)
def separator2():
    print("# "*20)
def separator3():
    print("* "*20)
#测试函数
#__name__ : Python中的内置变量 表示当前模块的名字(直接运行当前模块 __name__=__main__ ; 导入后运行则__name__=模块名)
#因此 直接执行当前文件 会执行如下代码 当作模块导入的话不执行
if __name__ == '__main__':
    separator()