import db

db_instance = db.db
movies_collection = db_instance['movies']

#Prints the id next to the movie title in case we want the id not to be shown

movie_dict = {}
for movie in movies_collection.find():
    movie_id = str(movie['_id'])
    movie_title = movie['title']
    movie_dict[movie_title] = movie_id

print("Movie IDs:")
for movie_title, movie_id in movie_dict.items():
    print(f"Movie: {movie_title}, ID: {movie_id}")
