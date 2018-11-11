
#-------------------------------------------
# 匯入必要模組
#-------------------------------------------
from selenium import webdriver
from html.parser import HTMLParser


#-------------------------------------------
# 定義一個HTML解譯類別
#-------------------------------------------
class MyHTMLParser(HTMLParser):
    content=''
    print=False

    def handle_data(self, data):
        if data.strip()=='驚奇4超人':
            self.print=True

        if '期待度' in data.strip():
            self.print=False
        if data.strip()=='劇情介紹':
            self.print=True

        if '展開劇情簡介' in data.strip():
            self.print=False

        if self.print:
            self.content+=data

    def get_content(self):
        return self.content

#-------------------------------------------
# 載入Chrome驅動程式
#-------------------------------------------
driver = webdriver.Chrome("chromedriver.exe")


#-------------------------------------------
# 待拜訪的網址
#-------------------------------------------
urls=[
	'https://movies.yahoo.com.tw/movieinfo_main.html/id=5644'
	]


#-------------------------------------------
# 依序將範例網址交給瀏覽器
#-------------------------------------------
for url in urls:
    driver.get(url)

    # 取得網頁原始碼
    with open('out.txt', 'w', encoding='utf-8') as outfile:
        pageSource = driver.page_source

        #-------------------------------------------
        # 取出沒有標籤的內容
        #-------------------------------------------
        parser = MyHTMLParser()
        parser.feed(pageSource)

        content=parser.get_content()
        print(content)

        outfile.write(content)


#-------------------------------------------
# 關閉Chrome驅動程式
#-------------------------------------------
driver.close()
