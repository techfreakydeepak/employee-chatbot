from flask import Blueprint, render_template
from flask_socketio import emit
from flask_login import login_required

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat')
@login_required
def chat():
    return render_template('chat.html')

def init_chat_socket(socketio):
    @socketio.on('send_message')
    def handle_send_message(data):
        # Broadcast message to all clients
        emit('receive_message', data, broadcast=True)
