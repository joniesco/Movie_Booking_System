import db

db_instance = db.db
movies_collection = db_instance['movies']

#This module is responsible to delete all documents from the data base and reset it.

result = movies_collection.delete_many({})

# Print the number of deleted documents and sucssesful message
print(f"Deleted {result.deleted_count} documents from the collection.")
print("The data base is clear now")

