from datetime import datetime
from app.config import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    profile_id = db.Column(db.Integer)
    photo = db.Column(db.LargeBinary, nullable=False, default=None)

    def __repr__(self):
        return '<Users %r>' % self.id