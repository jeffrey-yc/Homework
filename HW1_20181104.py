# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 08:49:39 2018
@author: Lian-Jie Wang
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup

def movie_crawler(url):
    html = requests.get(url)
    script = BeautifulSoup(html.text, "html.parser")
    info_of_movie = script.select(".movie_intro_info_r")
    #print(info_of_movie)

    ''' Name of movie in Chinese'''
    movie_name_cn = info_of_movie[0].find_all("h1")
    nameCN = str(movie_name_cn[0].text)
    #print("Name of movie in Chinese ：", nameCN)

    '''Name of movie in English'''
    movie_name_en = info_of_movie[0].find_all("h3")
    nameEN = str(movie_name_en[0].text)   
    #print("Name of movie in English ：", nameEN)

    '''Release of movie'''
    info_of_movie_span = info_of_movie[0].find_all("span")
    release = str(info_of_movie_span[0].text[5:])
    #print("Release of movie ：", release)

    '''Category of movie'''
    info_of_movie_category=info_of_movie[0].select(".level_name_box")
    movie_category=info_of_movie_category[0].find_all('a', {"class":"gabtn"})
    tmp=[]
    for i in range(len(movie_category)):
        tmp += movie_category[i].text.replace(' ','').replace("\n", "'")
    category = ''.join(tmp)
    #print("Category of movie ：",category)

    '''Time of movie'''
    movie_time = info_of_movie_span[1]
    time = movie_time.text[5:]
    #print("Time of movie ：", time)

    '''Director of movie''' 
    list_of_movie_into = script.select(".movie_intro_list")
    movie_director = list_of_movie_into[0].text.replace(' ','').replace('\n','')
    director = ''.join(movie_director)
    #print("Director of movie :", director)

    '''Actor of movie'''
    movie_actor = list_of_movie_into[1].text.replace(' ','').replace('\n','')
    actor = ''.join(movie_actor)
    #print("Actor of movie :", actor)

    '''Movie distributor'''
    movie_company = info_of_movie_span[2]
    company = movie_company.text[5:]
    #print("Movie distributor ：", company)

    '''Official movie website'''
    movie_website = info_of_movie[0].find_all('a', {'class':'gabtn'})[-1].text
    website = movie_website
    #print("Official movie website ：", website)

    '''Story''' 
    info_of_movie2 = script.select(".l_box_inner")[4].find_all('span')
    story = info_of_movie2[0].text.replace(' ','').replace('\n','')
    #print("Story ：", story)

    # Output as pandas's DataFrame
    index_of_movie=['NameCN', 'NameEN', 'Release', 'Category', 'Time',
                    'Director', 'Actor', 'Company', 'Website', 'Story']
    list_of_movie=[nameCN, nameEN, release, category, time,
                   director, actor, company, website, story]
    result=pd.DataFrame(list_of_movie, index=index_of_movie, 
                        columns=["content"])
    return result
url = "https://movies.yahoo.com.tw/movieinfo_main.html/id=8511"
print(movie_crawler(url))
