from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(40),nullable=False)
    address=db.Column(db.String(50),nullable=False)
    phone=db.Column(db.String(20),nullable=False)
    degree=db.Column(db.String(30),nullable=False)
    specialization=db.Column(db.String(40),nullable=True)
    desc=db.Column(db.String(400),nullable=True)
    dob=db.Column(db.Date,nullable=False)
    experience=db.Column(db.Integer,nullable=False)

    # password=db.Column(db.String(30),nullable=False)
    # photo=db.Column(db.String(40),nullable=False)
    # nmc_number=db.Column(db.String(50),nullable=False)
    # nmc_photo=db.column(db.string(100),nullable=False)

    
    