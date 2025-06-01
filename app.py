from flask import Flask
import openai
import os

from extensions import db, login_manager, socketio

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.secret_key = 'your-secret-key'

    # Use instance path for database file
    db_path = os.path.join(app.instance_path, 'chatbot.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except Exception as e:
        print("Error creating instance folder:", e)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    socketio.init_app(app, cors_allowed_origins="*")

    openai.api_key = "your-openai-api-key"

    # Import and register blueprints inside function to avoid circular imports
    from routes.auth import auth_bp
    from routes.chat import chat_bp, init_chat_socket
    from routes.dashboard import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(dashboard_bp)

    # User loader for login manager
    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))

    # Initialize chat socket events
    init_chat_socket(socketio)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app

# Create app instance
app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True)
