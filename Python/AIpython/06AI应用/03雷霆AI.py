import streamlit as st
import os#操作系统模块
from openai import OpenAI
import json#用json数据包保存会话记录
from datetime import datetime#引入时间库 作为每一个会话记录的名称
#配置页面
st.set_page_config(
    page_title="雷霆AI",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/lyrumu',
        'About': "一个基于streamlit的AI糖糖伴侣！"
    }
)
#保存会话记录函数
def save_session():
    if st.session_state.cur_session:
        session_data = {
            "lover": st.session_state.lover,
            "character": st.session_state.character,
            "cur_session": st.session_state.cur_session,
            "messages": st.session_state.messages
        }
        # 创建文件夹
        if not os.path.exists("sessions"):
            os.mkdir("sessions")
        with open(f"sessions/{st.session_state.cur_session}.json", "w", encoding="utf-8") as f:
            json.dump(session_data,f, ensure_ascii=False, indent=2)
#生成文件名函数
def generate_session_id():
    return datetime.now().strftime("%Y-%m-%d_%H_%M_%S")#注意不要用冒号 文件名不能包含冒号
#加载所有会话列表信息
def load_sessions():
    session_list=[]
    if os.path.exists("sessions"):
        file_list=os.listdir("sessions")#列出目录所有文件
        for file_name in file_list:
            if file_name.endswith(".json"):
                session_list.append(file_name[:-5])#“.json”不需要 所以用一个切片
    session_list.sort(reverse=True)#将最新会话记录显示在会话列表最上方
    return session_list
#加载指定会话信息
def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            with open(f"sessions/{session_name}.json","r",encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.lover = session_data["lover"]
                st.session_state.character = session_data["character"]
                st.session_state.messages = session_data["messages"]
                st.session_state.cur_session = session_name
    except Exception as e:
        st.error("加载失败了哦",e)
#删除指定会话
def delete_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json")
            if session_name==st.session_state.cur_session:
                st.session_state.cur_session=generate_session_id()
                st.session_state.messages=[]
    except Exception as e:
        st.error("删除失败了哦",e)
#保存当前会话记录名称
if "cur_session" not in st.session_state:
    cur_time = generate_session_id()#获取当前系统准确时间
    st.session_state.cur_session= cur_time
#保存侧边栏历史信息
#昵称
if "lover" not in st.session_state:
    st.session_state.lover = "你的伴侣"
#性格
if "character" not in st.session_state:
    st.session_state.character = "温柔"
#侧边栏
#想让元素出现在侧边栏 要么每个都加上.sidebar 要么用with
with (st.sidebar):
    st.header("伴侣控制面板")
    #新建会话按钮
    if st.button("新建聊天",width="stretch",icon="🥚"):
        #保存当前会话
        save_session()
        #创建新的会话
        if st.session_state.messages:#只有当前已经进行了会话 点击按钮才会创建新的空会话 更合理
            st.session_state.messages=[]#每次会话都从空文件开始 昵称和性格不管也没事
            st.session_state.cur_session=generate_session_id()
            save_session()
    #显示会话列表
    st.text("聊天记录")
    session_list=load_sessions()
    for log in session_list:
        col1,col2=st.columns([4,1])#将会话记录按钮和删除按钮按一定比例展示在同一行
        with col1:
            if st.button(log,width="stretch",icon="📖",type="primary" if log==st.session_state.cur_session else "secondary"):#进入所要加载的会话
                load_session(log)
                st.rerun()
        with col2:
            if st.button("",width="stretch",icon="❌️",key=f"{log}"):#删除所选的会话
                #如果不加key 每个删除会话按钮都是同一个label 会报错 所以加key确定唯一性是必要的
                delete_session(log)
                st.rerun()
    #分割线
    st.divider()
    #伴侣信息
    nickname = st.text_input("昵称", placeholder="写上你希望的伴侣名字")
    if nickname:
        st.session_state.lover = nickname
    like=st.text_area("性格",placeholder="写上你期望ta的性格")
    if like:
        st.session_state.character = like

#页面标题
st.title("雷霆AI")
st.logo("resources/logo.png")
#系统提示词 待输入
system_prompt = f"""
你叫{st.session_state.lover}，现在是用户的真实伴侣，请完全代入伴侣角色。
规则：
1. 每次只回1条消息
2. 禁止任何场景或状态描述性文字
3. 匹配用户的语言
4. 回复简短，像微信聊天一样
5. 有需要的话可以用❤️💓等emoji表情
6. 用符合伴侣性格的方式对话
7. 回复的内容，要充分体现伴侣的性格特征
伴侣性格：
{st.session_state.character}
你必须严格遵守上述规则来回复用户。
"""
#用于定义提示词消息输入框
prompt=st.chat_input("问些雷霆问题吧~")
#初始化历史聊天信息的保存
if 'messages' not in st.session_state:#messages存储当前会话的所有聊天记录
    st.session_state.messages=[]
st.text(f"当前会话:{st.session_state.cur_session}")
#展示历史聊天信息
#每次重新输入提示词 整个代码都会重头跑一遍 所以每次遍历更新后的列表打印出来即可
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])
    # if message["role"]=="user":
    #     st.chat_message("user",avatar="🫦").write(message["content"])
    # elif message["role"]=="assistant":
    #     st.chat_message("assistant",avatar="💩").write(message["content"])
if prompt:
    #chat_message()用于显示输入输出的信息
    st.chat_message("user",avatar="🫦").write(prompt)
    #这里只用一个图标 多个会无法渲染而报错的
    print("---->调用大模型,提示词为：",prompt)#这个不会显示在网页 而是显示在终端 提供日志来调试
    #保存用户提示词
    st.session_state.messages.append({"role": "user", "content":prompt})
    #接下来调用AI大模型
    client = OpenAI(
        api_key=os.environ.get('DEEPSEEK_API_KEY'),
        base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            #历史聊天记录此时已经包含最新输入的提示词
            #历史聊天记录是一个列表 每一个元素是字典 因此解包即可
            #就解决了会话记忆的问题
            *st.session_state.messages,
        ],
        stream=True#流式输出
    )

    #以下为非流式输出的输出代码
    # print("<-----大模型返回结果:",response.choices[0].message.content)#这里也是为了调试 提供日志
    # st.chat_message("assistant",avatar="💩").write(response.choices[0].message.content)
    # #只写到这里的话 每次对话都会覆盖上一次的
    # st.session_state.messages.append({"role": "assistant", "content":response.choices[0].message.content})

    response_message=st.empty()#每次创建一个空对象 用来保存大模型返回的完整结果 以便流式输出
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant",avatar="💩").write(full_response)#完成流式输出
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    #每次大模型回复 也需要保存会话
    save_session()