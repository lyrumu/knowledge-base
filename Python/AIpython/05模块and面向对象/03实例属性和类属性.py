"""
实例属性是属于每个对象独立特有的数据 通过__init__传参来为每个实例赋值独特的属性
类属性是所有实例共有的数据或者配置
"""
class Car:
    # 类属性 所有实例共享
    wheel=4
    tax_rate = 0.1
    def __init__(self,brand,name,price):#用于后续创建实例属性
        self.brand=brand
        self.name=name
        self.price=price
#通过创建好的实例来访问属性的时候 会先查找实例属性 实例属性中没有才会查找类属性
#通过类名来访问属性 就只能访问类属性