import requests
import csv
from lxml import html


"""
这个部分要结合html网页结构复习
核心就是自己借助浏览器寻找准确html路径xpath
并且随着时间推移网站可能会有变化 所以需要不断更新程序
"""
MOVIE_LIST_FILE = "csv_data/movie_list.csv"
URL = "https://www.themoviedb.org/"
TARGET_URL = "https://www.themoviedb.org/movie/top-rated"#直接访问 默认只访问界面第一页的信息 需要在页面点击“载入更多”才能刷新


#保存电影信息为csv文件
def save_movie(movie_info):
    with open(MOVIE_LIST_FILE,"w",encoding="utf-8",newline="") as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames = ["名称","年份","上映时间","类型","时长","评分","语言","作者","导演","简介","标语"])
        writer.writeheader()
        writer.writerows(movie_info)


#获取电影详情信息
def get_movie_info(movie_url):
    movie_html = requests.get(movie_url,timeout=100).text
    print(f"发送请求给电影{movie_url}")
    movie_doc = html.fromstring(movie_html)
    #获取电影名称
    #去浏览器f12 获取xpath
    movie_name_list = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/a/text()")
    #获取年份
    movie_year_list = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/span/text()")
    #获取上映时间
    movie_time_list = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[2]/text()")
    #电影类型
    movie_type_list = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[3]/a/text()")
    #电影时长
    movie_lasting_list = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[4]/text()")
    #电影评分
    #这里需要在html网页里上下文找到需要的属性->data-percent
    movie_score_list = movie_doc.xpath("//*[@id='consensus_pill']/div/div[1]/div/div/@data-percent")
    #电影语言
    movie_language_list = movie_doc.xpath("//*[@id='media_v4']/div/div/div[2]/div/section/div[1]/div/section[1]/p[3]/text()")
    #电影作者
    movie_author_list = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/ol/li[2]/p[1]/a/text()")
    #电影导演
    movie_director_list = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/ol/li[1]/p[1]/a/text()")
    #电影简介
    movie_introduction_list = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/div/p/text()")
    #电影标语
    movie_slogan_list = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/h3[1]/text()")

    #最后将以上内容封装到字典
    movie_info = {
        #用strip()去除空格
        #用if 判断是否为空
        #用.join()连接列表
        "名称":movie_name_list[0].strip() if movie_name_list else '',
        "年份":movie_year_list[0].strip() if movie_year_list else '',
        "上映时间":movie_time_list[0].strip() if movie_time_list else '',
        "类型":",".join(movie_type_list).strip() if movie_type_list else '',
        "时长":movie_lasting_list[0].strip() if movie_lasting_list else '',
        "评分":movie_score_list[0].strip() if movie_score_list else '',
        "语言":movie_language_list[0].strip() if movie_language_list else '',
        "作者":",".join(movie_author_list).strip() if movie_author_list else '',
        "导演":",".join(movie_director_list).strip() if movie_director_list else '',
        "简介":movie_introduction_list[0].strip() if movie_introduction_list else '',
        "标语":movie_slogan_list[0].strip() if movie_slogan_list else ''
    }
    # print(movie_info)
    return movie_info


#主函数 核心逻辑
def main():
    html_text = requests.get(TARGET_URL,timeout=60).text
    print("正在发送请求...获取TMDB高分榜单数据")
    #timeout表示请求可 超时的时间范围
    doc = html.fromstring(html_text)
    #从浏览器找到html文件中想要的结构路径 复制Xpath
    movie_list = doc.xpath("//*[@id='page_1']/div[@class='card style_1']")
    all_movies = []#用来存储所有电影的信息
    for movie in movie_list:
        movie_url = movie.xpath("./div/div/a/@href")#在当前目录下继续找 找到该部电影的详细url
        if movie_url:#如果存在
            movie_info_url=URL+movie_url[0]#得到该部电影准确url地址!!
            # print(movie_info_url)
            movie_info = get_movie_info(movie_info_url)
            #保存数据为csv文件
            all_movies.append(movie_info)
    print("已经获取所有电影详情 准备保存到csv文件")
    save_movie(all_movies)#存入csv表格


if __name__ == "__main__":#运行时调用
    main()