import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///user.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'pdf'}
    SECRET_KEY = 'your-secret-key'  # Change this to a random secret key