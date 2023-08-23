from flask import Blueprint, jsonify, request
from app.Models.booking import Booking
from app.DTO import db

# Create a Blueprint named 'booking' for booking-related routes
booking_bp = Blueprint('booking', __name__)

# Route for booking a ticket
@booking_bp.route('/book', methods=['POST'])
def book_ticket():
    data = request.json      # Extract JSON data from the request
    booking = Booking()
    response = booking.book_ticket(data)
    return jsonify(response), response['status_code']     # Return a JSON response along with the appropriate HTTP status code


# Route for canceling a booked ticket
@booking_bp.route('/cancel', methods=['DELETE'])
def cancel_ticket():
    data = request.json
    booking = Booking()
    response = booking.cancel_ticket(data)
    return jsonify(response), response['status_code']     # Return a JSON response along with the appropriate HTTP status code

