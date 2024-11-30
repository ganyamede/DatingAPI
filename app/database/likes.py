from datetime import datetime
from app.config import db


class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    liker_id = db.Column(db.Integer) # Кто
    liked_id = db.Column(db.Integer) # Кому
    liked_message = db.Column(db.Text)
    liked_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    liked_state = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Users %r>' % self.id