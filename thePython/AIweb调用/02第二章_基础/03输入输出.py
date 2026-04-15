# #输入,键盘无论输入什么数据 都当作字符串类型看待**
# name = input("请输入您的姓名")#可以直接在里面写提示信息
# print(f"欢迎您，{name}")

#案例
money = 10000
password = input("请输入密码：")
print(f"密码正确,{password}")
num = input("请输入取款金额")
#先将num转换为int型
print(f"剩余金额{money-int(num)}")

