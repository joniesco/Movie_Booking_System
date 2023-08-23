from DTO.db import db

# Testing via postman
movies_collection = db['movies']
sample_movie = movies_collection.find_one()
print(sample_movie)
