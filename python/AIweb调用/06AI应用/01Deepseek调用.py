# Please install OpenAI SDK first: `pip3 install openai`
import os
from openai import OpenAI#导入openai模块中的一个类
#创建一个openai类的实例client 创建一个与大模型交互的客户端对象
client = OpenAI(
    #这里最好把"DEEPSEEK_API_KEY"设置成环境变量 值设置成自己的API_key 这样api_key就不会暴露了
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")
#与AI大模型进行交互
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个IT界大佬 对待萌新很友好"},
        {"role": "user", "content": "你好 你是谁 能为我做什么?"},
    ],
    stream=False
)
#输出大模型返回的结果
print(response.choices[0].message.content)
#在开发工具中运行 就可以收到大模型的回复
