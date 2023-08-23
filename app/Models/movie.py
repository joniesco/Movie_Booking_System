from app.DTO import db
from datetime import datetime

class Movie:
    def create_movie(self, data):

        # Handle invalid time format
        try:
            # Convert start_time and end_time strings to time objects
            start_time = datetime.strptime(data['start_time'], '%H:%M').time()
            end_time = datetime.strptime(data['end_time'], '%H:%M').time()
        except ValueError:
            return {"error": "Invalid time format. Use HH:MM.", "status_code": 400}
        
        # Ensure end_time is after start_time
        if end_time <= start_time:
            return {"error": "End time must be after start time.", "status_code": 400}
        
        # Check if day is in correct format (DD-MM-YYYY)
        try:
            datetime.strptime(data['day'], '%d-%m-%Y')
        except ValueError:
            return {"error": "Invalid day format. Use DD-MM-YYYY.", "status_code": 400}
        
        # Get all movies on the specified day
        existing_movies = db.movies.find({
            'day': data['day']
        })
        
        conflicting_movies = 0
        for existing_movie in existing_movies:
            
             # Convert existing movie's start_time and end_time to time objects so we can compare
            existing_start_time = datetime.strptime(existing_movie['start_time'], '%H:%M').time()
            existing_end_time = datetime.strptime(existing_movie['end_time'], '%H:%M').time()

            if start_time <= existing_end_time and end_time >= existing_start_time:
                conflicting_movies += 1

        if conflicting_movies >= 3:
            return {"error": "There are already 3 movies playing at the same time.", "status_code": 400}

        new_movie = {
            'title': data['title'],
            'description': data['description'],
            'day': data['day'],
            'start_time': data['start_time'],
            'end_time': data['end_time'],
            'available_tickets': data['available_tickets']
        }
        # Insert the new movie into the 'movies' collection
        result = db.movies.insert_one(new_movie)
        movie_id = str(result.inserted_id)
        return {"message": "Movie created successfully!", "movie_id": movie_id, "status_code": 201} #Getting the movie Id for bookings to this movie
    
    def get_available_movies(self, day):
        # Find available movies for the specified day within the entire day
        available_movies = db.movies.find({
            'day': day,
            'start_time': {'$gte': '00:00'},
            'end_time': {'$lte': '23:59'}
        })

        movies_list = []
        for movie in available_movies:
            # Create a list of movie details
            movies_list.append({
                'movie_id': str(movie['_id']),
                'title': movie['title'],
                'description': movie['description'],
                'start_time': movie['start_time'],
                'end_time': movie['end_time'],
                'available_tickets': movie['available_tickets']
            })

        return movies_list
