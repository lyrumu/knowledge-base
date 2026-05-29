# 选修足球学生名单
football_set = {"王林", "曾牛", "徐立国", "通天", "天运子", "韩立", "厉飞雨", "乌丑", "紫灵"}
# 选修篮球学生名单
basketball_set = {"张铁", "墨居仁", "王林", "姜老道", "曾牛", "王蝉", "韩立", "天运子", "李化元", "厉飞雨", "云露"}
# 选修法语学生名单
french_set = {"许木", "王卓", "十三", "虎咆", "姜老道", "天运子", "红蝶", "厉飞雨", "韩立", "曾牛"}
# 选修艺术学生名单
art_set = { "通天", "天运子", "韩立", "虎咆", "姜老道", "紫灵"}

#找出同时选修法语和艺术的学生
#方法一
fa_set = french_set.intersection(art_set)
print(fa_set)
#方法二
fa_set2 = french_set & art_set#可以用“&”符号表示交集
print(fa_set2)

#找出同时选修四门课的学生
all_set = football_set & basketball_set & french_set & art_set
print(all_set)

#找出选修足球但没选篮球的学生
#方法一
fb_set = football_set.difference(basketball_set)
print(fb_set)
#方法二
fb_set2 = football_set-basketball_set#可以用“-”表示difference差集
print(fb_set2)
#方法三,集合推导式,类似于列表
print({s for s in football_set if s not in basketball_set})

#统计每个学生的选课数量
unite_set = football_set.union(basketball_set).union(art_set).union(french_set)
print(unite_set)
#或者用“|”表示并集
unite_set2 = football_set|basketball_set|art_set|french_set
print(unite_set2)
#现在已经获得所有学生的名单,再用list获取所有选过的课程
unite_list = [*football_set,*basketball_set,*art_set,*french_set]#先解包再组包
print(unite_list)
for s in unite_set2:
    print(f"{s}选修了{unite_list.count(s)}门课程")
