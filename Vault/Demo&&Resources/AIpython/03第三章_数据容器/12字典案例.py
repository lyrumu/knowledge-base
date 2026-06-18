#购物车管理系统
shopping_cart = dict()
#1.制作菜单
print("欢迎使用购物车管理系统")
menu = """
#########购物车系统#########
#      1.添加购物车        #
#      2.修改购物车        #
#      3.删除购物车        #
#      4.查询购物车        #
#      5.退出购物车        #
##########################
"""
print(menu)
#2.执行的操作
choice = -1
while choice != 5:
    choice = int(input("请选择要进行的操作(1-5)"))
    match choice:
        case 1:  # 添加
            good_name = input("请输入商品名称")
            good_price = float(input("请输入商品价格"))
            good_number = int(input("请输入商品数量"))
            if good_name in shopping_cart:
                print("商品已经添加，请重新输入")
            else:
                shopping_cart[good_name] = {"price": good_price, "number": good_number}
                print("商品添加完毕！")
        case 2:  # 修改
            good_name = input("请输入要修改的商品名称")
            if good_name not in shopping_cart:
                print("不存在该商品")
                continue
            good_price = float(input("请输入最新的商品价格"))
            good_number = int(input("请输入最新的商品数量"))
            if good_name not in shopping_cart:
                print("不存在该商品")
            else:
                shopping_cart[good_name] = {"price": good_price, "number": good_number}
                print("修改完毕")
        case 3:  # 删除
            good_name = input("请输入要删除的商品名称")
            if good_name not in shopping_cart:
                print("未添加该商品")
            else:
                del shopping_cart[good_name]
                print("删除完毕")
        case 4:  # 查询
            for good in shopping_cart.keys():
                print(f"{good}:{shopping_cart[good]}")
            print("查询完毕")
        case 5:  # 退出
            print("已退出系统")
        case _:
            print("非法操作！")
