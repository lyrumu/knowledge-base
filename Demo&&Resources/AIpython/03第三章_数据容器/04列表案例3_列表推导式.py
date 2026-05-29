#列表推导式：按一定规律快速生成一个列表
#语法：s = [要插入列表的表达式 for i in 列表/序列]
num_list = [i**2 for i in range(1,21)]#把1-20每个数的平方插入列表

#只把1-20中的奇数的平方插入列表呢
new_list = [i**2 for i in range(1,21) if i%2==1]#后面可以跟if语句来限制条件
print(new_list)
