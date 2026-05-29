#set集合会自动去重
#无序！可修改，不重复
#用"{}",但是空的{}不表示空集合，而是表示字典的
#无法用下标索引（无序的嘛）
new_set = {1,1,1,1}
new_set3 = {1,2,3,4}
print(new_set)
print(type(new_set))

#定义空集合
new_set1 = set()#正确
print(type(new_set1))
fake_blank_set = {}#错误,这样是字典
print(type(fake_blank_set))

#常用方法
new_set.add(2)#添加元素
print(new_set)

a = new_set.difference(new_set3)#取new_set中有的但是new_set3中没有的元素，反过来是不一样的哦
print(a)

b=new_set.union(new_set3)#取并集
print(b)

c=new_set.intersection(new_set3)#取交集
print(c)

new_set.remove(2)#删除指定元素，若元素不存在会报错
print(new_set)

new_set.clear()#清空集合
print(new_set)

#还有，set_name.pop()会随机删除一个元素并返回被删除的元素