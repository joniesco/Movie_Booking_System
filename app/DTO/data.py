import db

db_instance = db.db
movies_collection = db_instance['movies']


# Insert mock movie data into the movies collection handly, 
# can be done at the creat_movie method at the movie.py module
# Notice than by this insertetion the limits are not verified this insertion is just for handly insertetion of mock data only

mock_movie_data = [
    {
        "title": "The Lion King",
        "description": "An epic adventure",
        "day": "01-09-2023",
        "start_time": "14:00",
        "end_time": "16:00",
        "available_tickets": 10
    },
    {
        "title": "Mowgli: Legend of the Jungle",
        "description": "Jungle adventure",
        "day": "01-09-2023",
        "start_time": "16:30",
        "end_time": "18:30",
        "available_tickets": 15
    },
    {
        "title": "Doctor Strange",
        "description": "Marvel superhero",
        "day": "02-09-2023",
        "start_time": "14:00",
        "end_time": "16:00",
        "available_tickets": 8
    },
    {
        "title": "John Wick",
        "description": "Action thriller",
        "day": "02-09-2023",
        "start_time": "18:00",
        "end_time": "20:00",
        "available_tickets": 12
    },
    {
        "title": "The Notebook",
        "description": "Romantic drama",
        "day": "03-09-2023",
        "start_time": "15:00",
        "end_time": "17:00",
        "available_tickets": 20
    }
]

movies_collection.insert_many(mock_movie_data)
print("Movie mock data inserted successfully-please make sure that more then 3 movies do not play at the same time")
