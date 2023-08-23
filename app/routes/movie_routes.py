from flask import Blueprint, jsonify, request
from app.Models.movie import Movie
from app.DTO import db

# Create a Blueprint named 'movie' for movie-related routes
movie_bp = Blueprint('movie', __name__)

# Route for creating a movie
@movie_bp.route('/movies', methods=['POST'])
def create_movie():
    data = request.json # extreact json form request 
    movie = Movie()
    movie_id = movie.create_movie(data)
    return jsonify({"message": "Movie created successfully!", "movie_id": movie_id}), 201 # return related response ans SC

# Route for getting all movies showing on a specific day (by parameter) 
@movie_bp.route('/movies', methods=['GET'])
def get_available_movies():
    day = request.args.get('day') # Get the value of the 'day' parameter from the query
    if not day: # Check if the 'day' parameter is a good input
        return jsonify({"error": "Day parameter is missing."}), 400
    movie = Movie()
    available_movies = movie.get_available_movies(day)
    return jsonify({"available_movies": available_movies}), 200
