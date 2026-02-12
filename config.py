import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = "supersecretkey"

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "doctor.db")

SQLALCHEMY_TRACK_MODIFICATIONS = False
