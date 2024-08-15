# app/models.py

from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    sent_mails = db.Column(db.Integer, nullable=False)
    activity_time = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    pdf_file = db.Column(db.String(120))

    def __repr__(self):
        return f'<User {self.username}>'