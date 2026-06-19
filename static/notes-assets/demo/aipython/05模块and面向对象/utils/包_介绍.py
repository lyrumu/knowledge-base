#导入模块
"""
(1)
import utils.my_fun
utils.my_fun.separator()
(2)
from utils import my_fun
my_fun.separator()
(3)
from utils import *
#若想通过这种方式导入包中的所有模块 需要在init文件中写好__all__ 否则会报错
my_fun.separator()
"""
#导入模块具体功能
"""
(1)
from utils.mt_fun import separator()
(2)
from utils.my_fun import *
#以上大部分都是相对路径
#但有些时候可能会要用绝对路径来导入~
"""