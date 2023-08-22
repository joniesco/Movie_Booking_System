from pymongo import MongoClient

# Connect to the MongoDB database
client = MongoClient('mongodb://localhost:27017/')
db = client['movie_booking']
movies_collection = db['movies']

# Delete all documents from the collection
result = movies_collection.delete_many({})

# Print the number of deleted documents
print(f"Deleted {result.deleted_count} documents from the collection.")
