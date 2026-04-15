#列表用[],可以存储不同类型数据。元素是有序的，可重复，可修改
#第一个元素的索引是0
#倒数第一个元素的索引是-1，反向索引
s = [1,2,3,4,5,'a',True,1.314]
# print(type(s))#列表的类型是List
# for i in s:
#     print(type(i))
#
# #获取
# print(s[0])
# print(s[-1])
# print(s[2])
# #修改
# s[5] = "change"
# print(s)
# #删除
# del s[2]#删除用del（delete）
# print(s)

#列表切片
#开始索引默认0，结束索引默认len(s)，步长默认1
# print(s[::])#正向输出整个列表
# print(s[::-1])#逆向输出整个列表
# print(s[-1:0:-1])
# print(s[0:-2:1])


#列表相关函数
s.append("love")#在尾部追加一个元素
print(s)
s.insert(0,"i")#在索引前，插入一个元素
print(s)
s.remove("a")#删除第一个遇到的与参数a相同的元素
print(s)
s.pop()#pop(索引）->删除指定索引元素，不指定默认删除最后一个
print(s)
s.pop(-1)
print(s)
s.reverse()#翻转列表
print(s)