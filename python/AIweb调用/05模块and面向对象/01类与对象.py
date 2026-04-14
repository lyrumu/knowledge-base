#定义类(有点类似结构体)
class Car:#类名标准是驼峰命名大小写
    pass
#创建对象
c1=Car()
c1.brand = "BMW"#可以动态添加属性！但不推荐
c1.name = "X5"
c1.price = 999999
print(c1.__dict__)
"""
__dict__ 是自定义类对象的一个特殊属性
用于以字典形式存储对象的所有属性
"""
print(c1)


#标准-定义类
#def在类内不叫函数 而叫做方法
class Transport:
    def __init__(self,t_name,t_price,t_brand):#参数列表
#__init__是初始化方法 会被自动调用 主要用于设置对象的属性
        self.name=t_name#后续就会把传入的参数赋值给对象的对应属性
        self.price=t_price
        self.brand=t_brand
#创建对象
t1 = Transport("hth",9090,"China")
print(t1.__dict__)


#定义对象中的方法
class Acar:
    # 初始化方法
    def __init__(self,brand,name,price):
        #self就是代表当前对象 但调用的时候不用为self传参
        self.brand=brand
        self.name=name
        self.price=price
    # 其他方法
    def running(self):
        print(f"{self.brand}{self.name}正在高速行驶...")
    def all_cost(self,discount,rate=0.1):
        return self.price*discount+self.price*rate
a1 = Acar("BMW","X5",999999)
all_cost = a1.all_cost(0.9)
print(f"提车总价为{all_cost:.0f}")
a1.running()
print(a1.__dict__)





