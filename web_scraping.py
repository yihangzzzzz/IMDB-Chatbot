import nltk
import numpy as np
import random
import string 
import bs4 as bs
import urllib.request as rq
import re
import pandas as pd
import pymongo
from pymongo import MongoClient

def get_data(x):
    req = rq.Request(url=x,headers={'User-Agent': 'Mozilla/5.0'})
    link = rq.urlopen(req).read()
    data = bs.BeautifulSoup(link, 'lxml')
    return data

url = 'https://www.imdb.com/chart/top/'
# url = 'https://www.imdb.com/' + movie_url

data = get_data(url)

# all_movies_df = pd.DataFrame(columns=['title', 'year', 'duration', 'trailer', 'rating', 'review'])

all_movies = data.find_all('li', attrs = {'class' : 'ipc-metadata-list-summary-item sc-10233bc-0 iherUv cli-parent'})
# print(all_movies)
cluster = MongoClient("mongodb+srv://imdbchatbot:IMDBchatbot2024@chatbot.zgtjddk.mongodb.net/?retryWrites=true&w=majority&appName=Chatbot")
db = cluster["IMDB"]
collection = db["Top 250 Movies"]

for movie in all_movies:
    movie_url = 'https://www.imdb.com/'+movie.a['href']
#     print(movie_url)
    cur_movie = get_data(movie_url)
    
    title = cur_movie.find('h1', attrs = {'data-testid' : 'hero__pageTitle'}).text
    year = cur_movie.find_all('a', attrs = {'class' : 'ipc-link ipc-link--baseAlt ipc-link--inherit-color'})[5].text
    duration = cur_movie.find_all('li', attrs = {'class' : 'ipc-inline-list__item', 'role' : 'presentation'})[6].text
    trailer = cur_movie.find('a', attrs = {'class' : 'ipc-lockup-overlay ipc-focusable', 'data-testid':"videos-slate-overlay-1"})
    if trailer is not None:
        trailer = 'https://www.imdb.com/'+trailer['href']
    genres = cur_movie.find('div', attrs = {'data-testid' : 'genres', 'class' :'ipc-chip-list--baseAlt ipc-chip-list' })
    genres = genres.find_all('a', attrs = {'class':'ipc-chip ipc-chip--on-baseAlt'})
    genres = list(i.text for i in genres)
    rating = cur_movie.find('div', attrs = {'data-testid' : 'hero-rating-bar__aggregate-rating__score'}).text[0:3]
    review = 'https://www.imdb.com/'+cur_movie.find('ul', attrs = {'class' : 'ipc-inline-list sc-9e83797f-0 jflJlf baseAlt', 'data-testid':"reviewContent-all-reviews"}).li.a['href']
    
    print(title)
    add_movie = {'Title':title,"Year":year,"Duration":duration,"Trailer":trailer,"Genre":genres,"Rating":rating,"Reviews":review}
    collection.insert_one(add_movie)
    # all_movies_df.loc[len(all_movies_df.index)] = [title,year,duration,trailer,rating,review]

# all_movies_df.head()

