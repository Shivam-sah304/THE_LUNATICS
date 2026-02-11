from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(40),nullable=False)
    address=db.Column(db.String(50),nullable=False)
    def __init__(self) ->str:
        return f"{self.id}-{self.name}"
    