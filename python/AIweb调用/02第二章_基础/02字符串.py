#占位符,自动转换为字符串，不需要主动进行类型转换
s = "COke"
print("大家好 我是%s"%s)
#如果有多个需要占位符
name = "hth"
age = 22
pro = "软件工程"
hobby = "running"
print("我叫%s,我的年龄是%s,我学的专业是%s,我的爱好是%s"%(name,age,pro,hobby))
#多个占位符
a = 18
print("我今年"+str(a)+"岁")#‘+’只能连接字符串和字符串，
# 需要用str()转换


#推荐方式-->f"内容{变量或者表达式}内容"
Name = "Eren"
print(f"我的名字是{Name}")

