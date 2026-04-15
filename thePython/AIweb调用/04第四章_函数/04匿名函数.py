#之前的都是命名函数
#匿名函数就是没有名字的
#用lambda表达式 单行 适用于简单的表达式函数 会自动返回表达式结果
#也就是不需要写return
#格式:lambda 参数列表:函数主体
add=lambda x,y:x+y
print(add(1,2))


#案例：按每个元素的字符个数排序下面的列表
data = ["GO","C","C++","Java","Python","PHP","Rust","JavaScript"]
data.sort(key=lambda item:len(item),reverse=True)
print(data)
#sort函数中的key指的就是“按照什么排序” key是一个函数
#reverse默认是False 也就是按升序 现在改为True 降序
#sort默认是按字典序升序排序 现在按元素字符个数降序排序