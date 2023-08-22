from flask import Blueprint, jsonify, request
from app.Models.movie import Movie
from app.DTO import db

movie_bp = Blueprint('movie', __name__)

@movie_bp.route('/movies', methods=['POST'])
def create_movie():
    data = request.json
    movie = Movie()
    movie_id = movie.create_movie(data)
    return jsonify({"message": "Movie created successfully!", "movie_id": movie_id}), 201

@movie_bp.route('/movies', methods=['GET'])
def get_available_movies():
    day = request.args.get('day')
    if not day:
        return jsonify({"error": "Day parameter is missing."}), 400
    movie = Movie()
    available_movies = movie.get_available_movies(day)
    return jsonify({"available_movies": available_movies}), 200
