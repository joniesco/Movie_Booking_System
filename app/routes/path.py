from flask import request, jsonify,Blueprint
# from app.models import Movie
from app.DTO.db import db
from datetime import datetime
from bson import ObjectId
import uuid


movie_bp = Blueprint('movie', __name__)
booking_bp = Blueprint('booking', __name__)



@movie_bp.route('/movies', methods=['POST'])
def create_movie():
    data = request.json

    # Convert start_time and end_time to datetime objects
    try:
        start_time = datetime.strptime(data['start_time'], '%H:%M').time()
        end_time = datetime.strptime(data['end_time'], '%H:%M').time()
    except ValueError:
        return jsonify({"error": "Invalid time format. Use HH:MM."}), 400
    

    # Check if end_time is after start_time
    if end_time <= start_time:
        return jsonify({"error": "End time must be after start time."}), 400

    try:
        datetime.strptime(data['day'], '%d-%m-%Y')
    except ValueError:
        return jsonify({"error": "Invalid day format. Use DD-MM-YYYY."}), 400
    # Check for conflicting movies
    existing_movies = db.movies.find({
        'day': data['day']
    })
    
    conflicting_movies = 0
    for existing_movie in existing_movies:
        existing_start_time = datetime.strptime(existing_movie['start_time'], '%H:%M').time()
        existing_end_time = datetime.strptime(existing_movie['end_time'], '%H:%M').time()

        if start_time <= existing_end_time and end_time >= existing_start_time:
            conflicting_movies += 1

    if conflicting_movies >= 3:
        return jsonify({"error": "There are already 3 movies playing at the same time."}), 400

    # Insert new movie
    new_movie = {
        'title': data['title'],
        'description': data['description'],
        'day': data['day'],
        'start_time': data['start_time'],
        'end_time': data['end_time'],
        'available_tickets': data['available_tickets']
    }
    result = db.movies.insert_one(new_movie)

    movie_id = str(result.inserted_id)

    return jsonify({"message": "Movie created successfully!", "movie_id": movie_id}), 201


@movie_bp.route('/movies', methods=['GET'])
def get_available_movies():
    day = request.args.get('day')
    if not day:
        return jsonify({"error": "Day parameter is missing."}), 400

    # Query the database to get available movies
    available_movies = db.movies.find({
        'day': day,
        'start_time': {'$gte': '00:00'},
        'end_time': {'$lte': '23:59'}
    })

    movies_list = []
    for movie in available_movies:
        movies_list.append({
            'movie_id': str(movie['_id']),
            'title': movie['title'],
            'description': movie['description'],
            'start_time': movie['start_time'],
            'end_time': movie['end_time'],
            'available_tickets': movie['available_tickets']
        })

    return jsonify({"available_movies": movies_list}), 200

@booking_bp.route('/book', methods=['POST'])
def book_ticket():
    data = request.json

    # Check for user's booking limitations
    user_personal_id = data.get('personal_id')
    movie_id = data.get('movie_id')
    
    # Fetch 'day' from the movie details
    movie = db.movies.find_one({'_id': ObjectId(movie_id)})
    if not movie:
        return jsonify({"error": "Movie not found."}), 404

    # Extract start_time and end_time from the movie
    start_time = datetime.strptime(movie['start_time'], '%H:%M').time()
    end_time = datetime.strptime(movie['end_time'], '%H:%M').time()

    # Query user's bookings for the specific personal ID and day
    user_day_bookings = db.bookings.find({
        'personal_id': user_personal_id,
        'day': movie['day']
    })

    user_day_booking_count = db.bookings.count_documents({
        'personal_id': user_personal_id,
        'day': movie['day']
    })

    conflicting_bookings = 0
    for existing_booking in user_day_bookings:
        existing_movie_id = existing_booking['movie_id']
        existing_movie = db.movies.find_one({'_id': ObjectId(existing_movie_id)})

        existing_start_time = datetime.strptime(existing_movie['start_time'], '%H:%M').time()
        existing_end_time = datetime.strptime(existing_movie['end_time'], '%H:%M').time()

        if start_time <= existing_end_time and end_time >= existing_start_time:
            conflicting_bookings += 1

    if conflicting_bookings > 0:
        return jsonify({"error": "You can't book tickets for movies that run at the same time."}), 400

    if user_day_booking_count >= 2:
        return jsonify({"error": "You can't book tickets for more than two movies in a day."}), 400

    # Decrease available_tickets and insert booking
    db.movies.update_one({'_id': ObjectId(movie_id)}, {'$inc': {'available_tickets': -1}})
    ticket_id = str(uuid.uuid4())
    booking = {
        'movie_id': movie_id,
        'personal_id': user_personal_id,
        'day': movie['day'],
        'ticket_id': ticket_id
    }
    db.bookings.insert_one(booking)

    return jsonify({"message": "Ticket booked successfully!", "ticket_id": ticket_id}), 201