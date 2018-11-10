# Filename : davidfengCrawlLab.py
# Created by : 馮文龍
# License : GPL v2
# output file : ./outputs/davidfeng.txt

###
# 抓取yahoo!電影的某部電影, 例如:
# ○ https://tw.movies.yahoo.com/movieinfo_main.html/id=5644
# ○ 需要抓取的資訊如下:
# ■ 電影名稱 (中英)
# ■ 上映日期 u 類 型 u 片 長 u 導 演 u 演 員 u 發行公司 u 官方網站 u 劇情介紹
# ■ 將擷取出來的資料存檔，檔名: 編號.txt
###

from reppy.robots import Robots
import requests
from html.parser import HTMLParser
from html.entities import name2codepoint
import os


class MyHTMLParser(HTMLParser):
    movie_info_focus = False
    chinese_title_data_focus = False
    english_title_data_focus = False
    movie_category_focus = False
    director_focus = False
    website_focus = False
    actors_focus = False
    intro_focus = False
    __title_en = ''
    __title_zh = ''
    __categories = ''
    __info = {}
    __actors = ''
    __website = ''
    __intro = ''

    @property
    def title_en(self):
        return self.__title_en

    @property
    def title_zh(self):
        return self.__title_zh

    @property
    def categories(self):
        return self.__categories

    @property
    def info(self):
        return self.__info

    @property
    def actors(self):
        return self.__actors

    @property
    def website(self):
        return self.__website

    @property
    def intro(self):
        return self.__intro

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for attr in attrs:
                if attr[0] == 'class' and attr[1] == 'movie_intro_info_r': # start parsing movie info
                    self.movie_info_focus = True
                elif self.movie_info_focus and attr[0] == 'class' and attr[1] == 'level_name':
                    self.movie_category_focus = True
                elif self.movie_info_focus and attr[0] == 'class' and attr[1] == 'movie_intro_list':
                    if not self.director_focus:
                        self.director_focus = True
                    else:
                        self.director_focus = False
                        self.actors_focus = True
                elif attr[0] == 'class' and attr[1] == 'gray_infobox storeinfo':
                    self.intro_focus = True

        if self.movie_info_focus:
            if tag == 'h1':
                self.chinese_title_data_focus = True
            if tag == 'h3':
                self.english_title_data_focus = True
            if tag == 'dl':
                for attr in attrs:
                    if attr[0] == 'class' and attr[1] == 'evaluatebox': # end parsing movie info
                        self.movie_info_focus = False

    def handle_endtag(self, tag):
        if self.movie_category_focus:
            if tag == 'div':
                self.movie_category_focus = False
        elif self.chinese_title_data_focus:
            if tag == 'h1':
                self.chinese_title_data_focus = False
        elif self.english_title_data_focus:
            if tag == 'h3':
                self.english_title_data_focus = False
        elif self.intro_focus and tag == 'span':
            self.intro_focus = False

    def handle_data(self, data):
        if data.strip() == '、':
            return

        if self.chinese_title_data_focus:
            self.__title_zh = self.__title_zh + data.strip()
        elif self.english_title_data_focus:
            self.__title_en = self.__title_en + data.strip()
        elif self.movie_category_focus and data.strip() != '':
            self.__categories = self.__categories + data.strip() + ' '
        elif self.director_focus and data.strip() != '':
            if data.strip() == '演員：':
                self.__info['演員'] = '';
            else:
                self.__info['導演'] = data.strip()
        elif self.actors_focus and data.strip() != '':
            if data.strip() == '官方連結：':
                self.__info['官方連結'] = ''
                self.actors_focus = False
                self.website_focus = True
            else:
                self.__info['演員'] = self.__info['演員'] + data.strip() + ','
        elif self.website_focus and data.strip() != '':
            self.__info['官方連結'] = data.strip()
            self.__info['演員'] = self.__info['演員'][:-1] # remove the trailing ','
            self.website_focus = False
        elif self.movie_info_focus and data.strip() != '':
            dict_item = data.split('：')
            if dict_item[0] != 'IMDb分數':
                self.__info[dict_item[0]] = dict_item[1]
        elif self.intro_focus and data.strip() != '':
            self.__intro = data.strip()

    def handle_decl(self, data):
        pass


robots_url = "https://tw.movies.yahoo.com/robots.txt"
site_url = "https://tw.movies.yahoo.com/movieinfo_main.html/id=5644"
parser = MyHTMLParser()

# 讀取 robots.txt 判斷是否允許瀏覽
robot = Robots.fetch(robots_url)
sitemaps = robot.sitemaps
is_allowed = robot.allowed(site_url, '*')

print('網頁 url:', site_url)
for sitemap in sitemaps:
    print("sitemap :", sitemap)
    print('sitemap 可存取? ', robot.allowed(sitemap, '*'))

print('網頁可存取 ? -> ', is_allowed)
print()

if is_allowed:
    req = requests.get(site_url, timeout=5)
    parser.feed(req.text)
    try:
        if not os.path.exists('outputs'):
            os.makedirs('outputs')
    except OSError:
        print('Error: Creating directory "outputs". ')
    f = open("outputs/davidfeng.txt", "w")
    print('中文片名:', parser.title_zh)
    f.write('中文片名:'+parser.title_zh+"\n")
    print('Movie\'s Title:', parser.title_en)
    f.write('Movie\'s Title:' + parser.title_en+"\n")
    print('類型:', parser.categories)
    f.write('類型:' + parser.categories+"\n")
    for item in parser.info:
        print(item, ':', parser.info[item])
        f.write(item + ':' + parser.info[item]+"\n")
    print('劇情介紹:', parser.intro)
    f.write('劇情介紹:' + parser.intro+"\n")
    f.close()
else:
    print("網頁不允許訪問")



