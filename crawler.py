import numpy as np
import pandas as pd
import requests as rq
from bs4 import BeautifulSoup

class Crawler:

    def __init__(self):
        self.__soup = {}
        self.__releaseDate = ''
        self.__runTime = ''
        self.__filmCorporation = ''
        self.__IMDbScore = ''
        self.__titleTw = ''
        self.__titleEn = ''
        self.__filmTypes = ''
        self.__director = ''
        self.__actors = ''
        self.__officialLinks = ''
        self.__storeInfo = ''

    def setSoup(self, url):
        response = rq.get(str(url))
        self.__soup = BeautifulSoup(response.text, "lxml")

    @property
    def titleTw(self):
        return self.__titleTw

    @property
    def titleEn(self):
        return self.__titleEn

    @property
    def runTime(self):
        return self.__runTime

    @property
    def filmCorporation(self):
        return self.__filmCorporation

    @property
    def IMDbScore(self):
        return self.__IMDbScore

    @property
    def filmTypes(self):
        return self.__filmTypes

    @property
    def director(self):
        return self.__director

    @property
    def actors(self):
        return self.__actors

    @property
    def officialLinks(self):
        return self.__officialLinks

    @property
    def storeInfo(self):
        return self.__storeInfo

    @property
    def releaseDate(self):
        return self.__releaseDate

    def run(self):
        mainTag = self.__soup.find("div", id = "content_l")
        movieIntroTag = mainTag.find('div', class_ = 'movie_intro_info_r')
        datas = [child.string.strip().replace(u'\u3000', u'').split('：') for child in movieIntroTag.find_all('span')]

        try:
            self.__titleTw = movieIntroTag.h1.string
        except:
            self.__titleTw = np.nan
            print("Error: Couldn't find Traditional Chinese title.")

        try:
            self.__titleEn = movieIntroTag.h3.string
        except:
            self.__titleEn = np.nan
            print("Error: Couldn't find English title.")

        try:
            self.__filmTypes = ', '.join([child.find('a').get_text().strip() for child in movieIntroTag.find_all('div', class_ = 'level_name')])
        except:
            self.__filmTypes = np.nan
            print("Error: Couldn't find filmTypes.")

        try:
            self.__director = movieIntroTag.select("span + div")[0].get_text().strip()
        except:
            self.__director = np.nan
            print("Error: Couldn't find director.")

        try:
            self.__officialLinks = [child.string.strip() for child in movieIntroTag.select("span + a")]
        except:
            self.__officialLinks = np.nan
            print("Error: Couldn't find officialLinks.")

        try:
            self.__actors = ', '.join([child.get_text().strip() for child in movieIntroTag.select("span + div")[1].find_all('a')])
        except:
            self.__actors = np.nan
            print("Error: Couldn't find actors.")

        try:
            self.__storeInfo = mainTag.find('div', class_ = 'storeinfo').get_text()
        except:
            self.__storeInfo = np.nan
            print("Error: Couldn't find storeinfo.")

        for data in datas:
            if (data[0] == '上映日期'):
                try:
                    self.__releaseDate = data[1]
                except:
                    self.__releaseDate = np.nan
                    print("Error: Couldn't find releaseDate.")
                pass
            if (data[0] == '片長'):
                try:
                    self.__runTime = data[1]
                except:
                    self.__runTime = dnp.nan
                    print("Error: Couldn't find runTime.")
                pass
            if (data[0] == '發行公司'):
                try:
                    self.__filmCorporation = data[1]
                except:
                    self.__filmCorporation = np.nan
                    print("Error: Couldn't find fileCorporation.")
                pass
            if (data[0] == 'IMDb分數'):
                try:
                    self.__IMDbScore = data[1]
                except:
                    self.__IMDbScore = np.nan
                    print("Error: Couldn't find releaseDate.")
                pass

    def getDataFrame(self):
        ptt_nba_dict = {
            "電影名稱(中)": self.titleTw,
            "電影名稱(英)": self.titleEn,
            "上映日期": self.releaseDate,
            "類型": self.filmTypes,
            "片長": self.runTime,
            "導演": self.director,
            "演員": self.actors,
            "發行公司": self.filmCorporation,
            "IMDb分數": self.IMDbScore,
            "劇情介紹": self.storeInfo,
            "官方連結": self.officialLinks,
        }

        return pd.DataFrame(ptt_nba_dict)

url = 'https://tw.movies.yahoo.com/movieinfo_main.html/id=5644'

# initialize
crawler = Crawler()
crawler.setSoup(url)
crawler.run()
df = crawler.getDataFrame()

# format dataframe style
result = df.style
result = result.set_properties(**{'text-align': 'left'})
result.set_table_styles(
    # select the table header with th and set it right align
    [dict(selector="th", props=[("text-align", "left")])]
)

result
