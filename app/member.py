from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from .models import db, Booking, Availability, Image

member_bp = Blueprint('member', __name__, url_prefix='/member')

@member_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    taken_ids = [b.availability_id for b in Booking.query.all()]
    avail = Availability.query.filter(~Availability.id.in_(taken_ids)).all()

    image = Image.query.first()
    image_path = image.s3_key if image else None

    return render_template('member.html',
                           bookings=bookings,
                           avail=avail,
                           image_url=image_path)

@member_bp.post('/api/bookings/book')
@login_required
def book():
    avail_id = request.form['availability_id']
    db.session.add(Booking(user_id=current_user.id, availability_id=avail_id))
    db.session.commit()
    return redirect('/member')

@member_bp.post('/api/bookings/delete')
@login_required
def delete_booking():
    db.session.delete(Booking.query.get(request.form['booking_id']))
    db.session.commit()
    return redirect('/member')
