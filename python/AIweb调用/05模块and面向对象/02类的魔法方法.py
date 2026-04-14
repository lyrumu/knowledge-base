"""
魔法方法是python中提供的 以双下划线开头结尾的特殊方法
比如__init__ 用于创建对象时初始化
这类方法不需要手动调用 会在合适时机自动调用
有一点点类似运算符重载
"""
#比较两个对象时 默认比较对象的地址！ 而非内部的属性;因此真的比较就需要添加魔法方法
class Car:
    def __init__(self,brand,name,price):
        self.brand=brand
        self.name=name
        self.price=price
    def __str__(self):
        return f"{self.brand},{self.name},{self.price}"
    def __eq__(self,other):#重载“==”运算符
        return self.brand == other.brand and self.name == other.name and self.price == other.price
    def __lt__(self,other):#重载“<”运算符
        return self.price < other.price
    def __gt__(self,other):#重载“>”运算符
        return self.price > other.price
    def __le__(self,other):return self.price <= other.price#重载“<=”运算符
    def __ge__(self,other):return self.price >= other.price#重载“>=”运算符
c1 = Car("hth","china",66666)
c2 = Car("zjl","china",9999999)

print(c1,c2)#本来的话会输出十六进制地址 现在会按__str__格式输出字符串
print(c1==c2)#本来无法比较 重载后可以正常比较
print(c1<c2)
print(c1>c2)


