import os

# ----------------- Secret -----------------
SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")  # Can override via environment

# ----------------- Uploads -----------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")  # cross-platform

# ----------------- Database -----------------
DB_NAME = "doctor.db"
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, DB_NAME)}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

