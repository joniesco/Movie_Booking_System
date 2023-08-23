from pymongo import MongoClient

# Create a MongoClient instance connecting to the local MongoDB server
client = MongoClient('mongodb://localhost:27017/')

# Access the 'movie_booking' database
db = client['movie_booking']  
