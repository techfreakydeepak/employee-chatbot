from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user
from models import User
from extensions import db
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    if current_user.is_authenticated:
        if current_user.role == 'manager':
            return redirect(url_for('dashboard.dashboard'))
        else:
            return redirect(url_for('chat.chat'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('role')

        user = User.query.filter_by(email=email, role=role).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.role == 'manager':
                return redirect(url_for('dashboard.dashboard'))
            else:
                return redirect(url_for('chat.chat'))
        error = "Invalid credentials or role. Please try again."
    return render_template('login.html', error=error)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
