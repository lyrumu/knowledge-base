print(10/3)#取小数
print(10//3)#整除，取整
print(10%3)#取余
print(10**3)#幂次方
#优先级就是跟数学一样的
print(0.5-0.4)#输出并非0.1而是0.0999998...
#这是因为计算机底层二进制不能精确表示所有小数，float类型会有精度问题

#案例
x = float(input())
y = float(input())
z = float(input())
avg = (x+y+z)/3
print(avg)

#类似+=。-=，*=这些运算符也都和c++一样可以用
#比较运算符也和c++一样使用，返回值是bool型(True False)
#逻辑运算符and or not
n =  int(input())
print(f"{n}在10-20之间：",10<=n<=20)
#python不等式关系可以写成链式的哦
#简化"n>=10 and n<=20"



