#定义eg
def outline():
    print("--------------------")
#调用
outline()
#其余基本都和C++一样的,不多说了


def sc(a):
    return round(3.14*a*a,2),round(2*3.14*a,2)
    #round函数用于控制保留小数位数
    #返回多个内容的话就用逗号分开，输出会封装到元组里
    #调用获得多个返回值的话，可以用解包，给多个变量赋值
r = float(input("请输入半径"))
s,c = sc(r)
print(f"面积{s},周长{c}")


#函数的说明文档
#写在函数开头 用三引号包裹
def ball_area(e):
    """
    用于计算球的表面积
    :param e: 球的半径
    :return: 球的表面积
    """
    area = 4*3.1415926*e*e
    return area
print(ball_area(4))
#查看函数说明文档
help(ball_area)
#或者按住Ctrl 鼠标浮在某个函数上然后点击函数 也可查看说明文档


#在函数内部想要定义全局变量 使用global关键字
debug_mode = False
def open_debug_mode():
    global debug_mode#全局变量
    debug_mode = True
    print("调试模式已打开")
