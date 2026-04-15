import streamlit as st
st.set_page_config(#设置页面配置
    page_title="lyrumu's first streamlit work",#这里设置的是浏览器标签上显示的网站名称
    page_icon="A",#设置浏览器标签的图标
    layout="wide",#默认本来是居中展示 两边空出来 设置成wide的话就是铺满整个页面展示
    #这个是设置侧边栏
    initial_sidebar_state="expanded",
    #这个是设置右上角的菜单 指定跳转的网页
    menu_items={
        'Get Help': 'https://github.com/lyrumu',#注意 streamlit只支持Get Help,Report a bug ,About三个选项 其他的会报错
        'About': "一个基于streamlit的呆呆的一无是处的页面~"
    }
)
st.logo("resources/logo.png")
st.title("其实无限月读挺好")
st.write("“流水落花春去也”")#每一个write是一段
st.write("“天上人间”")
st.image("./resources/music_connects_people.png")#"."表示当前目录
# st.audio()引入音频
# st.video()引入视频
# st.logo()可以为网页左上角设置图标
human={
    "JayChou":["《怎么了》","《好久不见》","《一点点》","《搁浅》"],#注意不要把冒号错写成赋值等号 这里跟JSON格式挺像的 毕竟是数据传输
    "JJ":["《可惜没如果》","《美人鱼》","《醉赤壁》","《曹操》"],
    "DavidTao":["《讨厌红楼梦》","《小镇姑娘》","《二十二》","《找自己》"],
}
st.table(human,border="horizontal")#制表
options=st.multiselect(#多选
    "Whats your favorite singers based on these songs?",
    ["JayChou","JJ","DavidTao"]
)
st.write(f"your favorite singers are{options}")
gender=st.radio("请选择你的性别",["male","female","unknown"],index=2)#单选 index表示默认选择的选项索引
if gender=="male":
    st.write("Please marry me!")
elif gender=="female":
    st.write("Please fuck me!")
else:
    st.write("Choose your gender please!")
advice = st.text_input("说说你对本站的建议吧~")#用户输入
if advice=="":
    st.write("你真的什么也不说吗！！？")
else:
    st.write("Thanks for your advice!")



