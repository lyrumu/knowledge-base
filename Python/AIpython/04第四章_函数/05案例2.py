#n的阶乘
def f(n):
    if n==1:
        return n
    return n*f(n-1)
print(f(3))

#电商订单计算器
def all_cost(*args,coupon=0,score=0,express=0):
    """
    计算订单金额
    :param args: 商品信息:名称,价格,数量
    :param coupon: 优惠券
    :param score: 积分
    :param express: 运费
    :return: 最终金额
    """
    total_price = [goods[1]*goods[2] for goods in args]
    total_cost = sum(total_price)
    if total_cost>=5000 and coupon<=total_cost:
        total_cost-=coupon
    if total_cost>=5000 and (score//100)<=total_cost:
        total_cost-=score//100#整除取整
    total_cost+=express
    return total_cost
print(all_cost(("hth",100,19),("zjl",999,2),coupon=300,express=20,score=5000))


