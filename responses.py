import pandas as pd
import numpy as np
from pulldata import get_query, get_recommend
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import SequenceMatcher
import random

threshold = 0.3

all_menus = {
    'main' : {
        'search' : 
            ('search find look','Sure thing. Would you like to search by title or genre?'),
        'recommend' :
            ('suggest recommend','Of course. Please provide a short description on what type of movie you would like')
    },
    'search' : {
        'Title' : 
            ('title','Whats the title'),
        'Genre' :
            ('genre','Whats the genre')
    },
    'Title' : {'s':''},
    'Genre' : {'s':''},
    'recommend' : {'r' : ''}

}

def get_Chat_response(level,text):
    
    qns = all_menus.get(level)

    result = 'Sorry I couldnt understand that'
    state = level

    if 's' in qns.keys():
        ans = get_query(level,text)
        return return_movie(level,ans),state
    
    elif 'r' in qns.keys():
        ans = get_recommend(text)
        return return_movie(level,ans),state

    else:
        highest = 0
        for k,v in qns.items():
            score = SequenceMatcher(None, v[0], text).ratio()
            if score > threshold and score > highest:
                highest = score
                result = v[1]
                state = k
        
        return result,state
    
def display_movie(movie):
    title = movie.get('Title')
    year = movie.get('Year')
    duration = movie.get('Duration')
    genre = ' '.join(movie.get('Genre'))
    rating = movie.get('Rating')
    image = movie.get('Image')
    trailer = movie.get('Trailer')
    reviews = movie.get('Reviews')
    description = movie.get('Description')

    html = '''
    <div>
        <img class="movie__poster" src ='''+image+'''>
        <h3>'''+title+'''</h3>
        <p>'''+year+'<br>'+duration+'<br>'+genre+'<br>'+rating+'''</p><br>
        <p>'''+description+'''</p><br>
        <a href='''+trailer+'''target="_blank">Watch trailer</a><br>
        <a href='''+reviews+'''target="_blank">See reviews</a>
    </div>
    '''
    return html

def return_movie(level,ans):
    if len(ans):
        if level == "Genre":
            result = display_movie(ans[random.randint(0,len(ans)-1)])
        else:
            result = display_movie(ans[0])
    else:
        result = 'Sorry no results found'
    return result


