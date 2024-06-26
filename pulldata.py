import pymongo
from pymongo import MongoClient
from difflib import SequenceMatcher
import re
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# from gensim.models import Word2Vec
# from gensim.utils import simple_preprocess
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')

cluster = MongoClient("mongodb+srv://imdbchatbot:IMDBchatbot2024@chatbot.zgtjddk.mongodb.net/?retryWrites=true&w=majority&appName=Chatbot")
db = cluster["IMDB"]
collection = db["Top 250 Movies"]

def get_query(att,value):
  rgx = re.compile('.*'+value+'.*', re.IGNORECASE)
  ans = []
  for x in collection.find({att:rgx}):
    ans.append(x)
  # if att == "Genre":
  #   random_index = random.randint(0, len(ans)-1)
  #   ans.insert(0, ans.pop(random_index))
  return ans

def get_recommend(text):
  all_movies = collection.find()
  descriptions = [d['Sypnosis'] for d in all_movies]
  vectorizer = TfidfVectorizer()
  tfidf_matrix = vectorizer.fit_transform(descriptions)
  query_vector = vectorizer.transform([text])
  similarities = list(cosine_similarity(query_vector, tfidf_matrix)[0])
  result_index = similarities.index(max(similarities))
  ans = collection.find_one({"Movie_ID":result_index})
  return [ans]

#   model = Word2Vec(descriptions, vector_size=100, window=5, min_count=1, sg=0)
    
#   descriptions.pop()
    
#   vectors = []
#   for d in descriptions:
#       vectors.append(model.wv[d])
#   query_vector = model.wv[query_tokens]

#   similarities = [cosine_similarity(query_vector.mean(axis=0).reshape(1, -1), pv.mean(axis=0).reshape(1, -1)) for pv in vectors]

#   result_index = similarities.index(max(similarities))
#   ans = collection.find_one({"Movie_ID":result_index})
#   return [ans]

# movie = get_query('Ttile','dune')
# print(movie)


  
