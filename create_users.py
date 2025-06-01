from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def create_users():
    with app.app_context():
        manager = User.query.filter_by(email='manager@123gmail.com').first()
        if not manager:
            manager = User(
                email='manager@123gmail.com',
                password=generate_password_hash('123'),
                role='Manager'
            )
            db.session.add(manager)
            print("Manager user created.")
        else:
            print("Manager user already exists.")

        employee = User.query.filter_by(email='employee@123gmail.com').first()
        if not employee:
            employee = User(
                email='employee@123gmail.com',
                password=generate_password_hash('123'),
                role='Employee'
            )
            db.session.add(employee)
            print("Employee user created.")
        else:
            print("Employee user already exists.")

        db.session.commit()
        print("User creation process completed.")

if __name__ == '__main__':
    create_users()
