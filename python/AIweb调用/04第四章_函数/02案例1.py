def triangle_area(d,h):
    """
    计算三角形面积
    :param d: 底
    :param h: 高
    :return: 面积
    """
    return d*h/2

def vowel_cnt(s):
    """
    计算字符串的元音字符个数
    :param s: 字符串
    :return: 元音字符个数
    """
    cnt = 0
    for c in s:
        if c in "aeiouAEIOU":
            cnt += 1
    return cnt

def scores(score_list):
    """
    计算学生成绩的最高最低以及平均分
    :param score_list: 学生成绩列表
    :return: 略了
    """
    maxs = max(score_list)
    mins = min(score_list)
    avg = round(sum(score_list)/len(score_list),3)
    return maxs,mins,avg

