# 1.计算三角形面积
def triangle_area(b, h):
    return b * h / 2


print("面积: ", triangle_area(30, 20))


# 2.统计元音字母
def count_vowel(s):
    count = 0
    for c in s:
        if c in 'aeiouAEIOU':
            count += 1
    return count


print(count_vowel("Hello Python Hello World OK"))


# 3: 计算学员成绩最高分、最低分、平均分(保留1位小数)
def calc_score(score_list):
    return max(score_list), min(score_list), round(sum(score_list) / len(score_list), 1)


s_list = [589, 609, 605, 643, 677, 455, 477, 489, 503]
max_score, min_score, avg_score = calc_score(s_list)
print("最高分: ", max_score)
print("最低分: ", min_score)
print("平均分: ", avg_score)
