import random
import re
import time

import requests
from lxml import html
import csv

TMDB_BASE_URL = 'https://www.themoviedb.org'
TMDB_TOP_PAGE_1_URL = '/movie/top-rated'
TMDB_TOP_PAGE_OTHER_URL = '/discover/movie/items'
TMDB_TOP_PAGE_OTHER_BODY = 'air_date.gte=&air_date.lte=&certification=&certification_country=TW&debug=&first_air_date.gte=&first_air_date.lte=&include_adult=false&include_softcore=false&latest_ceremony.gte=&latest_ceremony.lte=&page=%d&primary_release_date.gte=&primary_release_date.lte=&region=&release_date.gte=&release_date.lte=2026-09-28&show_me=everything&sort_by=vote_average.desc&vote_average.gte=0&vote_average.lte=10&vote_count.gte=300&watch_region=TW&with_genres=&with_keywords=&with_networks=&with_origin_country=&with_original_language=&with_watch_monetization_types=&with_watch_providers=&with_release_type=&with_runtime.gte=0&with_runtime.lte=400'

TOP_MOVIE_CSV_PATH = 'csv_data/top_movies.csv'
TOP_MOVIE_NUM = 100

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://www.themoviedb.org/",
    "Accept-Language": "zh-CN,zh;q=0.9"
}


def get_movie_detail(movie_detail_url):
    time.sleep(random.uniform(0.5, 1.5))
    print(f"开始获取电影详情... url:{movie_detail_url}")

    response = requests.get(movie_detail_url)

    movie_doc = html.fromstring(response.text)
    movie_names = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/a/text()")  # 电影名称
    movie_years = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/span/text()")  # 上映年份
    movie_dates = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[2]/text()")  # 上映时间
    movie_tags = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[3]/a/text()")  # 类型
    movie_cost_times = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[4]/text()")  # 时长
    movie_scores = movie_doc.xpath("//*[@id='consensus_pill']/div/div[1]/div/div/@data-percent")  # 评分
    movie_languages = movie_doc.xpath(
        "//*[@id='media_v4']/div/div/div[2]/div/section/div[1]/div/section[1]/p[3]/text()")  # 语言
    movie_directors = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/ol/li[1]/p[1]/a/text()")  # 导演
    movie_authors = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/ol/li[2]/p[1]/a/text()")  # 作者
    movie_slogans = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/h3[1]/text()")  # 宣传语
    movie_descriptions = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/div/p/text()")  # 简介

    movie_info = {
        "电影名": movie_names[0].strip() if movie_names else '',
        "年份": movie_years[0].strip() if movie_years else '',
        "上映时间": movie_dates[0].strip() if movie_dates else '',
        "类型": ",".join(movie_tags) if movie_tags else '',
        "时长": movie_cost_times[0].strip() if movie_cost_times else '',
        "评分": movie_scores[0].strip() if movie_scores else '',
        "语言": movie_languages[0].strip() if movie_languages else '',
        "导演": ",".join(movie_directors) if movie_directors else '',
        "作者": ",".join(movie_authors) if movie_authors else '',
        "宣传语": movie_slogans[0].strip() if movie_slogans else '',
        "简介": movie_descriptions[0].strip() if movie_descriptions else ''
    }

    return data_clean(movie_info)


def data_clean(movie_info):
    for key in movie_info.keys():
        value = movie_info[key]
        if value == '':
            continue

        match key:
            case "年份":
                match_res = re.search(r"\d{4}", value)
                if match_res:
                    movie_info[key] = match_res.group()
            case "上映时间":
                match_res = re.search(r"\d{2}/\d{2}/\d{4}", value)
                if match_res:
                    movie_info[key] = match_res.group()
            case "时长":
                h_res = re.search(r"(\d+)h", value)
                m_res = re.search(r"(\d+)m", value)
                hour = int(h_res.group(1)) if h_res else 0
                minute = int(m_res.group(1)) if m_res else 0
                movie_info[key] = str(hour * 60 + minute) + "m"
            case _:
                pass

    return movie_info


def save_all_movies(all_movies, page):
    print(f"开始保存电影数据... len(movies)={len(all_movies)}")
    if not all_movies:
        return

    with open(TOP_MOVIE_CSV_PATH, 'w' if page == 1 else 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, all_movies[0].keys())
        if page == 1:
            writer.writeheader()

        writer.writerows(all_movies)


def main():
    page_num = TOP_MOVIE_NUM // 20

    for page in range(1, page_num + 1):
        # 1.发送请求,获取电影榜单数据
        print(f"开始获取第{page}页电影列表数据...")

        if page == 1:
            response = requests.get(TMDB_BASE_URL + TMDB_TOP_PAGE_1_URL, timeout=60, headers=headers)
        else:
            response = requests.post(TMDB_BASE_URL + TMDB_TOP_PAGE_OTHER_URL, data=TMDB_TOP_PAGE_OTHER_BODY % page,
                                     timeout=60, headers=headers)

        # 2.解析数据,获取电影列表
        document = html.fromstring(response.text)
        movie_list = document.xpath(f"//*[@id='page_{page}']/div[@class='card style_1']")

        # 3.遍历电影列表,获取详情数据
        all_movies = []
        for movie in movie_list:
            movie_detail_urls = movie.xpath("./div/div/a/@href")
            if movie_detail_urls:
                movie_detail_url = TMDB_BASE_URL + movie_detail_urls[0]
                # 请求电影详情数据
                movie_detail = get_movie_detail(movie_detail_url)
                all_movies.append(movie_detail)

        # 4.保存电影数据到csv文件
        save_all_movies(all_movies, page)


if __name__ == '__main__':
    main()
