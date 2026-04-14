# while后可以跟else，表示循环结束后执行
cnt = 0
while cnt<10:
    print("人生苦短，我用python")
    cnt+=1
else:
    print("执行完毕")



# 累加1-100的偶数
i = 1
sum_1 = 0
while i<=100:
    if i%2==0:
        sum_1+=i
    i+=1
else:
    print(sum_1)
    print("累加完毕")


# for循环
# 遍历字符串,计算字符串长度
cnt = 0
msg = input("请输入一个字符串")
for i in msg:
    cnt+=1
else:
    print(f"字符串长度是{cnt}")



"""
range语句
range(end):表示从0-end，但不包括end
range(start,end):表示从start到end-1
range(start,end,step):step表示步长，每次走几步，不包括end的
"""
total = 0
for i in range(1,101):
    if i%2==1:
        total += i
print(total)



# print()自带换行效果，每次执行都会换行；即默认print(,end="\n")
a = int(input())
b = int(input())
for i in range(a):
    for j in range(b):
        print("*",end="")#让print以空字符结尾而非换行符
    print()#每结束一行执行一次print来换行


#打印乘法口诀表
for i in range(1,10):
    for j in range(1,i+1):
        print(f"{j}*{i}={i*j}",end="\t")#用制表符会比较整齐
    print()