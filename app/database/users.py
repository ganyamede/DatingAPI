from datetime import datetime
from app.config import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gmail = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255), nullable=True)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Users %r>' % self.id