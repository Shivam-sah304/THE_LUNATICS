import os

# Secret key
SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")  # use env var if set

# Upload folder
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # project root
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

# SQLite database URI
DB_NAME = "doctor.db"
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, DB_NAME)}"

# SQLAlchemy settings
SQLALCHEMY_TRACK_MODIFICATIONS = False
