#异常处理
"""
当程序出现异常时 "异常处理"能够帮助程序入PLAN B 而不是直接崩溃停止
能够让程序继续进行
"""
try:
    #一但在try中检测到错误 try中剩余的代码就不会再执行
    #之后执行except中的代码 来处理错误
    print("======================")
    print(my_name)
    print("======================")
    #...
except NameError as e:
    #except用于捕获并进一步处理异常 但只有当发生的异常类型和规定的一致才可以捕获
    #比如在这里 必须是NameError类型的错误才会被捕获
    #会一个个except去尝试
    print(f"异常信息是{e}")
except ZeroDivisionError as e:
    print(f"0不能作为除数 {e}")
except IndexError as e:
    print(f"索引出错! {e}")
except Exception as e:
    #Exception会兜底 能捕获所有类型的异常
    print("程序出错 请联系管理员")
    print(e)
    #finally代码块是无论如何都会运行的代码块 不受其他影响 不是必须写的
finally:
    print("资源释放成功")

#异常传递
"""
出现异常时 异常信息会被层层上报 直到被处理 或者最后崩溃返回在控制台
"""


