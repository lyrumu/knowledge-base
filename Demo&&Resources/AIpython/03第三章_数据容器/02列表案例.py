s = []
total = 0
print("请输入10个数字：")
for i in range(10):
    num = int(input())
    total+=num
    s.append(num)
s.sort()
print(s)
print("average = ",sum(s)/len(s))#这里不用total，而是用sum和len函数来计算平均值哦
