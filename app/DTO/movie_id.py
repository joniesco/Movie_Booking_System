from pymongo import MongoClient

# Connect to the MongoDB database
client = MongoClient('mongodb://localhost:27017/')
db = client['movie_booking']
movies_collection = db['movies']

# Query all movies and create a dictionary with movie names and their _id values
movie_dict = {}
for movie in movies_collection.find():
    movie_id = str(movie['_id'])
    movie_title = movie['title']
    movie_dict[movie_title] = movie_id

# Print the dictionary
print("Movie IDs:")
for movie_title, movie_id in movie_dict.items():
    print(f"Movie: {movie_title}, ID: {movie_id}")
