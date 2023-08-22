from flask import Flask

app = Flask(__name__)


from app.routes.path import movie_bp
from app.routes.path import booking_bp

app.register_blueprint(movie_bp)
app.register_blueprint(booking_bp)

if __name__ == '__main__':
    app.run(debug=True)
