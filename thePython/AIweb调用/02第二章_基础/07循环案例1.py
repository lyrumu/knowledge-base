a_password = "666888"
a_admin = "admin"
b_password = "123456"
b_admin = "zhangsan"
c_password = "888666"
c_admin = "taoge"
admin = input("请输入账号")
password = input("请输入密码")


while True:
    if (admin==a_admin and password==a_password) or (admin==b_admin and password==b_password) or (admin==c_admin and password==c_password):
        print("登陆成功！")
        break
    elif admin == "" or password == "":
        print("用户名和密码不能为空哦,请重新输入哦哦")
        admin = input("请输入账号")
        password = input("请输入密码")
    else:
        print("用户名或密码错误，请再次输入！")
        admin = input("请输入账号")
        password = input("请输入密码")


