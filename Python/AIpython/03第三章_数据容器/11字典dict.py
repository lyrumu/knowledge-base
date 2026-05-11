#dict就是一种键值对,类似C++中的map
#键不能重复,且必须为不可变类型,可修改

#定义空字典
a = dict()
b = {}

#查找
dict1 = {"a":1,"b":2,"c":3}
value = dict1["a"]#查找键对应的值
print(value)#或者dict1.get(key)

keys = dict1.keys()#获取所有键
print(keys)
values = dict1.values()#获取所有值
print(values)
items = dict1.items()#获取所有键值对
print(items)

#修改值
dict1["a"] = 0
print(dict1["a"])

#添加键值对
dict1["hth"] = 10
print(dict1)

#删除键值对
dict1.pop("a")#方法一
print(dict1)
del dict1["b"]#方法二
print(dict1)

#遍历字典
for key in dict1.keys():#方法一
    print(f"{key}:{dict1[key]}")
for k,v in dict1.items():#方法二
    print(f"{k}:{v}")

