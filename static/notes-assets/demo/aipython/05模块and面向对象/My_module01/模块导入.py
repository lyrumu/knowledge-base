#导入模块--->通过 模块名.功能名来调用
import random as rd
for i in range(100):
    print(rd.randint(1,100))


#导入模块中的功能--->就可以直接通过功能名调用
from random import randint
for i in range(10):
    print(randint(1,10))
#可以 from random import * 来导入random中的所有功能 然后直接使用功能名调用
