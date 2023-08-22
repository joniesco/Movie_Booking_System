from pymongo import MongoClient

# Connect to the MongoDB database
client = MongoClient('mongodb://localhost:27017/')
db = client['movie_booking']
movies_collection = db['movies']

# Fetch a sample movie document from the database
sample_movie = movies_collection.find_one()

# Print the structure of the sample movie document
print(sample_movie)
