score = int(input())
if score >= 700:#判断条件的结果一定要是bool型
    print("可能能上清华")
else:
    print("几乎不可能上清华")
#if语句也是用Tab缩进来表示if语句块
#缩进很严格 不能多也不能少

account = input("请输入你的账号：")
password = input("请输入你的密码：")
real_account = "1111"
real_password = "12345"
if account == real_account and password == real_password:
    print("yes")
else:
    print("no")

year = int(input("请输入年份"))
if (year%4==0 and year%100!=0) or year%400==0:
    print(f"{year}年是闰年")
else:
    print(f"{year}年是平年")


number = int(input("请输入一个整数"))
if number>0:
    print(f"{number}是正数")
elif number<0:
    print(f"{number}是负数")
else:
    print(f"{number}是0")

#案例：判断三角形类型
a = int(input("请输入三角形边长a:"))
b = int(input("请输入三角形边长b:"))
c = int(input("请输入三角形边长c:"))
if a+b>c and a+c>b and b+c>a:
    if a==b==c:#pyhton可以连等
        print(f"{a},{b},{c}能构成等边三角形")
    elif a==b or b==c or a==c:
        print(f"{a},{b},{c}能构成等腰三角形")
    else:
        print(f"{a},{b},{c}能构成普通三角形")
else:
    print(f"{a},{b},{c}不能构成三角形")

#match case
day = int(input("请输入星期几"))
match day:
    case 1 if day==1:#case后可以跟if追加条件**
        print(1)
    case 2:
        print(2)
    case 3|4:#竖线表示“或者”
        print(3+4)
    case _:#用下划线表示“else”
        print("nothing")

a = int(input())
b = int(input())
print(f"{a}+{b} = {a+b}")#这个写法稍稍留意奥
