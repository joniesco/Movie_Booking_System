from app.DTO import db
from datetime import datetime
from bson import ObjectId
import uuid

class Booking:
    def book_ticket(self, data):
        user_personal_id = data.get('personal_id')
        movie_id = data.get('movie_id')
        movie = db.movies.find_one({'_id': ObjectId(movie_id)})
        if not movie:
            return {"error": "Movie not found.", "status_code": 404}

        start_time = datetime.strptime(movie['start_time'], '%H:%M').time()
        end_time = datetime.strptime(movie['end_time'], '%H:%M').time()

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
            return {"error": "You can't book tickets for movies that run at the same time.", "status_code": 400}

        if user_day_booking_count >= 2:
            return {"error": "You can't book tickets for more than two movies in a day.", "status_code": 400}

        db.movies.update_one({'_id': ObjectId(movie_id)}, {'$inc': {'available_tickets': -1}})
        ticket_id = str(uuid.uuid4())
        booking = {
            'movie_id': movie_id,
            'personal_id': user_personal_id,
            'day': movie['day'],
            'ticket_id': ticket_id
        }
        db.bookings.insert_one(booking)

        return {"message": "Ticket booked successfully!", "ticket_id": ticket_id, "status_code": 201}
    
    def cancel_ticket(self, data):
        user_personal_id = data.get('personal_id')
        user_ticket_id = data.get('ticket_id')

        booking = db.bookings.find_one({
            'ticket_id': user_ticket_id,
            'personal_id': user_personal_id
        })
        if not booking:
            return {"error": "Ticket not found or not owned by the user.", "status_code": 404}

        movie_id = booking['movie_id']

        db.movies.update_one({'_id': ObjectId(movie_id)}, {'$inc': {'available_tickets': 1}})
        db.bookings.delete_one({'ticket_id': user_ticket_id, 'personal_id': user_personal_id})

        return {"message": "Ticket canceled successfully!", "status_code": 200}
