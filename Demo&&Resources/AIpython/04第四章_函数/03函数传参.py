#除了一般的按位置顺序传参 其他的传参方式
#关键字传参
def reg_stu(name,age,gender):
    print(f"注册成功，姓名{name}，年龄{age}，性别{gender}")
    return {"name":name,"age":age,"gender":gender}
stu1 = reg_stu(name="hth",age = 18,gender="male")
print(stu1)
#关键字传参和位置传参混用的时候 位置参数要在前 关键字在后


#默认参数
def reg_stu1(name,age,gender,city="北京"):#city默认参数
    print(f"注册成功，姓名{name}，年龄{age}，性别{gender}，城市{city}")
    return {"name":name,"age":age,"gender":gender,"city":city}
#如果在函数内部对默认参数传参了 还是会使用新的参数的


#不定长参数
#就是传参个数是变化的 不定的
#基于位置参数的不定长参数
def calc_data(*args):#args实际上封装为元组 可以接受多个不定长的参数 注意args并非关键字
    total = sum(args)
    maxs= max(args)
    mins= min(args)
    return total,maxs,mins
print(calc_data(1,2,3,3,4,5,5,6,7,7))
print(calc_data(9,9,9,9,0,0,0))
#基于关键字参数的不定长参数
def calc_data1(*args,**kwargs):#kwargs实际上封装为字典 可以接受不定长的关键字参数
    """
    计算一组不定长数据的最大值最小值平均值
    :param args:不定长数据
    :param kwargs:不定长关键字参数
        round:保留的小数位位数
        print:是否打印输出
    :return:略
    """
    avgs = sum(args) / len(args)
    if kwargs.get("round") is not None:
        avgs = round(avgs,kwargs.get("round"))
    maxs= max(args)
    mins= min(args)
    if kwargs.get("print"):
        print(f"最大值{maxs},最小值{mins},平均值{avgs}")
    return maxs,mins,avgs
print(calc_data1(1,3,4,5,6,6,round=3,print=True))
print(calc_data1(33,44,55,66,round=1,print=False))
#一个*就是基于位置传参 处理函数数量不确定的数据
#两个*就是基于关键字传参 处理函数数量不确定的选项


#参数类型
#函数传参时基本所有数据类型都可以当作参数
#有时函数本身也可以当作一个参数 比如:
def add(a,b):
    return a+b
def sub(a,b):
    return a-b
def calc(a,b,oper):
    return oper(a,b)
result = calc(1,2,add)
ans = calc(1,2,sub)
print(result,ans)
