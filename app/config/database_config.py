from app.config import db, app

def create_table():
    with app.app_context():
        db.create_all()