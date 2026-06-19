email = input("请输入邮箱：")
if email.count("@") == 1 and email.find(".") != -1:
    print("yes")
else:
    print("no")
#也可以用in来判断子串是否在字符串中
email_1 = email[::-1]#翻转字符串
print(email_1)
if email_1==email:#是否为回文字符串
    print("yes")
