import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://imdbchatbot:IMDBchatbot2024@chatbot.zgtjddk.mongodb.net/?retryWrites=true&w=majority&appName=Chatbot")
db = cluster["IMDB"]
collection = db["Top 250 Movies"]

post = {"title":"Toy Story", "year":2017, "rating":6.7}

# collection.insert_one(post)
collection.delete_one(post)