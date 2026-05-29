#用于明确变量的数据类型
#虽然python解释器会类型推断出一些变量的类型 但前提是该变量已经被赋值 就是根据值 来推断变量的类型的
#明确之后 编写代码之后若出现数据类型冲突 就百分百会报错了
#但是这些都是提示 并不会强制检查 python是动态的
a:int = 10
score:float=95.5
hobby:str="python"
flag:bool=True
names:list[str]=["hth","zjl"]
phones:set[str]={"19734005711","15858238845"}
options:dict[str,int]={"count":0,"total":0}
goods:tuple[str,int,int]=("666",6969,2778)
#表示存放字符串或者整形的列表
objects:list[str|int]=[1,2,3,"666"]#竖线分隔


#函数的类型注解
#指定参数数据类型同上 指定返回值数据类型用箭头->
def calc(scores:list[int])->float:
    total=0
    for s in scores:
        total+=s
    return total

