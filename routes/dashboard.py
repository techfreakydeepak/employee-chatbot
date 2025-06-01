from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import User, Message

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'manager':
        return "Unauthorized", 403
    employees = User.query.filter_by(role='employee').all()
    messages = Message.query.all()
    return render_template('dashboard.html', employees=employees, messages=messages)
