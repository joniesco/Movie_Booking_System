from flask import Blueprint, jsonify, request
from app.Models.booking import Booking
from app.DTO import db
import uuid

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/book', methods=['POST'])
def book_ticket():
    data = request.json
    booking = Booking()
    response = booking.book_ticket(data)
    return jsonify(response), response['status_code']

@booking_bp.route('/cancel', methods=['DELETE'])
def cancel_ticket():
    data = request.json
    booking = Booking()
    response = booking.cancel_ticket(data)
    return jsonify(response), response['status_code']
