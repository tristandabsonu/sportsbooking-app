from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    pw_hash  = db.Column(db.String(128), nullable=False)
    role     = db.Column(db.String(10), default='member')  # 'admin' / 'member'
    bookings = db.relationship('Booking', backref='user',
                            cascade='all, delete-orphan')

class Availability(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time   = db.Column(db.DateTime, nullable=False)

    bookings   = db.relationship('Booking', back_populates='availability',
                                cascade='all, delete-orphan')

class Booking(db.Model):
    id             = db.Column(db.Integer, primary_key=True)
    user_id        = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    availability_id= db.Column(db.Integer, db.ForeignKey('availability.id'), nullable=False)

    availability = db.relationship('Availability', back_populates='bookings')

class Image(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    s3_key    = db.Column(db.String(255), nullable=False)   # = uploads/filename
    uploaded  = db.Column(db.DateTime, default=datetime.utcnow)

