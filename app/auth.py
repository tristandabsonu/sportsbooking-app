from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, User
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/')

bcrypt = Bcrypt()

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        pw    = bcrypt.generate_password_hash(request.form['password']).decode()
        db.session.add(User(email=email, pw_hash=pw))  # auto-member role
        db.session.commit()
        flash('Registered successfully; please log in.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth_bp.route('/', methods=['GET', 'POST'])
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pw    = request.form['password']
        user  = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.pw_hash, pw):
            # Promote to admin if email matches env var
            if email == os.getenv('ADMIN_EMAIL'):
                user.role = 'admin'
                db.session.commit()
            login_user(user)
            return redirect('/admin' if user.role == 'admin' else '/member')
        flash('Bad credentials')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
