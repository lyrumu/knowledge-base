#打开文件
#如果文件不存在会自动创建一个
f = open("resources/poem.txt","r",encoding="utf-8")#"r"表示read
#读文件
content=f.read()
print(content)
#关闭文件(很重要
f.close()

#写文件
f0=open("resources/poem.txt","w",encoding="utf-8")#"w"表示write
f0.write("hello world")
f0.close()
#为了防止程序中断而没有close文件 一般把close写在finally块里面

#但更推荐的方式是 使用with
#文件会自动close
with open("resources/poem.txt","w",encoding="utf-8") as f:
    f.write("hello world")
