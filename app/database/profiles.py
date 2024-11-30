from app.config import db

class Profiles(db.Model):

    id = db.Column(db.Integer, primary_key=True, default=None)
    age = db.Column(db.Integer, nullable=False, default=None)
    name = db.Column(db.String(50), nullable=False, default=None)
    city = db.Column(db.String(100), nullable=False, default=None)
    description = db.Column(db.Text, nullable=False, default=None)
    search_sex = db.Column(db.Integer, nullable=False, default=None)
    sex = db.Column(db.Integer, nullable=False, default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return '<Users %r>' % self.id