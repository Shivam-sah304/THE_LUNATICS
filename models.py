from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Doctor(db.Model):
    # id = db.Column(db.Integer, nullable=False)
    name=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(40),nullable=False)
    address=db.Column(db.String(50),nullable=False)
    phone=db.Column(db.String(20),primary_key=True)
    degree=db.Column(db.String(30),nullable=False)
    specialization=db.Column(db.String(40),nullable=True)
    desc=db.Column(db.String(400),nullable=True)
    dob=db.Column(db.Date,nullable=False)
    experience=db.Column(db.Integer,nullable=False)

    password=db.Column(db.String(30),nullable=True)
    photo=db.Column(db.String(40),nullable=True)
    nmc_number=db.Column(db.String(50),nullable=True)
    nmc_photo=db.Column(db.String(100),nullable=True)

    
    