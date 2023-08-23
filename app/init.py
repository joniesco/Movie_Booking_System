from flask import Flask

app = Flask(__name__)

# Import the Blueprints for movie and booking routes
from app.routes.path import movie_bp
from app.routes.path import booking_bp

# Register the movie_bp and the booking_bp Blueprints with the Flask app
app.register_blueprint(movie_bp)
app.register_blueprint(booking_bp)

# Start the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)
