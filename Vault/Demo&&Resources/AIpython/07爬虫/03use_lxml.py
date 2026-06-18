from lxml import html
print("lxml")
with open("resources/仙逆人物志.html", "r", encoding="utf-8") as f:#先打开resouce中的文件
    html_text = f.read()
    doc = html.fromstring(html_text)#将html文本转化为文档对象
    th_list = doc.xpath("//table/thead/tr/th/text()")#按路径将获取的内容封装到列表里-----解析表头
    print(th_list)
    td_list = doc.xpath("//table/tbody/tr[1]/td/text()")#按路径将获取的内容封装到列表里-----解析第一行内容
    #注意这里的"tr[1]"就是获取第一个表内容 索引是从1开始
    print(td_list)
    #解析所有行数据
    for tr in doc.xpath("//table/tbody/tr"):
        #此时每个tr是一整个<tr>和</tr>内的内容
        every_list = tr.xpath("td/text()")
        print(every_list)
        print("-"*20)



