"""
/ 从根节点找直接子元素
// 从任意位置选择节点
. 从当前节点下查找
[n] 第n个元素
[last()] 最后一个元素
text() 获取文本内容
p[@attr] 获取p标签中带有attr属性的内容
p[@attr='value'] 获取p标签中明确属性值的内容
//body/div/* 获取div下的所有元素
‘*’就是一个通配符
"""
from lxml import html
print("lxml")
with open("resources/仙逆人物志.html", "r", encoding="utf-8") as f:#先打开resouces中的文件
    html_text = f.read()
    doc = html.fromstring(html_text)#将html文本转化为文档对象
    th_list = doc.xpath("//table/thead/tr/th/text()")#按路径将获取的内容封装到列表里-----解析表头
    print(th_list)

