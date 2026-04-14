# list1 = [19,23,54,64,875,20,109,232,123,54]
# list2 = [55,80,72,35,60,123,54,29,91]
# for i in list1:
#     list2.append(i)
# list3 = []
# for i in list2:
#     if i in list3:#python可以直接这样判断list3中是否已经存在数值i
#         continue
#     list3.append(i)
# list3.sort()
# print(list3)


#简化版本1
list1 = [19,23,54,64,875,20,109,232,123,54]
list2 = [55,80,72,35,60,123,54,29,91]
#解包：加*，表示将列表这一类容器拆成一个个元素，然后就可以将这些元素放到一个新的列表list3里面了
#组包：顾名思义就是将独立的元素组成一个容器整体？
list3 = [*list1,*list2]
list4= []
for i in list3:
    if i in list4:#python可以直接这样判断list3中是否已经存在数值i，（或者“not in”也可判断）
        continue
    list4.append(i)
list4.sort()
print(list4)

#简化版2
# list5 = list1+list2#直接可以相加合并（但不去重）
# print(list5)
