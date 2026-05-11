#元组嵌套,初始固定数据
students = (
("s001","王林",85,92,78),
("s002","李慕婉",92,88,95),
("s003","十三",78,85,82),
("s004","曾牛",88,79,91),
("s005","周铁",95,96,89),
("s006","王卓",76,82,77)
)

print("学号\t\t姓名\t\t语文\t\t数学\t\t语文\t\t总分\t\t平均分")
# #方式一:利用索引
# for i in students:
#     total = i[2]+i[3]+i[4]
#     avg = total/3
#     print(f"{i[0]} \t {i[1]} \t {i[2]} \t {i[3]} \t {i[4]} \t {total} \t {avg:.1f}")# ":.1f"表示浮点数保留一位小数
#方式二:解包
for number,name,chinese,math,english in students:#直接在循环的时候进行解包
    total = chinese+math+english
    avg = total/3
    print(f"{number} \t {name} \t {chinese} \t {math} \t {english} \t {total} \t {avg:.1f}")#保留一位小数
print()#空行换行

#列表推导式
chinese_score = [s[2] for s in students]
math_score = [s[3] for s in students]
english_score = [s[4] for s in students]
print(f"语文最低分:{min(chinese_score)} 语文最高分:{max(chinese_score)} 语文平均分:{sum(chinese_score)/len(chinese_score):.1f}")
print(f"数学最低分:{min(math_score)} 数学最高分:{max(math_score)} 数学平均分:{sum(math_score)/len(math_score):.1f}")
print(f"语文最低分:{min(english_score)} 语文最高分:{max(english_score)} 语文平均分:{sum(english_score)/len(english_score):.1f}")
