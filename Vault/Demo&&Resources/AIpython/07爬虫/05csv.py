#comma-separated-values
#逗号分割值
#用于存储表格数据 可以直接用Excel打开
#编码选择ANSI系统编码

#文件操作原始方式
# with open("csv_data/csv入门.csv","w",encoding="utf-8") as f:
#     f.write("姓名,年龄,性别,爱好\n")#表头
#     f.write("蔡徐坤,30,男,'篮球,music'\n")#数据
#     f.write("周杰伦,45,男,太阳之子\n")


#csv模块操作
#写
import csv
with open("csv_data/02.csv","w",encoding="utf-8",newline="") as f:#newline参数解决换行问题
    writer=csv.DictWriter(f,fieldnames=["姓名","年龄","性别","爱好"])#先定义表头
    #调用DictWriter写表头
    writer.writeheader()
    writer.writerow({"姓名":"周杰伦","年龄":45,"性别":"男","爱好":"太阳之子"})
    writer.writerow({"姓名":"蔡徐坤","年龄":30,"性别":"男","爱好":"篮球,music"})
    writer.writerow({"姓名":"王源","年龄":28,"性别":"男","爱好":"篮球,rap"})
#读
with open("csv_data/02.csv","r",encoding="utf-8") as f:
    reader=csv.DictReader(f)
    for row in reader:
        print(row)
        #使用csv模块后可以基于字典键值对解析特定内容
        print(row["姓名"])



