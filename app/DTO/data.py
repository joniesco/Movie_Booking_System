from pymongo import MongoClient

# Create a MongoDB client and connect to the database
client = MongoClient('mongodb://localhost:27017/')
db = client['movie_booking']

# Define your collection name
movies_collection = db['movies']

# Define the mock movie data
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

# Insert mock movie data into the collection
movies_collection.insert_many(mock_movie_data)

print("Mock movie data inserted successfully!")
